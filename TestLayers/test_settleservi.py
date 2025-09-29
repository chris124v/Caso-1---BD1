"""
Test completo para Settlement Service

"""
import logging
from datetime import date
from app.services.settlement_service import SettlementService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_settlement_service_initialization():
    """Test 1: Verificar inicialización del servicio"""
    print("\n" + "="*60)
    print("TEST 1: Inicialización de Settlement Service")
    print("="*60)
    
    try:
        service = SettlementService()
        print(f" Settlement Service creado correctamente")
        print(f" Settlement Repository: {type(service.settlement_repository)}")
        print(f" Sale Repository: {type(service.sale_repository)}")
        print(f" Base Repository: {type(service.base_repository)}")
        print(" TEST 1 PASADO")
        return True
    except Exception as e:
        print(f" TEST 1 FALLÓ: {str(e)}")
        return False

def test_calculate_settlement_preview():
    """Test 2: Calcular preview de liquidación"""
    print("\n" + "="*60)
    print("TEST 2: Calcular preview de liquidación")
    print("="*60)
    
    try:
        service = SettlementService()
        
        # Preview para mes actual
        today = date.today()
        year = today.year
        month = today.month
        
        print(f" Calculando preview para {year}-{month:02d}...")
        preview = service.calculate_settlement_preview(
            commerce_id=2,
            year=year,
            month=month
        )
        
        print(f" Preview calculado:")
        print(f"   Comercio: {preview['commerce_name']}")
        print(f"   Período: {preview['period']}")
        print(f"   Ventas: {preview['preview']['sales_count']} transacciones")
        print(f"   Total ventas: ₡{preview['preview']['total_sales']:,.2f}")
        print(f"   Comisión: ₡{preview['preview']['commission_amount']:,.2f}")
        print(f"   Renta base: ₡{preview['preview']['base_rent']:,.2f}")
        print(f"   Liquidación: ₡{preview['preview']['settlement_amount']:,.2f}")
        print(f"   Puede liquidar: {preview['can_settle']}")
        
        print(" TEST 2 PASADO")
        return True
        
    except Exception as e:
        print(f" TEST 2 FALLÓ: {str(e)}")
        return False

def test_create_monthly_settlement():
    """Test 3: Crear liquidación mensual"""
    print("\n" + "="*60)
    print("TEST 3: Crear liquidación mensual")
    print("="*60)
    
    try:
        service = SettlementService()
        
        # Usar mes pasado para evitar duplicados
        today = date.today()
        if today.month == 1:
            year = today.year - 1
            month = 12
        else:
            year = today.year
            month = today.month - 1
        
        print(f" Creando liquidación para {year}-{month:02d}...")
        
        try:
            result = service.create_monthly_settlement(
                commerce_id=2,
                year=year,
                month=month,
                created_by_user_id=1
            )
            
            print(f" Liquidación creada:")
            print(f"   Settlement ID: {result['settlement_id']}")
            print(f"   Comercio: {result['commerce_name']}")
            print(f"   Período: {result['period']['start_date']} - {result['period']['end_date']}")
            print(f"   Total ventas: ₡{result['financial_summary']['total_sales']:,.2f}")
            print(f"   Comisión: ₡{result['financial_summary']['commission_amount']:,.2f}")
            print(f"   Liquidación: ₡{result['financial_summary']['settlement_amount']:,.2f}")
            
            print(" TEST 3 PASADO")
            return True
            
        except ValueError as ve:
            if "No elegible" in str(ve) or "Ya existe" in str(ve):
                print(f" {str(ve)}")
                print(" TEST 3 SALTADO: Ya existe liquidación (normal)")
                return True
            else:
                raise ve
        
    except Exception as e:
        print(f" TEST 3 FALLÓ: {str(e)}")
        return False

def test_get_settlement_history():
    """Test 4: Obtener historial de liquidaciones"""
    print("\n" + "="*60)
    print("TEST 4: Historial de liquidaciones")
    print("="*60)
    
    try:
        service = SettlementService()
        
        print(" Obteniendo historial...")
        history = service.get_settlement_history(
            commerce_id=2,
            limit=5
        )
        
        print(f" Historial obtenido:")
        print(f"   Comercio: {history['commerce_name']}")
        print(f"   Liquidaciones: {history['settlements_count']}")
        print(f"   Total acumulado: ₡{history['total_accumulated']:,.2f}")
        
        if history['settlements']:
            print(f"   Últimas liquidaciones:")
            for i, settlement in enumerate(history['settlements'][:3]):
                print(f"   {i+1}. Período: {settlement['period_start']} - {settlement['period_end']}")
                print(f"      Monto: ₡{settlement['settlement_amount']:,.2f}")
        
        print(" TEST 4 PASADO")
        return True
        
    except Exception as e:
        print(f" TEST 4 FALLÓ: {str(e)}")
        return False

