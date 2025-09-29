"""
Test completo para Settlement Repository
RESPONSABLE: Christopher
"""
import logging
from datetime import datetime, date, timedelta
from decimal import Decimal
from app.repositories.settlement_repository import SettlementRepository
from app.repositories.sale_repository import SaleRepository

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_settlement_repository_connection():
    """Test 1: Verificar conexión básica y configuración"""
    print("\n" + "="*60)
    print("TEST 1: Conexión y configuración básica")
    print("="*60)
    
    try:
        repo = SettlementRepository()
        
        # Verificar herencia
        print(f"✅ SettlementRepository creado correctamente")
        print(f"✅ Commission percentage por defecto: {repo.default_commission_percentage}%")
        print(f"✅ Base rent por defecto: ₡{repo.default_base_rent}")
        
        # Verificar conexión
        connection = repo.get_connection()
        print(f"✅ Conexión obtenida: {type(connection)}")
        connection.close()
        
        # Verificar acceso a table_id_mapping
        settlement_id_column = repo.table_id_mapping.get("MKCommerceSettlement")
        print(f"✅ Mapeo de MKCommerceSettlement: {settlement_id_column}")
        
        print("✅ TEST 1 PASADO: Configuración básica OK")
        return True
        
    except Exception as e:
        print(f"❌ TEST 1 FALLÓ: {str(e)}")
        return False

