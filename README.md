# Caso #1 BD1
Repositorio del Caso #1 de Bases de Datos I. 

## Profesor
* Rodrigo Nuñez Nuñez 

## Integrantes
* Dylan Gabriel Chacon Berrocal, 
* Christopher Daniel Vargas Villalta, 2024108443

Entidades: 

- Profiles (Chris) - User Roles and Access Control
1. Users (Usuarios del Sistema, tanto los administrados como los owners del negocio)
2. Roles (Roles dentro del sistema)
3. UserRoles (Roles asignados al usuario en especifico)
4. Permissions (Listado de Permisos del sistema)
5. RolePermissions (Permisos que tiene cada rol dentro del sistema)

- Espacio y Comercio (Dylan) - Space and Contract Management
6. Mercado (Nombre del mercado y quien lo administra, puede ser una empresa con varios mercados)
7. Building (Plazas comerciales donde se ubican los mercados)
8. BuildingxMercado (Un mercado tiene varios buildings o una building tiene varios mercados, el local donde esta el mercado)
9. Spaces (Espacios dentro del mercado en donde se ubican los comercios )
10. SpaceAttributes (Atributos del espacio dentro del mercado, tamano, caracteristicas, ubicacion)
11. SpaceTypes (Tipos de espacios esto seria si esta adecuado para tienda de conveniencia, restaurante o mixta)
12. SpaceStatus (Estado del espacio si esta ocupado, disponible, remodelacion etc)
13. Commerces (Comercios dentro del mercado)
14. Commerce Category (Categoria del comercio: restaurante, tienda de conveniencia etc..)
15. CommerceStatus (Si esta activo, remodelandose, etc)

- Localizaciones (Chris) - Space and Contract Management
16. Countries (Paises dentro del sistema)
17. States (Provincias o estado dentro del sistema)
18. Cities (Ciudades dentro de las provincias o estados)
19. Address (Direccion especifica de los lugares)

- Contratos con Comercios y Buildings (Chris) - Space and Contract Management
20. Contracts (Contratos generales)
21. ContractPerCommerce (Contratos por cada comercio Maestro-Detalle)
22. ContractStatus (Estado del contrato si esta vigente o es suspendido)
23. ContractTerms (Terminos de un contrato, un contrato tiene muchos terminos)
24. ContractPerBuilding (Lo voy a quitar)
25. ContractRenewals (Renovaciones de contratos con los comercios)
26. ContractTypes (Tipos de contratos en el sistema)

- Logs (Dylan) - User and Access Control
26. Log (Registros de lo que sucede en el sistema)
27. LogTypes (Tipo de log)
28. Log Sources (Origen del log, login etc)
29. Log Severities (Nivel de importancia del log)

- Inventario y Productos (Dylan) - POS
30. Products (Productos disponibles en el inventario)
31. ProductCategories (Distintas categorias de los productos)
32. ProductBrands (Marcas de los diferentes productos)
34. ProductPrice (Historial de los precios de un producto)
35. Inventory (Inventario que posee cada negocio)
36. InventoryMovements (Movimientos del inventario)
37. Barcodes (Barcode especifico de cada producto)

- Ventas y Facturacion (Chris) - POS
38. Sales (Ventas registradas en el negocio)
39. SalesDetails (Detalle de la venta)
40. Invoices (Factura con validez tributaria en caso de que el cliente lo necesite)
41. InvoiceDetails (Detalles de la factura con validez tributaria)
42. Receipts (Recibos normales o facturas del comercio)
43. SaleDiscounts (Descuentos aplicados a las ventas)

- Finanzas y Contabilidad (Chris) -  Administrator Financial Management
45. InitialInvestments (Tabla para los investements que se realicen para el mercado)
46. OperationalExpenses (Gastos operacionales en el mercado)
47. ExpenseCategories (Categorias de gastos)
48. AccountsReceivable (Lo que debe el comercio)
49. FinancialTransactions (Registro de los pagos recibidos)
50. TransactionTypes (Tipos de Transaccion)
51. CommissionCalculations (Calculo de las comisiones del comercio)
52. CommerceSettlement (Resumen mensual de ventas)
53. CommenrceSettlementDetail (Detalles del resumen mensual de ventas)

- Payments (Dylan)
54. PaymentMethods
55. PaymentConfirmations
56. PaymentReferences
57. SalePayments

- Reports and Analysis (Dylan)
58. TenantMonthlyReports
59. ConsolidatedTenantReports
60. SpaceOccupancyReports
61. FinancialComparativeReports
62. ReportTemplates
63. ReportConfigurations
64. GeneratedReports


