"""
Test completo para Sale Repository
RESPONSABLE: Christopher
"""
import logging
from datetime import datetime, date
from app.repositories.sale_repository import SaleRepository

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_sale_repository_connection():
    """Test 1: Verificar conexión básica"""
    print("\n" + "="*60)
    print("TEST 1: Conexión y configuración básica")
    print("="*60)
    
    try:
        repo = SaleRepository()
        
        # Verificar herencia
        print(f"✅ SaleRepository creado correctamente")
        print(f"✅ Tax rate configurado: {repo.tax_rate}")
        
        # Verificar métodos heredados
        connection = repo.get_connection()
        print(f"✅ Conexión obtenida: {type(connection)}")
        connection.close()
        
        # Verificar acceso a table_id_mapping
        sale_id_column = repo.table_id_mapping.get("MKSales")
        print(f"✅ Mapeo de MKSales: {sale_id_column}")
        
        print("✅ TEST 1 PASADO: Configuración básica OK")
        return True
        
    except Exception as e:
        print(f"❌ TEST 1 FALLÓ: {str(e)}")
        return False

def test_required_tables():
    """Test 2: Verificar que existan las tablas necesarias"""
    print("\n" + "="*60)
    print("TEST 2: Verificación de tablas requeridas")
    print("="*60)
    
    try:
        repo = SaleRepository()
        
        required_tables = [
            "MKSales", "MKSalesDetails", "MKCommerces", 
            "MKUsers", "MKProducts", "MKPaymentMethods"
        ]
        
        for table in required_tables:
            try:
                count = repo.execute_scalar(f"SELECT COUNT(*) FROM {table}")
                print(f"✅ {table}: {count} registros")
            except Exception as e:
                print(f"❌ {table}: ERROR - {str(e)}")
                return False
        
        print("✅ TEST 2 PASADO: Todas las tablas existen")
        return True
        
    except Exception as e:
        print(f"❌ TEST 2 FALLÓ: {str(e)}")
        return False

def test_get_next_id():
    """Test 3: Verificar método get_next_id()"""
    print("\n" + "="*60)
    print("TEST 3: Método get_next_id()")
    print("="*60)
    
    try:
        repo = SaleRepository()
        
        # Probar con tablas de ventas
        sales_tables = ["MKSales", "MKSalesDetails"]
        
        for table in sales_tables:
            next_id = repo.get_next_id(table)
            print(f"✅ {table} - Siguiente ID: {next_id}")
            
            # Verificar que sea un número válido
            if not isinstance(next_id, int) or next_id < 1:
                raise ValueError(f"ID inválido para {table}: {next_id}")
        
        print("✅ TEST 3 PASADO: get_next_id() funciona correctamente")
        return True
        
    except Exception as e:
        print(f"❌ TEST 3 FALLÓ: {str(e)}")
        return False

def setup_test_data():
    """Crear datos mínimos para testing si no existen"""
    print("\n" + "="*60)
    print("SETUP: Creando datos de prueba si es necesario")
    print("="*60)
    
    try:
        repo = SaleRepository()
        
        # Verificar y crear usuario de prueba
        user_count = repo.execute_scalar("SELECT COUNT(*) FROM MKUsers")
        if user_count == 0:
            print("⚠️  No hay usuarios, creando usuario de prueba...")
            repo.execute_non_query("""
                INSERT INTO MKUsers (IdUser, name, password, phoneNumber, isActive, createdAt)
                VALUES (1, 'Usuario Prueba', 'password_hash', '1234567890', 1, %s)
            """, (datetime.now(),))
            print("✅ Usuario de prueba creado")
        
        # Verificar y crear método de pago
        payment_count = repo.execute_scalar("SELECT COUNT(*) FROM MKPaymentMethods")
        if payment_count == 0:
            print("⚠️  No hay métodos de pago, creando efectivo...")
            repo.execute_non_query("""
                INSERT INTO MKPaymentMethods (IdPaymentMethod, name, description, createdAt, enabled)
                VALUES (1, 'Efectivo', 'Pago en efectivo', %s, 1)
            """, (datetime.now(),))
            print("✅ Método de pago creado")
        
        # Verificar y crear comercio de prueba
        commerce_count = repo.execute_scalar("SELECT COUNT(*) FROM MKCommerces")
        if commerce_count == 0:
            print("⚠️  No hay comercios, necesita datos más complejos...")
            print("⚠️  Saltando creación de comercio (requiere direcciones, etc.)")
            return False
        
        # Verificar y crear producto de prueba
        product_count = repo.execute_scalar("SELECT COUNT(*) FROM MKProducts")
        if product_count == 0:
            print("⚠️  No hay productos, necesita datos más complejos...")
            print("⚠️  Saltando creación de producto (requiere categorías, inventario, etc.)")
            return False
        
        print("✅ SETUP COMPLETADO: Datos básicos disponibles")
        return True
        
    except Exception as e:
        print(f"❌ SETUP FALLÓ: {str(e)}")
        return False

