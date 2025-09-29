"""
Test completo para Sale Service

"""
import logging
from datetime import date
from app.services.sale_service import SaleService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_sale_service_initialization():
    """Test 1: Verificar inicialización del servicio"""
    print("\n" + "="*60)
    print("TEST 1: Inicialización de Sale Service")
    print("="*60)
    
    try:
        service = SaleService()
        print(f" Sale Service creado correctamente")
        print(f" Sale Repository inicializado: {type(service.sale_repository)}")
        print(f" Base Repository inicializado: {type(service.base_repository)}")
        print(" TEST 1 PASADO")
        return True
    except Exception as e:
        print(f" TEST 1 FALLÓ: {str(e)}")
        return False

def test_process_sale():
    """Test 2: Procesar una venta completa"""
    print("\n" + "="*60)
    print("TEST 2: Procesar venta completa")
    print("="*60)
    
    try:
        service = SaleService()
        
        # Datos de prueba
        test_items = [
            {'product_id': 1, 'quantity': 2, 'unit_price': 1200.00},
            {'product_id': 2, 'quantity': 1, 'unit_price': 1500.00}
        ]
        
        print(" Procesando venta con 2 productos...")
        result = service.process_sale(
            commerce_id=2,
            cashier_user_id=2,
            items=test_items,
            payment_method_id=1
        )
        
        print(f" Venta procesada exitosamente:")
        print(f"   Sale ID: {result['sale_id']}")
        print(f"   Reference: {result['reference_number']}")
        print(f"   Total: ₡{result['total_amount']:,.2f}")
        print(f"   Items: {result['items_count']}")
        print(f"   Comercio: {result['commerce_name']}")
        
        print(" TEST 2 PASADO")
        return True
        
    except Exception as e:
        print(f" TEST 2 FALLÓ: {str(e)}")
        return False

def test_sales_report():
    """Test 3: Generar reporte de ventas"""
    print("\n" + "="*60)
    print("TEST 3: Generar reporte de ventas")
    print("="*60)
    
    try:
        service = SaleService()
        
        # Reporte del mes actual
        today = date.today()
        start_date = f"{today.year}-{today.month:02d}-01"
        end_date = str(today)
        
        print(f" Generando reporte: {start_date} - {end_date}")
        report = service.get_sales_report(
            commerce_id=2,
            start_date=start_date,
            end_date=end_date
        )
        
        print(f" Reporte generado:")
        print(f"   Período: {report['period']['start']} - {report['period']['end']}")
        print(f"   Ventas: {report['sales_count']} transacciones")
        print(f"   Total ventas: ₡{report['total_sales']:,.2f}")
        print(f"   Comisión {report['commission_percentage']}%: ₡{report['commission_amount']:,.2f}")
        print(f"   Renta base: ₡{report['base_rent']:,.2f}")
        
        print(" TEST 3 PASADO")
        return True
        
    except Exception as e:
        print(f" TEST 3 FALLÓ: {str(e)}")
        return False

def test_daily_summary():
    """Test 4: Resumen diario de ventas"""
    print("\n" + "="*60)
    print("TEST 4: Resumen diario de ventas")
    print("="*60)
    
    try:
        service = SaleService()
        
        print(" Obteniendo resumen del día...")
        summary = service.get_daily_sales_summary(commerce_id=2)
        
        print(f" Resumen diario:")
        print(f"   Fecha: {summary['date']}")
        print(f"   Ventas hoy: ₡{summary['total_sales_today']:,.2f}")
        print(f"   Transacciones: {summary['transactions_today']}")
        print(f"   Ventas recientes: {len(summary['recent_sales'])}")
        
        print(" TEST 4 PASADO")
        return True
        
    except Exception as e:
        print(f" TEST 4 FALLÓ: {str(e)}")
        return False

def test_validations():
    """Test 5: Validaciones de negocio"""
    print("\n" + "="*60)
    print("TEST 5: Validaciones de negocio")
    print("="*60)
    
    try:
        service = SaleService()
        
        # Test 1: Venta sin items
        print(" Probando venta sin items...")
        try:
            service.process_sale(
                commerce_id=2,
                cashier_user_id=2,
                items=[],
                payment_method_id=1
            )
            print("❌ Debería fallar con items vacíos")
            return False
        except ValueError as e:
            print(f" Validación correcta: {str(e)}")
        
        # Test 2: Commerce ID inválido
        print(" Probando commerce_id inválido...")
        try:
            service.process_sale(
                commerce_id=-1,
                cashier_user_id=2,
                items=[{'product_id': 1, 'quantity': 1, 'unit_price': 1000}],
                payment_method_id=1
            )
            print(" Debería fallar con commerce_id inválido")
            return False
        except ValueError as e:
            print(f" Validación correcta: {str(e)}")
        
        # Test 3: Stock insuficiente
        print(" Probando stock insuficiente...")
        try:
            service.process_sale(
                commerce_id=2,
                cashier_user_id=2,
                items=[{'product_id': 1, 'quantity': 99999, 'unit_price': 1000}],
                payment_method_id=1
            )
            print(" Debería fallar con stock insuficiente")
            return False
        except ValueError as e:
            print(f" Validación correcta: {str(e)}")
        
        print(" TEST 5 PASADO: Todas las validaciones funcionan")
        return True
        
    except Exception as e:
        print(f" TEST 5 FALLÓ: {str(e)}")
        return False

def test_get_sale_details():
    """Test 6: Obtener detalles de venta"""
    print("\n" + "="*60)
    print("TEST 6: Obtener detalles de venta")
    print("="*60)
    
    try:
        service = SaleService()
        
        # Primero crear una venta
        test_items = [
            {'product_id': 1, 'quantity': 1, 'unit_price': 1200.00}
        ]
        
        result = service.process_sale(
            commerce_id=2,
            cashier_user_id=2,
            items=test_items,
            payment_method_id=1
        )
        
        sale_id = result['sale_id']
        
        # Obtener detalles
        print(f" Obteniendo detalles de venta {sale_id}...")
        details = service.get_sale_details(sale_id)
        
        if details:
            print(f" Detalles obtenidos:")
            print(f"   Sale ID: {details['sale_id']}")
            print(f"   Comercio: {details['commerce_name']}")
            print(f"   Total: ₡{details['total_amount']:,.2f}")
            print(f"   Items: {len(details['items'])}")
            print(" TEST 6 PASADO")
            return True
        else:
            print(" No se pudieron obtener detalles")
            return False
        
    except Exception as e:
        print(f" TEST 6 FALLÓ: {str(e)}")
        return False

def main():
    """Ejecutar todos los tests del Sale Service"""
    print(" INICIANDO TESTS DE SALE SERVICE")
    print("=" * 70)
    
    tests = [
        ("Inicialización", test_sale_service_initialization),
        ("Procesar venta", test_process_sale),
        ("Reporte de ventas", test_sales_report),
        ("Resumen diario", test_daily_summary),
        ("Validaciones", test_validations),
        ("Detalles de venta", test_get_sale_details)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f" ERROR INESPERADO en {test_name}: {str(e)}")
    
    # Resumen final
    print("\n" + "="*70)
    print(" RESUMEN DE TESTS - SALE SERVICE")
    print("="*70)
    print(f" Tests pasados: {passed}/{total}")
    print(f" Tests fallidos: {total - passed}/{total}")
    
    if passed == total:
        print("\n ¡TODOS LOS TESTS PASARON!")
        print(" Sale Service está listo para usar")
    else:
        print(f"\n {total - passed} tests fallaron")
        print(" Revisa los errores antes de continuar")
    
    print("="*70)

if __name__ == "__main__":
    main()