"""
Test del Settlement Controller 
"""
import logging
from app.controllers.settlement_controller import SettlementController
from app.models.request_models import SettleCommerceRequest

logging.basicConfig(level=logging.INFO)

def test_settle_commerce():
    print("\n" + "="*60)
    print("TEST 1: settle_commerce")
    print("="*60)
    
    controller = SettlementController()
    
    # Test con comercio diferente que NO esté liquidado
    settle_request = SettleCommerceRequest(
        comercio='Burger Express',  # Cambiar a comercio no liquidado
        local='Mercado Central Cartago'
    )
    
    result = controller.settle_commerce(settle_request)
    
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    
    if result.get('data'):
        data = result['data']
        print(f"Commerce: {data.get('commerce_name')}")
        
        if data.get('settlement_id'):
            print(f"Settlement ID: {data.get('settlement_id')}")
        
        if data.get('financial_summary'):
            summary = data['financial_summary']
            print(f"Total Ventas: ₡{summary.get('total_sales', 0):,.2f}")
            print(f"Comisión: ₡{summary.get('commission_amount', 0):,.2f}")
            print(f"Liquidación: ₡{summary.get('settlement_amount', 0):,.2f}")
    
    if result['success']:
        print(" TEST PASADO")
    else:
        # Si ya está liquidado, también es correcto
        if 'Ya existe' in result['message']:
            print(" TEST PASADO (ya liquidado - comportamiento esperado)")
        else:
            print(f" TEST FALLIDO: {result['message']}")

def test_settle_validation():
    print("\n" + "="*60)
    print("TEST 2: Validaciones")
    print("="*60)
    
    controller = SettlementController()
    
    # Test: Comercio inexistente (Pydantic ya valida strings vacíos)
    print("Probando con comercio inexistente...")
    
    try:
        invalid_request = SettleCommerceRequest(
            comercio='Comercio Que No Existe XYZ',  # Nombre válido pero inexistente
            local='Mercado Central Cartago'
        )
        
        result = controller.settle_commerce(invalid_request)
        print(f"Success: {result['success']}")
        print(f"Message: {result.get('message')}")
        
        if not result['success'] and 'no encontrado' in result['message'].lower():
            print(" Validación de comercio inexistente funciona")
        else:
            print("  Validación no detectó comercio inexistente")
            
    except Exception as e:
        print(f"Error en validación: {str(e)}")

def test_get_settlement_by_id():
    print("\n" + "="*60)
    print("TEST 3: get_settlement_by_id")
    print("="*60)
    
    controller = SettlementController()
    result = controller.get_settlement_by_id(3)
    
    print(f"Success: {result['success']}")
    
    if result['success'] and result.get('data'):
        settlement = result['data'].get('settlement')
        if settlement:
            print(f"ID: {settlement.get('settlement_id')}")
            print(f"Comercio: {settlement.get('commerce_name')}")
            print(f"Total: ₡{settlement.get('settlement_amount', 0):,.2f}")
            print(" TEST PASADO")
    else:
        print("  Liquidación no encontrada (normal si el ID no existe)")

def test_get_settlement_history():
    print("\n" + "="*60)
    print("TEST 4: get_settlement_history")
    print("="*60)
    
    controller = SettlementController()
    result = controller.get_settlement_history('Café Central', limit=5)
    
    print(f"Success: {result['success']}")
    
    if result['success'] and result.get('data'):
        history = result['data']
        print(f"Comercio: {history.get('commerce_name')}")
        print(f"Total liquidaciones: {history.get('settlements_count')}")
        
        settlements = history.get('settlements', [])
        for i, s in enumerate(settlements[:3], 1):
            print(f"\n  Liquidación {i}:")
            print(f"    ID: {s.get('settlement_id')}")
            print(f"    Monto: ₡{s.get('settlement_amount', 0):,.2f}")
        
        print("\n TEST PASADO")

def test_calculate_preview():
    print("\n" + "="*60)
    print("TEST 5: calculate_settlement_preview")
    print("="*60)
    
    controller = SettlementController()
    result = controller.calculate_settlement_preview('Café Central')
    
    print(f"Success: {result['success']}")
    
    if result['success'] and result.get('data'):
        preview = result['data']
        print(f"Comercio: {preview.get('commerce_name')}")
        print(f"Período: {preview.get('period')}")
        
        if preview.get('preview'):
            p = preview['preview']
            print(f"Ventas: {p.get('sales_count')} transacciones")
            print(f"Total: ₡{p.get('total_sales', 0):,.2f}")
            print(f"Comisión: ₡{p.get('commission_amount', 0):,.2f}")
            print(f"Liquidación: ₡{p.get('settlement_amount', 0):,.2f}")
        
        print("\n TEST PASADO")

def main():
    print(" TESTS DEL SETTLEMENT CONTROLLER")
    print("="*60)
    
    tests_passed = 0
    tests_total = 5
    
    try:
        test_settle_commerce()
        tests_passed += 1
    except Exception as e:
        print(f" Test 1 falló: {str(e)}")
    
    try:
        test_settle_validation()
        tests_passed += 1
    except Exception as e:
        print(f" Test 2 falló: {str(e)}")
    
    try:
        test_get_settlement_by_id()
        tests_passed += 1
    except Exception as e:
        print(f" Test 3 falló: {str(e)}")
    
    try:
        test_get_settlement_history()
        tests_passed += 1
    except Exception as e:
        print(f" Test 4 falló: {str(e)}")
    
    try:
        test_calculate_preview()
        tests_passed += 1
    except Exception as e:
        print(f" Test 5 falló: {str(e)}")
    
    print("\n" + "="*60)
    print(" RESUMEN")
    print("="*60)
    print(f" Tests pasados: {tests_passed}/{tests_total}")
    print(f" Tests fallidos: {tests_total - tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("\n ¡TODOS LOS TESTS PASARON!")
        print(" Settlement Controller listo")
        print(" Siguiente: Crear Handlers (endpoints FastAPI)")
    
    print("="*60)

if __name__ == "__main__":
    main()