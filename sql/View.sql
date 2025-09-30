-- View para el Bussiness Report

USE Caso1;

-- Eliminar VIEW si existe 
DROP VIEW IF EXISTS vw_BusinessReport;

-- Crear VIEW para el reporte
CREATE VIEW vw_BusinessReport AS
SELECT 
    c.name AS business_name,
    b.name AS building_name,
    CONCAT('Local ', mpb.localNumberInBuidling) AS space_name,
    DATE_FORMAT(MIN(s.saleDate), '%Y-%m-%d') AS first_sale_date,
    DATE_FORMAT(MAX(s.saleDate), '%Y-%m-%d') AS last_sale_date,
    COUNT(DISTINCT s.IdSale) AS sales_count,
    SUM(sd.quantitySold) AS items_sold,
    ROUND(SUM(s.totalAmount), 2) AS total_sales,
    cpc.commisionPercentage AS commission_percentage,
    ROUND(SUM(s.totalAmount) * (cpc.commisionPercentage / 100), 2) AS commission_amount,
    cpc.baseMonthlyRent AS rental_fee,
    ROUND(SUM(s.totalAmount) - (SUM(s.totalAmount) * (cpc.commisionPercentage / 100)) - cpc.baseMonthlyRent, 2) AS net_balance
FROM MKCommerces c
INNER JOIN MKSales s ON c.IdCommerce = s.IDCommerceFK2
INNER JOIN MKSalesDetails sd ON s.IdSale = sd.IDSaleFK
INNER JOIN MKContractsPerCommerces cpc ON c.IdCommerce = cpc.IDCommerceFK AND cpc.isCurrent = 1
INNER JOIN MKMercadoPerBuilding mpb ON cpc.IDMercadoPerBuilding = mpb.IdMercadoPerBuilding
INNER JOIN MKBuilding b ON mpb.IDBuildingFK = b.IdBuilding
WHERE MONTH(s.saleDate) = MONTH(CURDATE())
  AND YEAR(s.saleDate) = YEAR(CURDATE())
  AND s.saleStatus = 'COMPLETED'
GROUP BY 
    c.IdCommerce, 
    c.name, 
    b.name, 
    mpb.localNumberInBuidling,
    cpc.commisionPercentage, 
    cpc.baseMonthlyRent
ORDER BY b.name, c.name;

SELECT * FROM vw_BusinessReport;