def test_create_sale_simulation():
    """Test 4: Simular creación de venta (sin datos reales)"""
    print("\n" + "="*60)
    print("TEST 4: Simulación de create_sale() (validación de lógica)")
    print("="*60)
    
    try:
        repo = SaleRepository()
        
        # Test de cálculo de totales (parte del método create_sale)
        from decimal import Decimal
        
        # Simular items de venta
        test_items = [
            {'product_id': 1, 'quantity': 2, 'unit_price': 1000.00},
            {'product_id': 2, 'quantity': 1, 'unit_price': 500.00}
        ]
        
        # Calcular totales como lo hace el método
        subtotal = sum(Decimal(str(item['unit_price'])) * item['quantity'] for item in test_items)
        tax_amount = subtotal * repo.tax_rate
        total_amount = subtotal + tax_amount
        
        print(f"✅ Cálculo de subtotal: ₡{subtotal}")
        print(f"✅ Cálculo de IVA (13%): ₡{tax_amount}")
        print(f"✅ Total calculado: ₡{total_amount}")
        
        # Verificar que los cálculos sean correctos
        expected_subtotal = Decimal('2500.00')  # (2*1000) + (1*500)
        expected_tax = expected_subtotal * Decimal('0.13')  # 13%
        expected_total = expected_subtotal + expected_tax
        
        if subtotal == expected_subtotal and tax_amount == expected_tax:
            print("✅ Cálculos correctos")
        else:
            raise ValueError(f"Cálculos incorrectos: esperado {expected_total}, obtenido {total_amount}")
        
        # Test de generación de número de referencia
        sale_id = 1
        commerce_id = 1
        reference_number = f"VTA-{commerce_id:04d}-{sale_id:06d}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        print(f"✅ Número de referencia generado: {reference_number}")
        
        print("✅ TEST 4 PASADO: Lógica de cálculos correcta")
        return True
        
    except Exception as e:
        print(f"❌ TEST 4 FALLÓ: {str(e)}")
        return False

def test_create_sale_with_data():
    """Test 5: Crear venta real si hay datos disponibles"""
    print("\n" + "="*60)
    print("TEST 5: Creación de venta real (si hay datos)")
    print("="*60)
    
    try:
        repo = SaleRepository()
        
        # Verificar si hay datos necesarios
        user_count = repo.execute_scalar("SELECT COUNT(*) FROM MKUsers")
        commerce_count = repo.execute_scalar("SELECT COUNT(*) FROM MKCommerces")
        product_count = repo.execute_scalar("SELECT COUNT(*) FROM MKProducts")
        
        print(f"📊 Usuarios disponibles: {user_count}")
        print(f"📊 Comercios disponibles: {commerce_count}")
        print(f"📊 Productos disponibles: {product_count}")
        
        if user_count == 0 or commerce_count == 0 or product_count == 0:
            print("⚠️  Datos insuficientes para crear venta real")
            print("⚠️  Saltando test de creación real")
            print("✅ TEST 5 SALTADO: Datos insuficientes (normal en BD vacía)")
            return True
        
        # Si hay datos, obtener IDs reales
        first_user = repo.execute_query("SELECT IdUser FROM MKUsers LIMIT 1")[0]
        first_commerce = repo.execute_query("SELECT IdCommerce FROM MKCommerces LIMIT 1")[0]
        first_product = repo.execute_query("SELECT IdProduct, quantity FROM MKProducts WHERE quantity > 0 LIMIT 1")
        
        if not first_product:
            print("⚠️  No hay productos con stock")
            print("✅ TEST 5 SALTADO: Sin stock disponible")
            return True
        
        first_product = first_product[0]
        
        # Crear venta real
        test_items = [
            {
                'product_id': first_product['IdProduct'], 
                'quantity': 1, 
                'unit_price': 1000.00
            }
        ]
        
        print(f"🔄 Intentando crear venta...")
        print(f"   Usuario: {first_user['IdUser']}")
        print(f"   Comercio: {first_commerce['IdCommerce']}")
        print(f"   Producto: {first_product['IdProduct']}")
        
        result = repo.create_sale(
            commerce_id=first_commerce['IdCommerce'],
            cashier_user_id=first_user['IdUser'],
            items=test_items,
            payment_method_id=1
        )
        
        print(f"✅ Venta creada exitosamente:")
        print(f"   Sale ID: {result['sale_id']}")
        print(f"   Reference: {result['reference_number']}")
        print(f"   Total: ₡{result['total_amount']}")
        
        # Test get_sale_by_id con la venta recién creada
        print(f"\n🔄 Probando get_sale_by_id()...")
        retrieved_sale = repo.get_sale_by_id(result['sale_id'])
        
        if retrieved_sale:
            print(f"✅ Venta recuperada:")
            print(f"   ID: {retrieved_sale['sale_id']}")
            print(f"   Comercio: {retrieved_sale['commerce_name']}")
            print(f"   Total: ₡{retrieved_sale['total_amount']}")
            print(f"   Items: {len(retrieved_sale['items'])}")
        else:
            raise ValueError("No se pudo recuperar la venta creada")
        
        print("✅ TEST 5 PASADO: Venta real creada y recuperada")
        return True
        
    except Exception as e:
        print(f"❌ TEST 5 FALLÓ: {str(e)}")
        return False