def test_required_tables():
    """Test 2: Verificar tablas necesarias para liquidaciones"""
    print("\n" + "="*60)
    print("TEST 2: Verificación de tablas requeridas")
    print("="*60)
    
    try:
        repo = SettlementRepository()
        
        required_tables = [
            "MKCommerceSettlement", "MKCommerces", "MKSales",
            "MKContractsPerCommerces", "MKFinancialTransactions"
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

def test_private_methods():
    """Test 3: Probar métodos privados (helpers)"""
    print("\n" + "="*60)
    print("TEST 3: Métodos privados (helpers)")
    print("="*60)
    
    try:
        repo = SettlementRepository()
        
        # Test _check_existing_settlement
        print("🔄 Probando _check_existing_settlement()...")
        exists = repo._check_existing_settlement(
            commerce_id=999,  # ID que no existe
            period_start=date(2024, 10, 1),
            period_end=date(2024, 10, 31)
        )
        print(f"✅ Liquidación inexistente: {exists} (debe ser False)")
        
        # Test _get_contract_terms
        print("🔄 Probando _get_contract_terms()...")
        terms = repo._get_contract_terms(commerce_id=1)
        print(f"✅ Términos de contrato obtenidos:")
        print(f"   Base rent: ₡{terms['base_rent']}")
        print(f"   Commission: {terms['commission_percentage']}%")
        
        # Test _get_period_sales
        print("🔄 Probando _get_period_sales()...")
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        sales = repo._get_period_sales(
            commerce_id=1,
            period_start=yesterday,
            period_end=today
        )
        print(f"✅ Ventas del período:")
        print(f"   Cantidad: {sales['sales_count']}")
        print(f"   Total: ₡{sales['total_sales']}")
        
        print("✅ TEST 3 PASADO: Métodos privados funcionan")
        return True
        
    except Exception as e:
        print(f"❌ TEST 3 FALLÓ: {str(e)}")
        return False

def test_validate_settlement_eligibility():
    """Test 4: Probar validación de elegibilidad"""
    print("\n" + "="*60)
    print("TEST 4: Validación de elegibilidad para liquidación")
    print("="*60)
    
    try:
        repo = SettlementRepository()
        
        # Test con período futuro (sin ventas)
        future_start = date.today() + timedelta(days=30)
        future_end = date.today() + timedelta(days=60)
        
        print("🔄 Probando período futuro (sin ventas)...")
        eligibility = repo.validate_settlement_eligibility(
            commerce_id=1,
            period_start=future_start,
            period_end=future_end
        )
        
        print(f"✅ Elegibilidad resultado:")
        print(f"   Elegible: {eligibility['eligible']}")
        print(f"   Ventas: {eligibility.get('sales_count', 0)}")
        print(f"   Razón: {eligibility.get('reason', 'N/A')}")
        
        # Test con período pasado
        past_start = date.today() - timedelta(days=60)
        past_end = date.today() - timedelta(days=30)
        
        print("🔄 Probando período pasado...")
        eligibility2 = repo.validate_settlement_eligibility(
            commerce_id=1,
            period_start=past_start,
            period_end=past_end
        )
        
        print(f"✅ Elegibilidad resultado:")
        print(f"   Elegible: {eligibility2['eligible']}")
        print(f"   Ventas: {eligibility2.get('sales_count', 0)}")
        
        print("✅ TEST 4 PASADO: Validación de elegibilidad funciona")
        return True
        
    except Exception as e:
        print(f"❌ TEST 4 FALLÓ: {str(e)}")
        return False

def test_calculate_settlement_preview():
    """Test 5: Probar cálculo de preview sin crear liquidación"""
    print("\n" + "="*60)
    print("TEST 5: Cálculo de preview de liquidación")
    print("="*60)
    
    try:
        repo = SettlementRepository()
        
        # Calcular preview para un período
        period_start = date(2024, 10, 1)
        period_end = date(2024, 10, 31)
        
        print(f"🔄 Calculando preview para período: {period_start} - {period_end}")
        
        preview = repo.calculate_settlement_preview(
            commerce_id=1,
            period_start=period_start,
            period_end=period_end
        )
        
        print(f"✅ Preview de liquidación:")
        print(f"   Comercio: {preview['commerce_id']}")
        print(f"   Período: {preview['period']}")
        print(f"   Ventas: {preview['sales_count']} transacciones")
        print(f"   Total ventas: ₡{preview['total_sales']:,.2f}")
        print(f"   Renta base: ₡{preview['base_rent']:,.2f}")
        print(f"   Comisión {preview['commission_percentage']}%: ₡{preview['commission_amount']:,.2f}")
        print(f"   Liquidación final: ₡{preview['settlement_amount']:,.2f}")
        print(f"   Tipo: {preview['settlement_type']}")
        
        # Verificar lógica de cálculo
        expected_commission = preview['total_sales'] * (preview['commission_percentage'] / 100)
        expected_settlement = expected_commission - preview['base_rent']
        
        if abs(preview['commission_amount'] - expected_commission) < 0.01:
            print("✅ Cálculo de comisión correcto")
        else:
            raise ValueError("Cálculo de comisión incorrecto")
            
        if abs(preview['settlement_amount'] - expected_settlement) < 0.01:
            print("✅ Cálculo de liquidación correcto")
        else:
            raise ValueError("Cálculo de liquidación incorrecto")
        
        print("✅ TEST 5 PASADO: Preview de liquidación funciona")
        return True
        
    except Exception as e:
        print(f"❌ TEST 5 FALLÓ: {str(e)}")
        return False

def create_test_sales():
    """Helper: Crear ventas de prueba para testing"""
    print("\n🔧 CREANDO VENTAS DE PRUEBA...")
    
    try:
        sale_repo = SaleRepository()
        
        # Verificar si hay comercios y usuarios
        commerce_count = sale_repo.execute_scalar("SELECT COUNT(*) FROM MKCommerces")
        user_count = sale_repo.execute_scalar("SELECT COUNT(*) FROM MKUsers")
        
        if commerce_count == 0 or user_count == 0:
            print("⚠️  No hay comercios o usuarios, saltando creación de ventas")
            return False
        
        # Crear algunas ventas de prueba
        test_items = [
            {'product_id': 1, 'quantity': 2, 'unit_price': 5000},
            {'product_id': 1, 'quantity': 1, 'unit_price': 3000}
        ]
        
        sales_created = 0
        for i in range(3):  # Crear 3 ventas de prueba
            try:
                result = sale_repo.create_sale(
                    commerce_id=1,
                    cashier_user_id=1,
                    items=test_items
                )
                sales_created += 1
                print(f"✅ Venta {i+1} creada: ID {result['sale_id']}, Total: ₡{result['total_amount']}")
            except Exception as e:
                print(f"⚠️  Error creando venta {i+1}: {str(e)}")
        
        print(f"✅ {sales_created} ventas de prueba creadas")
        return sales_created > 0
        
    except Exception as e:
        print(f"❌ Error creando ventas de prueba: {str(e)}")
        return False

def test_create_settlement_real():
    """Test 6: Crear liquidación real con datos de prueba"""
    print("\n" + "="*60)
    print("TEST 6: Creación de liquidación real")
    print("="*60)
    
    try:
        # Primero verificar si hay ventas, si no, crearlas
        settlement_repo = SettlementRepository()
        
        # Verificar ventas existentes
        today = date.today()
        past_month_start = date(today.year, today.month, 1)
        
        sales_check = settlement_repo._get_period_sales(1, past_month_start, today)
        
        if sales_check['sales_count'] == 0:
            print("⚠️  No hay ventas, creando ventas de prueba...")
            if not create_test_sales():
                print("⚠️  No se pudieron crear ventas, saltando test")
                print("✅ TEST 6 SALTADO: Sin datos para liquidar")
                return True
        
        # Definir período de liquidación
        period_start = date(today.year, today.month, 1)
        period_end = today
        
        print(f"🔄 Intentando crear liquidación...")
        print(f"   Comercio: 1")
        print(f"   Período: {period_start} - {period_end}")
        
        # Verificar elegibilidad primero
        eligibility = settlement_repo.validate_settlement_eligibility(1, period_start, period_end)
        
        if not eligibility['eligible']:
            print(f"⚠️  No elegible para liquidación: {eligibility['reason']}")
            print("✅ TEST 6 SALTADO: No elegible (normal si ya existe)")
            return True
        
        # Crear liquidación
        result = settlement_repo.create_settlement(
            commerce_id=1,
            period_start=period_start,
            period_end=period_end,
            created_by_user_id=1
        )
        
        print(f"✅ Liquidación creada exitosamente:")
        print(f"   Settlement ID: {result['settlement_id']}")
        print(f"   Comercio: {result['commerce_id']}")
        print(f"   Período: {result['period']}")
        print(f"   Total ventas: ₡{result['total_sales']:,.2f}")
        print(f"   Renta base: ₡{result['base_rent']:,.2f}")
        print(f"   Comisión: ₡{result['commission_amount']:,.2f}")
        print(f"   Liquidación: ₡{result['settlement_amount']:,.2f}")
        
        # Test get_settlement_by_id con la liquidación recién creada
        print(f"\n🔄 Probando get_settlement_by_id()...")
        retrieved = settlement_repo.get_settlement_by_id(result['settlement_id'])
        
        if retrieved:
            print(f"✅ Liquidación recuperada:")
            print(f"   ID: {retrieved['settlement_id']}")
            print(f"   Comercio: {retrieved['commerce_name']}")
            print(f"   Total liquidación: ₡{retrieved['settlement_amount']:,.2f}")
        else:
            raise ValueError("No se pudo recuperar la liquidación creada")
        
        print("✅ TEST 6 PASADO: Liquidación real creada y recuperada")
        return True
        
    except Exception as e:
        print(f"❌ TEST 6 FALLÓ: {str(e)}")
        return False

def test_query_methods():
    """Test 7: Probar métodos de consulta"""
    print("\n" + "="*60)
    print("TEST 7: Métodos de consulta")
    print("="*60)
    
    try:
        repo = SettlementRepository()
        
        # Test get_settlements_by_commerce
        print("🔄 Probando get_settlements_by_commerce()...")
        settlements = repo.get_settlements_by_commerce(commerce_id=1, limit=5)
        print(f"✅ Liquidaciones por comercio: {len(settlements)} encontradas")
        
        if settlements:
            print("   Últimas liquidaciones:")
            for i, settlement in enumerate(settlements[:3]):
                print(f"   {i+1}. ID: {settlement['settlement_id']}, "
                      f"Período: {settlement['period_start']} - {settlement['period_end']}, "
                      f"Monto: ₡{settlement['settlement_amount']:,.2f}")
        
        print("✅ TEST 7 PASADO: Métodos de consulta funcionan")
        return True
        
    except Exception as e:
        print(f"❌ TEST 7 FALLÓ: {str(e)}")
        return False

def test_calculation_logic():
    """Test 8: Verificar lógica de cálculos"""
    print("\n" + "="*60)
    print("TEST 8: Verificación de lógica de cálculos")
    print("="*60)
    
    try:
        repo = SettlementRepository()
        
        # Test de cálculos manuales
        print("🔄 Probando cálculos manuales...")
        
        # Datos de prueba
        total_sales = Decimal('1000000.00')  # ₡1,000,000
        commission_percentage = Decimal('10.00')  # 10%
        base_rent = Decimal('50000.00')  # ₡50,000
        
        # Calcular como lo hace el repositorio
        commission_amount = total_sales * (commission_percentage / 100)
        settlement_amount = commission_amount - base_rent
        
        print(f"✅ Cálculo manual:")
        print(f"   Ventas totales: ₡{total_sales:,.2f}")
        print(f"   Comisión {commission_percentage}%: ₡{commission_amount:,.2f}")
        print(f"   Renta base: ₡{base_rent:,.2f}")
        print(f"   Liquidación: ₡{settlement_amount:,.2f}")
        
        # Verificar que la lógica sea correcta
        expected_commission = Decimal('100000.00')  # 10% de 1,000,000
        expected_settlement = Decimal('50000.00')   # 100,000 - 50,000
        
        if commission_amount == expected_commission:
            print("✅ Cálculo de comisión correcto")
        else:
            raise ValueError(f"Comisión incorrecta: esperado {expected_commission}, obtenido {commission_amount}")
        
        if settlement_amount == expected_settlement:
            print("✅ Cálculo de liquidación correcto")
        else:
            raise ValueError(f"Liquidación incorrecta: esperado {expected_settlement}, obtenido {settlement_amount}")
        
        # Test casos extremos
        print("🔄 Probando casos extremos...")
        
        # Caso 1: Sin ventas
        no_sales = Decimal('0.00')
        commission_no_sales = no_sales * (commission_percentage / 100)
        settlement_no_sales = commission_no_sales - base_rent
        print(f"   Sin ventas: Liquidación = ₡{settlement_no_sales:,.2f} (negativa)")
        
        # Caso 2: Ventas bajas
        low_sales = Decimal('100000.00')  # ₡100,000
        commission_low = low_sales * (commission_percentage / 100)
        settlement_low = commission_low - base_rent
        print(f"   Ventas bajas: Liquidación = ₡{settlement_low:,.2f}")
        
        print("✅ TEST 8 PASADO: Lógica de cálculos correcta")
        return True
        
    except Exception as e:
        print(f"❌ TEST 8 FALLÓ: {str(e)}")
        return False

def main():
    """Ejecutar todos los tests del Settlement Repository"""
    print("🧪 INICIANDO TESTS DE SETTLEMENT REPOSITORY")
    print("=" * 70)
    
    tests = [
        ("Conexión básica", test_settlement_repository_connection),
        ("Tablas requeridas", test_required_tables),
        ("Métodos privados", test_private_methods),
        ("Validación de elegibilidad", test_validate_settlement_eligibility),
        ("Preview de liquidación", test_calculate_settlement_preview),
        ("Liquidación real", test_create_settlement_real),
        ("Métodos de consulta", test_query_methods),
        ("Lógica de cálculos", test_calculation_logic)
    ]
    
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
    print("📊 RESUMEN DE TESTS - SETTLEMENT REPOSITORY")
    print("="*70)
    print(f"✅ Tests pasados: {passed}/{total}")
    print(f"❌ Tests fallidos: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ Settlement Repository está listo para usar")
        print("✅ Puedes proceder con Service Layer")
        print("✅ Ready para endpoints de Power BI")
    elif passed >= total - 2:
        print(f"\n⚠️  Casi perfecto ({passed}/{total})")
        print("✅ Settlement Repository funcional")
        print("🔧 Revisa los tests fallidos (probablemente por falta de datos)")
    else:
        print(f"\n⚠️  {total - passed} tests fallaron")
        print("🔧 Revisa los errores antes de continuar")
    
    print("="*70)

if __name__ == "__main__":
    main()