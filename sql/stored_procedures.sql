use Caso1;

-- Stored Procedure: registerSale
-- Proposito: Registrar una venta completa con validaciones

DELIMITER $$

DROP PROCEDURE IF EXISTS registerSale$$

CREATE PROCEDURE registerSale(
    -- Parametros 
    IN p_commerce_id INT,
    IN p_product_name VARCHAR(60),
    IN p_quantity INT,
    IN p_amount_paid DECIMAL(10,2),
    IN p_payment_method VARCHAR(30),
    IN p_payment_confirmation VARCHAR(100),
    IN p_reference_number VARCHAR(60),
    IN p_invoice_number VARCHAR(50),
    IN p_customer_name VARCHAR(100),
    IN p_discount_amount DECIMAL(10,2),
    IN p_cashier_user_id INT,
    
    -- Salidas
    OUT p_sale_id INT,
    OUT p_message VARCHAR(255)
)

proc_label: BEGIN  
    DECLARE v_error INT DEFAULT 0;
    
    -- Handler para errores
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        SET v_error = 1;
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    -- Validación básica: comercio existe
    IF NOT EXISTS(SELECT 1 FROM MKCommerces WHERE IdCommerce = p_commerce_id) THEN
        SET p_message = 'Error: Comercio no existe';
        ROLLBACK;
        LEAVE proc_label;  -- ← CORREGIDO: Usa el label
    END IF;
    
    -- Calcular totales
    SET @subtotal = p_amount_paid / 1.13;
    SET @tax = p_amount_paid - @subtotal;
    
    -- Insertar venta
    INSERT INTO MKSales (
        IDCommerceFK2, saleDate, saleStatus, subTotalAmount,
        discountAmount, taxAmount, totalAmount, paymentStatus,
        invoiceRequired, receiptGenerated, IDPaymentMethodFK,
        IDcashierUserFK, referenceNumber, createdAt, updatedAt, checksum
    ) VALUES (
        p_commerce_id, NOW(), 'COMPLETED', @subtotal,
        p_discount_amount, @tax, p_amount_paid, 'COMPLETED',
        IF(p_customer_name IS NOT NULL, 1, 0), 1, 1,
        p_cashier_user_id, p_reference_number, NOW(), NOW(),
        SHA2(CONCAT(p_commerce_id, NOW()), 256)
    );
    
    SET p_sale_id = LAST_INSERT_ID();
    
    -- Insertar detalle
    INSERT INTO MKSalesDetails (
        IDSaleFK, IDProductFK3, productName, quantitySold,
        unitMeasure, unitPrice, listPrice, costPrice,
        lineTotal, inventoryUpdated, createdAt
    ) VALUES (
        p_sale_id, 1, p_product_name, p_quantity,
        'unidad', p_amount_paid/p_quantity, p_amount_paid/p_quantity,
        (p_amount_paid/p_quantity)*0.5, p_amount_paid, 1, NOW()
    );
    
    -- Log
    INSERT INTO MKLogs (
        description, postTime, computer, username, trace,
        referenceID1, referenceID2, value1, value2, checksum,
        lastUpdate, IDLogSeverityFK, IDLogSourceFK, IDLogTypeFK,
        IDUserFK2, createdAt
    ) VALUES (
        CONCAT('Venta registrada: ', p_sale_id), NOW(), 'SP', 
        CONCAT('user_', p_cashier_user_id), 'registerSale',
        p_sale_id, p_commerce_id, p_reference_number, p_payment_confirmation,
        SHA2(CONCAT('log_', p_sale_id), 256), NOW(), 1, 4, 1,
        p_cashier_user_id, NOW()
    );
    
    IF v_error = 0 THEN
        COMMIT;
        SET p_message = CONCAT('Venta exitosa. ID: ', p_sale_id, ', Total: ₡', p_amount_paid);
    ELSE
        SET p_message = 'Error al registrar venta';
    END IF;
    
END$$

DELIMITER ;

-- Prueba de la stored procedure
CALL registerSale(
    2,                  -- commerce_id (Cafe Central)
    'Café Americano',   -- product_name
    2,                  -- quantity
    2400.00,            -- amount_paid
    'Efectivo',         -- payment_method
    'CONF-123',         -- payment_confirmation
    'REF-001',          -- reference_number
    'INV-001',          -- invoice_number
    'Juan Pérez',       -- customer_name
    0.00,               -- discount_amount
    2,                  -- cashier_user_id
    @sale_id,           -- OUT
    @message            -- OUT
);

SELECT @sale_id, @message;

-- Stored Procedure de SettleCommerce

DELIMITER $$

DROP PROCEDURE IF EXISTS settleCommerce$$

