"""
Test del Sale Controller con SaleService
"""
import logging
from decimal import Decimal
from app.controllers.sale_controller import SaleController
from app.models.request_models import RegisterSaleRequest

logging.basicConfig(level=logging.INFO)

def test_register_sale():
    print("\n" + "="*60)
    print("TEST 1: register_sale")
    print("="*60)
    
    controller = SaleController()
    
    sale_request = RegisterSaleRequest(
        product_name='Café Americano',
        store_name='Café Central',
        quantity_sold=2,
        amount_paid=Decimal('2400.00'),
        payment_method='Efectivo',
        invoice_number='INV-TEST-001',
        customer='Test Customer'
    )
    
    result = controller.register_sale(sale_request)
    
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    if result['success']:
        print(f"Sale ID: {result.get('sale_id')}")
        print(f"Total: ₡{result.get('total_amount')}")
        print("TEST PASADO")
    else:
        print("TEST FALLIDO")

def test_get_sale_by_id():
    print("\n" + "="*60)
    print("TEST 2: get_sale_by_id")
    print("="*60)
    
    controller = SaleController()
    result = controller.get_sale_by_id(722)
    
    print(f"Success: {result['success']}")
    if result['success']:
        data = result['data']
        print(f"Comercio: {data.get('commerce_name')}")
        print(f"Total: ₡{data.get('total_amount')}")
        print("TEST PASADO")

def test_get_sales_report():
    print("\n" + "="*60)
    print("TEST 3: get_sales_report")
    print("="*60)
    
    controller = SaleController()
    result = controller.get_sales_report('Café Central')
    
    print(f"Success: {result['success']}")
    if result['success']:
        data = result['data']
        print(f"Ventas: {data.get('sales_count')}")
        print(f"Total: ₡{data.get('total_sales'):,.2f}")
        print("TEST PASADO")

def test_get_daily_summary():
    print("\n" + "="*60)
    print("TEST 4: get_daily_summary")
    print("="*60)
    
    controller = SaleController()
    result = controller.get_daily_summary('Café Central')
    
    print(f"Success: {result['success']}")
    if result['success']:
        data = result['data']
        print(f"Fecha: {data.get('date')}")
        print(f"Total hoy: ₡{data.get('total_sales_today'):,.2f}")
        print("TEST PASADO")

def main():
    print("TESTS DEL SALE CONTROLLER")
    print("="*60)
    
    test_register_sale()
    test_get_sale_by_id()
    test_get_sales_report()
    test_get_daily_summary()
    
    print("\nTests completados")

if __name__ == "__main__":
    main()