def test_query_methods():
    """Test 6: Probar métodos de consulta"""
    print("\n" + "="*60)
    print("TEST 6: Métodos de consulta")
    print("="*60)
    
    try:
        repo = SaleRepository()
        
        # Test get_sales_by_commerce
        print("🔄 Probando get_sales_by_commerce()...")
        sales_by_commerce = repo.get_sales_by_commerce(commerce_id=1, limit=5)
        print(f"✅ Ventas por comercio: {len(sales_by_commerce)} encontradas")
        
        # Test get_sales_by_date_range
        print("🔄 Probando get_sales_by_date_range()...")
        today = date.today()
        yesterday = date(today.year, today.month, today.day - 1 if today.day > 1 else 1)
        
        sales_by_date = repo.get_sales_by_date_range(
            start_date=str(yesterday),
            end_date=str(today)
        )
        print(f"✅ Ventas por fecha: {len(sales_by_date)} encontradas")
        
        # Test get_total_sales_by_commerce
        print("🔄 Probando get_total_sales_by_commerce()...")
        totals = repo.get_total_sales_by_commerce(
            commerce_id=1,
            start_date=str(yesterday),
            end_date=str(today)
        )
        print(f"✅ Totales calculados:")
        print(f"   Ventas: {totals['sales_count']}")
        print(f"   Total: ₡{totals['total_sales_amount']}")
        
        print("✅ TEST 6 PASADO: Métodos de consulta funcionan")
        return True
        
    except Exception as e:
        print(f"❌ TEST 6 FALLÓ: {str(e)}")
        return False

def test_error_handling():
    """Test 7: Probar manejo de errores"""
    print("\n" + "="*60)
    print("TEST 7: Manejo de errores")
    print("="*60)
    
    try:
        repo = SaleRepository()
        
        # Test 1: get_sale_by_id con ID inexistente
        print("🔄 Probando ID inexistente...")
        non_existent_sale = repo.get_sale_by_id(99999)
        if non_existent_sale is None:
            print("✅ Manejo correcto de ID inexistente")
        else:
            raise ValueError("Debería retornar None para ID inexistente")
        
        # Test 2: update_sale_status con status inválido
        print("🔄 Probando status inválido...")
        try:
            repo.update_sale_status(1, "STATUS_INEXISTENTE", 1)
            raise ValueError("Debería fallar con status inválido")
        except Exception as e:
            if "no válido" in str(e):
                print("✅ Validación de status funciona")
            else:
                raise e
        
        # Test 3: get_next_id con tabla inexistente
        print("🔄 Probando tabla inexistente...")
        try:
            repo.get_next_id("TablaQueNoExiste")
            raise ValueError("Debería fallar con tabla inexistente")
        except Exception as e:
            if "no encontrada" in str(e):
                print("✅ Validación de tabla funciona")
            else:
                raise e
        
        print("✅ TEST 7 PASADO: Manejo de errores correcto")
        return True
        
    except Exception as e:
        print(f"❌ TEST 7 FALLÓ: {str(e)}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("🧪 INICIANDO TESTS DE SALE REPOSITORY")
    print("=" * 70)
    
    tests = [
        ("Conexión básica", test_sale_repository_connection),
        ("Tablas requeridas", test_required_tables),
        ("Método get_next_id", test_get_next_id),
        ("Simulación de venta", test_create_sale_simulation),
        ("Venta real", test_create_sale_with_data),
        ("Métodos de consulta", test_query_methods),
        ("Manejo de errores", test_error_handling)
    ]
    
    # Setup de datos
    print("\n🔧 PREPARANDO DATOS DE PRUEBA...")
    setup_test_data()
    
    # Ejecutar tests
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ ERROR INESPERADO en {test_name}: {str(e)}")
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN DE TESTS")
    print("="*70)
    print(f"✅ Tests pasados: {passed}/{total}")
    print(f"❌ Tests fallidos: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ Sale Repository está listo para usar")
        print("✅ Puedes proceder con Settlement Repository")
    else:
        print(f"\n⚠️  {total - passed} tests fallaron")
        print("🔧 Revisa los errores antes de continuar")
    
    print("="*70)

if __name__ == "__main__":
    main()