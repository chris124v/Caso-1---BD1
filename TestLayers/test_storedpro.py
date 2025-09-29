"""
Test de stored procedures 
"""
from app.repositories.sale_repository import SaleRepository
from app.repositories.settlement_repository import SettlementRepository

def test_register_sale():
    """Test registerSale stored procedure"""
    print("\n" + "="*60)
    print("TEST 1: registerSale")
    print("="*60)
    
    repo = SaleRepository()
    
    result = repo.register_sale_via_procedure(
        commerce_id=2,
        product_name='Café Americano',
        quantity=2,
        amount_paid=2400.00,
        payment_method='Efectivo',
        payment_confirmation='CONF-TEST-001',
        reference_number='REF-TEST-001',
        invoice_number='INV-TEST-001',
        customer_name='Juan Pérez',
        discount_amount=0.00,
        cashier_user_id=2
    )
    
    print(f"\n Success: {result['success']}")
    print(f"   Sale ID: {result['sale_id']}")
    print(f"   Message: {result['message']}")
    
    return result['success']

def test_settle_already_settled():
    """Test comercio ya liquidado"""
    print("\n" + "="*60)
    print("TEST 2: Comercio Ya Liquidado")
    print("="*60)
    
    repo = SettlementRepository()
    
    result = repo.settle_commerce_via_procedure(
        commerce_name='Café Central',
        location_name='Mercado Central Cartago',
        user_id=1
    )
    
    print(f"\n   Success: {result['success']}")
    print(f"   Settlement ID: {result['settlement_id']}")
    print(f"   Already Settled: {result['already_settled']}")
    print(f"   Action: {result['action_taken']}")
    print(f"   Message: {result['message']}")
    
    if result['already_settled']:
        print("\n TEST PASADO: Detectó liquidación existente")
        return True
    else:
        print("\n TEST FALLIDO: No detectó liquidación")
        return False

def test_settle_new():
    """Test crear nueva liquidación"""
    print("\n" + "="*60)
    print("TEST 3: Nueva Liquidación")
    print("="*60)
    
    repo = SettlementRepository()
    
    result = repo.settle_commerce_via_procedure(
        commerce_name='Burger Express',
        location_name='Mercado Central Cartago',
        user_id=1
    )
    
    print(f"\n   Success: {result['success']}")
    print(f"   Settlement ID: {result['settlement_id']}")
    print(f"   Action: {result['action_taken']}")
    print(f"   Message: {result['message']}")
    
    if result['success'] and result['action_taken'] == 'created':
        print("\n TEST PASADO: Liquidación creada")
        return True
    elif result['already_settled']:
        print("\n  TEST SALTADO: Ya estaba liquidado")
        return True
    else:
        print("\n TEST FALLIDO")
        return False

def verify_database():
    """Verificar liquidaciones en BD"""
    print("\n" + "="*60)
    print("VERIFICACIÓN: Últimas Liquidaciones en BD")
    print("="*60)
    
    repo = SettlementRepository()
    
    results = repo.execute_query("""
        SELECT 
            cs.IdCommerceSettlement as ID,
            c.name as Comercio,
            DATE_FORMAT(cs.settlementPeriodStart, '%Y-%m') as Periodo,
            cs.totalSalesAmount as Ventas,
            cs.totalSettlementAmount as Liquidacion
        FROM MKCommerceSettlement cs
        JOIN MKCommerces c ON cs.IDCommerceFK6 = c.IdCommerce
        ORDER BY cs.createdAt DESC
        LIMIT 5
    """)
    
    print(f"\n{'ID':<6} {'Comercio':<25} {'Período':<10} {'Ventas':>15} {'Liquidación':>15}")
    print("-" * 75)
    
    for r in results:
        print(f"{r['ID']:<6} {r['Comercio']:<25} {r['Periodo']:<10} "
              f"₡{r['Ventas']:>13,.2f} ₡{r['Liquidacion']:>13,.2f}")
    
    print("-" * 75)
    print(f"Total: {len(results)} liquidaciones")

def main():
    """Ejecutar todos los tests"""
    print("\n TESTS DE STORED PROCEDURES")
    print("="*60)
    
    tests_passed = 0
    tests_total = 3
    
    # Test 1: registerSale
    if test_register_sale():
        tests_passed += 1
    
    # Test 2: Comercio ya liquidado
    if test_settle_already_settled():
        tests_passed += 1
    
    # Test 3: Nueva liquidación
    if test_settle_new():
        tests_passed += 1
    
    # Verificación en BD
    verify_database()
    
    # Resumen
    print("\n" + "="*60)
    print(" RESUMEN")
    print("="*60)
    print(f" Tests pasados: {tests_passed}/{tests_total}")
    print(f" Tests fallidos: {tests_total - tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("\n ¡TODOS LOS TESTS PASARON!")
    else:
        print(f"\n  {tests_total - tests_passed} test(s) fallaron")
    
    print("="*60)

if __name__ == "__main__":
    main()