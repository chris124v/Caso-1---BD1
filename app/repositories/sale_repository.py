"""
Operaciones de ventas (sales), esto nos ayudara luego para los stored procedures

"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from decimal import Decimal
from app.repositories.base_repository import BaseRepository

# Repositorio especifico para ventas
class SaleRepository(BaseRepository):
    
    def __init__(self):
        super().__init__()
        self.tax_rate = Decimal('0.13')  # 13% IVA de Costa Rica
    
    #Crea una nueva venta
    def create_sale(self, commerce_id: int, cashier_user_id: int, items: List[Dict], 
                   payment_method_id: int = 1) -> Dict[str, Any]:
        """
        Estos serian los parametros necesarios para crear una venta
            commerce_id: Id del comercio
            cashier_user_id: Id del cajero
            items: Lista de items [{'product_id': int, 'quantity': int, 'unit_price': float}]
            payment_method_id: ID del método de pago utilizado
        """
        connection = None

        try:

            #Conexion con la base de datos
            connection = self.get_connection()
            connection.begin()
            
            # 1. Calcular totales
            subtotal = sum(Decimal(str(item['unit_price'])) * item['quantity'] for item in items)
            tax_amount = subtotal * self.tax_rate
            total_amount = subtotal + tax_amount
            
            # 2. Crear venta principal, usamos un numero de referencia unico
            sale_id = self.get_next_id("MKSales")
            reference_number = f"VTA-{commerce_id:04d}-{sale_id:06d}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            with connection.cursor() as cursor:

                # Insertar venta con el query
                cursor.execute("""
                    INSERT INTO MKSales (
                        IdSale, IDCommerceFK2, saleDate, saleStatus, subTotalAmount,
                        discountAmount, taxAmount, totalAmount, paymentStatus,
                        invoiceRequired, receiptGenerated, IDPaymentMethodFK,
                        IDcashierUserFK, referenceNumber, createdAt, updatedAt, checksum
                    ) VALUES (
                        %s, %s, %s, 'COMPLETED', %s, 0, %s, %s, 'COMPLETED', 
                        0, 0, %s, %s, %s, %s, %s, %s
                    )
                """, (
                    sale_id, commerce_id, datetime.now(), subtotal, tax_amount, 
                    total_amount, payment_method_id, cashier_user_id, reference_number,
                    datetime.now(), datetime.now(), b'checksum_placeholder'
                ))
                
                # 3. Crear detalles de venta 
                for item in items: #Itera sobre cada producto de la venta 
                    detail_id = self.get_next_id("MKSalesDetails")
                    line_total = Decimal(str(item['unit_price'])) * item['quantity']
                    
                    #Ejecuta la insercion en la tabala MKSalesDetails
                    cursor.execute("""
                        INSERT INTO MKSalesDetails (
                            IdSaleDetails, IDSaleFK, IDProductFK3, productName,
                            quantitySold, unitMeasure, unitPrice, listPrice,
                            costPrice, lineTotal, inventoryUpdated, createdAt
                        ) VALUES (
                            %s, %s, %s, 'Producto', %s, 'unidad', %s, %s, %s, %s, 1, %s
                        )
                    """, (
                        detail_id, sale_id, item['product_id'], item['quantity'],
                        item['unit_price'], item['unit_price'], item['unit_price'],
                        line_total, datetime.now()
                    ))
                    
                    # 4. Actualizar inventario del producto en especifico
                    cursor.execute("""
                        UPDATE MKProducts 
                        SET quantity = quantity - %s 
                        WHERE IdProduct = %s
                    """, (item['quantity'], item['product_id']))
            
            #Confirmamos la transaccion
            connection.commit()
            
            # 5. Log de operacion
            self.log_operation(
                user_id=cashier_user_id,
                operation="CREATE_SALE",
                description=f"Venta creada: ID={sale_id}, Total=${total_amount}",
                reference_id1=sale_id,
                reference_id2=commerce_id
            )
            
            #Retorna diccionario con los resultados 
            return {
                'success': True,
                'sale_id': sale_id,
                'reference_number': reference_number,
                'total_amount': float(total_amount),
                'items_count': len(items)
            }
        
        #Manejo de errores con la creacion de una venta
        except Exception as e:
            if connection:
                connection.rollback()
            raise Exception(f"Error creando venta: {str(e)}")
        
        #Corta la conexion con la base de datos
        finally:
            if connection:
                connection.close()
    
    # Este metodo nos sirve para obtener una venta por su ID
    def get_sale_by_id(self, sale_id: int) -> Optional[Dict[str, Any]]:
        
        try:
            # Datos principales de la venta
            sale_query = """
                SELECT s.*, c.name as commerce_name, u.name as cashier_name
                FROM MKSales s
                JOIN MKCommerces c ON s.IDCommerceFK2 = c.IdCommerce
                JOIN MKUsers u ON s.IDcashierUserFK = u.IdUser
                WHERE s.IdSale = %s
            """
            
            #Ejecuta el query usando el metodo heredado del repositoprio base
            sale_data = self.execute_query(sale_query, (sale_id,))

            #Esto seria si no hay resultados
            if not sale_data:
                return None
            
            #Obtiene la primera fila (deberia ser unica)
            sale = sale_data[0]
            
            # Detalles de la venta
            details_query = """
                SELECT sd.*, p.name as product_name
                FROM MKSalesDetails sd
                JOIN MKProducts p ON sd.IDProductFK3 = p.IdProduct
                WHERE sd.IDSaleFK = %s
            """
            
            #Ejecuta el query de detalles
            details = self.execute_query(details_query, (sale_id,))
            
            #Construye el resultado final
            return {
                'sale_id': sale['IdSale'],
                'commerce_name': sale['commerce_name'],
                'cashier_name': sale['cashier_name'],
                'sale_date': sale['saleDate'].isoformat() if sale['saleDate'] else None,
                'status': sale['saleStatus'],
                'total_amount': float(sale['totalAmount']),
                'reference_number': sale['referenceNumber'],
                'items': [
                    {
                        'product_name': detail['product_name'],
                        'quantity': detail['quantitySold'],
                        'unit_price': float(detail['unitPrice']),
                        'line_total': float(detail['lineTotal'])
                    }
                    for detail in details
                ]
            }
        
        #Error en caso de que no se obtenga la venta 
        except Exception as e:
            raise Exception(f"Error obteniendo venta {sale_id}: {str(e)}")
    
    #Obtener ventas por comercio 
    def get_sales_by_commerce(self, commerce_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        
        # Limit seria la cantidad maxima de ventas a obtener
        # manejo de excepciones, realizamos el query para obtener las ventas por comercio 
        try:
            query = """
                SELECT s.IdSale, s.saleDate, s.totalAmount, s.referenceNumber,
                       u.name as cashier_name, COUNT(sd.IdSaleDetails) as items_count
                FROM MKSales s
                JOIN MKUsers u ON s.IDcashierUserFK = u.IdUser
                LEFT JOIN MKSalesDetails sd ON s.IdSale = sd.IDSaleFK
                WHERE s.IDCommerceFK2 = %s
                GROUP BY s.IdSale, s.saleDate, s.totalAmount, s.referenceNumber, u.name
                ORDER BY s.saleDate DESC
                LIMIT %s
            """
            
            # Ejecuta el query
            results = self.execute_query(query, (commerce_id, limit))
            
            # Construye la lista de ventas
            return [
                {
                    'sale_id': sale['IdSale'],
                    'sale_date': sale['saleDate'].isoformat() if sale['saleDate'] else None,
                    'total_amount': float(sale['totalAmount']),
                    'reference_number': sale['referenceNumber'],
                    'cashier_name': sale['cashier_name'],
                    'items_count': sale['items_count']
                }
                for sale in results
            ]
        
        #Manejo de errores en caso de que no se obtengan las ventas por comercio
        except Exception as e:
            raise Exception(f"Error obteniendo ventas del comercio {commerce_id}: {str(e)}")
    
    #Este metodo nos sirve para obtener ventas en un rango de fechas
    def get_sales_by_date_range(self, start_date: str, end_date: str, commerce_id: Optional[int] = None) -> List[Dict[str, Any]]:
        
        # Manejo de excepciones, realizamos el query para obtener las ventas por rango de fechas, recordemos que %s es un placeholder para parametros
        try:
            query = """
                SELECT s.IdSale, s.IDCommerceFK2, s.saleDate, s.totalAmount,
                       c.name as commerce_name
                FROM MKSales s
                JOIN MKCommerces c ON s.IDCommerceFK2 = c.IdCommerce
                WHERE DATE(s.saleDate) BETWEEN %s AND %s
            """
            #Los parametros para el query son la fecha de inicio y fin
            params = [start_date, end_date]
            
            #Si se proporciona un ID de comercio, lo agregamos al query
            if commerce_id:
                query += " AND s.IDCommerceFK2 = %s"
                params.append(commerce_id)
            
            #Ordenamos los resultados por fecha de venta descendente
            query += " ORDER BY s.saleDate DESC"
            
            #Ejecuta el query con los parametros
            results = self.execute_query(query, tuple(params))
            
            #Construye la lista de ventas por fecha 
            return [
                {
                    'sale_id': sale['IdSale'],
                    'commerce_id': sale['IDCommerceFK2'],
                    'commerce_name': sale['commerce_name'],
                    'sale_date': sale['saleDate'].isoformat() if sale['saleDate'] else None,
                    'total_amount': float(sale['totalAmount'])
                }
                for sale in results
            ]
        
        #Manejo de errores en caso de que no se obtengan las ventas por fecha
        except Exception as e:
            raise Exception(f"Error obteniendo ventas por fecha: {str(e)}")
    
    #Metodo para actualizar el status de una venta
    def update_sale_status(self, sale_id: int, new_status: str, user_id: int) -> bool:
        
        #Manejo de excepciones, actualizamos el status de una venta con los estados validadados
        try:
            valid_statuses = ['PENDING', 'COMPLETED', 'CANCELED', 'REFUNDED']
            if new_status not in valid_statuses:
                raise ValueError(f"Status '{new_status}' no válido")
            
            #Define las filas afectadas por la actualizacion
            affected_rows = self.execute_non_query(
                "UPDATE MKSales SET saleStatus = %s, updatedAt = %s WHERE IdSale = %s",
                (new_status, datetime.now(), sale_id)
            )
            
            #Si se actualizo al menos una fila, registramos la operacion en el log
            if affected_rows > 0:
                self.log_operation(
                    user_id=user_id,
                    operation="UPDATE_SALE_STATUS",
                    description=f"Status actualizado a '{new_status}'",
                    reference_id1=sale_id
                )
                return True
            
            return False
        
        #Manejo de errores en caso de que no se actualice el status de la venta
        except Exception as e:
            raise Exception(f"Error actualizando status: {str(e)}")
    
    #Metodo para obtener totales de ventas por comercio para la parte de liquidaciones
    def get_total_sales_by_commerce(self, commerce_id: int, start_date: str, end_date: str) -> Dict[str, Any]:
        
        #Manejo de excepciones, realizamos el query para obtener los totales de ventas por comercio en un rango de fechas
        try:
            query = """
                SELECT 
                    COUNT(*) as sales_count,
                    COALESCE(SUM(totalAmount), 0) as total_sales_amount,
                    COALESCE(SUM(subTotalAmount), 0) as total_subtotal,
                    COALESCE(SUM(taxAmount), 0) as total_tax
                FROM MKSales 
                WHERE IDCommerceFK2 = %s 
                AND DATE(saleDate) BETWEEN %s AND %s 
                AND saleStatus = 'COMPLETED'
            """
            
            #Ejecuta el query con los parametros de comercio y fechas
            result = self.execute_query(query, (commerce_id, start_date, end_date))
            
            #Si hay resultados, los retornamos en un diccionario
            if result:
                return {
                    'commerce_id': commerce_id,
                    'period_start': start_date,
                    'period_end': end_date,
                    'sales_count': result[0]['sales_count'],
                    'total_sales_amount': float(result[0]['total_sales_amount']),
                    'total_subtotal': float(result[0]['total_subtotal']),
                    'total_tax': float(result[0]['total_tax'])
                }
            
            #Si no hay resultados, retornamos ceros
            return {
                'commerce_id': commerce_id,
                'period_start': start_date,
                'period_end': end_date,
                'sales_count': 0,
                'total_sales_amount': 0.0,
                'total_subtotal': 0.0,
                'total_tax': 0.0
            }
        
        #Manejo de errores en caso de que no se obtengan los totales de ventas por comercio
        except Exception as e:
            raise Exception(f"Error calculando totales: {str(e)}")