CREATE PROCEDURE settleCommerce(
    -- Parametros 
    IN p_commerce_name VARCHAR(60),
    IN p_location_name VARCHAR(60),
    IN p_user_id INT,
    
    -- Salidas
    OUT p_settlement_id INT,
    OUT p_message VARCHAR(500)
)
proc_label: BEGIN  
    DECLARE v_commerce_id INT;
    DECLARE v_total_sales DECIMAL(10,2);
    DECLARE v_commission DECIMAL(10,2);
    DECLARE v_rent DECIMAL(10,2) DEFAULT 50000;
    DECLARE v_settlement DECIMAL(10,2);
    DECLARE v_error INT DEFAULT 0;
    
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        SET v_error = 1;
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    -- Obtener ID del comercio
    SELECT IdCommerce INTO v_commerce_id
    FROM MKCommerces
    WHERE name = p_commerce_name
    LIMIT 1;
    
    IF v_commerce_id IS NULL THEN
        SET p_message = CONCAT('Error: Comercio "', p_commerce_name, '" no encontrado');
        ROLLBACK;
        LEAVE proc_label;
    END IF;
    
    -- Verificar si ya fue liquidado este mes
    IF EXISTS(
        SELECT 1 FROM MKCommerceSettlement
        WHERE IDCommerceFK6 = v_commerce_id
        AND MONTH(settlementPeriodStart) = MONTH(NOW())
        AND YEAR(settlementPeriodStart) = YEAR(NOW())
    ) THEN
        SET p_message = 'Error: Comercio ya liquidado este mes';
        ROLLBACK;
        LEAVE proc_label;
    END IF;
    
    -- Calcular ventas del mes
    SELECT COALESCE(SUM(totalAmount), 0) INTO v_total_sales
    FROM MKSales
    WHERE IDCommerceFK2 = v_commerce_id
    AND MONTH(saleDate) = MONTH(NOW())
    AND YEAR(saleDate) = YEAR(NOW())
    AND saleStatus = 'COMPLETED';
    
    -- Calcular liquidación
    SET v_commission = v_total_sales * 0.10;  -- 10%
    SET v_settlement = v_commission - v_rent;
    
    -- Crear liquidacion
    INSERT INTO MKCommerceSettlement (
        IDCommerceFK6, totalSalesAmount, settlementPeriodStart,
        settlementPeriodEnd, totalRent, totalCommission,
        totalSettlementAmount, settlementDate, createdAt, UpdatedAt,
        MKContractsPerCommerces_IdContractPerCommerce,
        MKMercadoPerBuilding_IdMercadoPerBuilding
    ) VALUES (
        v_commerce_id, v_total_sales, DATE_FORMAT(NOW(), '%Y-%m-01'),
        LAST_DAY(NOW()), v_rent, v_commission,
        v_settlement, CURDATE(), NOW(), NOW(), 1, 1
    );
    
    SET p_settlement_id = LAST_INSERT_ID();
    
    -- Log
    INSERT INTO MKLogs (
        description, postTime, computer, username, trace,
        referenceID1, referenceID2, value1, value2, checksum,
        lastUpdate, IDLogSeverityFK, IDLogSourceFK, IDLogTypeFK,
        IDUserFK2, createdAt
    ) VALUES (
        CONCAT('Liquidación creada: ', p_settlement_id), NOW(), 'SP',
        CONCAT('user_', p_user_id), 'settleCommerce',
        p_settlement_id, v_commerce_id, 
        CONCAT('Ventas: ', v_total_sales), CONCAT('Settlement: ', v_settlement),
        SHA2(CONCAT('log_', p_settlement_id), 256), NOW(), 1, 4, 2,
        p_user_id, NOW()
    );
    
    IF v_error = 0 THEN
        COMMIT;
        SET p_message = CONCAT(
            'Liquidacion exitosa | Comercio: ', p_commerce_name,
            ' | Ventas: ₡', FORMAT(v_total_sales, 2),
            ' | Comisión: ₡', FORMAT(v_commission, 2),
            ' | Renta: ₡', FORMAT(v_rent, 2),
            ' | Total: ₡', FORMAT(v_settlement, 2),
            ' | ID: ', p_settlement_id
        );
    ELSE
        SET p_message = 'Error al crear liquidacion';
    END IF;
    
END$$

DELIMITER ;

CALL settleCommerce(
    'Café Central',     -- commerce_name
    'Local 101',        -- location_name
    1,                  -- user_id
    @settlement_id,     -- OUT
    @message            -- OUT
);

SELECT @settlement_id, @message;

SELECT * FROM MKCommerceSettlement WHERE IdCommerceSettlement = @settlement_id;