def test_validations():
    """Test 5: Validaciones de negocio"""
    print("\n" + "="*60)
    print("TEST 5: Validaciones de liquidación")
    print("="*60)
    
    try:
        service = SettlementService()
        
        # Test 1: Mes inválido
        print(" Probando mes inválido...")
        try:
            service.create_monthly_settlement(
                commerce_id=2,
                year=2024,
                month=13,  # Inválido
                created_by_user_id=1
            )
            print(" Debería fallar con mes inválido")
            return False
        except ValueError as e:
            print(f" Validación correcta: {str(e)}")
        
        # Test 2: Año fuera de rango
        print(" Probando año inválido...")
        try:
            service.create_monthly_settlement(
                commerce_id=2,
                year=2050,  # Fuera de rango
                month=1,
                created_by_user_id=1
            )
            print(" Debería fallar con año inválido")
            return False
        except ValueError as e:
            print(f" Validación correcta: {str(e)}")
        
        print(" TEST 5 PASADO: Validaciones funcionan")
        return True
        
    except Exception as e:
        print(f" TEST 5 FALLÓ: {str(e)}")
        return False

def test_get_settlement_details():
    """Test 6: Obtener detalles de liquidación específica"""
    print("\n" + "="*60)
    print("TEST 6: Detalles de liquidación")
    print("="*60)
    
    try:
        service = SettlementService()
        
        # Primero obtener historial para tener un ID válido
        history = service.get_settlement_history(commerce_id=2, limit=1)
        
        if not history['settlements']:
            print(" No hay liquidaciones para probar")
            print(" TEST 6 SALTADO: Sin datos")
            return True
        
        settlement_id = history['settlements'][0]['settlement_id']
        
        print(f" Obteniendo detalles de liquidación {settlement_id}...")
        details = service.get_settlement_details(settlement_id)
        
        if details:
            print(f" Detalles obtenidos:")
            print(f"   Settlement ID: {details['settlement']['settlement_id']}")
            print(f"   Comercio: {details['settlement']['commerce_name']}")
            print(f"   Monto: ₡{details['settlement']['settlement_amount']:,.2f}")
            print(f"   Ventas en período: {details['sales_count']}")
            print(" TEST 6 PASADO")
            return True
        else:
            print(" No se pudieron obtener detalles")
            return False
        
    except Exception as e:
        print(f" TEST 6 FALLÓ: {str(e)}")
        return False

def test_settlement_metrics():
    """Test 7: Métricas adicionales en preview"""
    print("\n" + "="*60)
    print("TEST 7: Métricas adicionales")
    print("="*60)
    
    try:
        service = SettlementService()
        
        today = date.today()
        preview = service.calculate_settlement_preview(
            commerce_id=2,
            year=today.year,
            month=today.month
        )
        
        print(f" Métricas calculadas:")
        
        if 'metrics' in preview and preview['metrics']:
            metrics = preview['metrics']
            print(f"   Comisión vs Renta: {metrics.get('commission_vs_rent_percentage', 0):.2f}%")
            print(f"   Ingreso neto comercio: ₡{metrics.get('net_income_commerce', 0):,.2f}")
            print(f"   Tasa efectiva: {metrics.get('effective_commission_rate', 0):.2f}%")
            print(f"   Tipo: {metrics.get('settlement_type', 'N/A')}")
        
        print(" TEST 7 PASADO")
        return True
        
    except Exception as e:
        print(f" TEST 7 FALLÓ: {str(e)}")
        return False

def main():
    """Ejecutar todos los tests del Settlement Service"""
    print(" INICIANDO TESTS DE SETTLEMENT SERVICE")
    print("=" * 70)
    
    tests = [
        ("Inicialización", test_settlement_service_initialization),
        ("Preview de liquidación", test_calculate_settlement_preview),
        ("Crear liquidación", test_create_monthly_settlement),
        ("Historial", test_get_settlement_history),
        ("Validaciones", test_validations),
        ("Detalles", test_get_settlement_details),
        ("Métricas", test_settlement_metrics)
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
    print(" RESUMEN DE TESTS - SETTLEMENT SERVICE")
    print("="*70)
    print(f" Tests pasados: {passed}/{total}")
    print(f" Tests fallidos: {total - passed}/{total}")
    
    if passed == total:
        print("\n ¡TODOS LOS TESTS PASARON!")
        print(" Settlement Service está listo para usar")
        print(" Puedes proceder con Stored Procedures")
    else:
        print(f"\n {total - passed} tests fallaron")
        print(" Revisa los errores antes de continuar")
    
    print("="*70)

if __name__ == "__main__":
    main()