use Caso1;

-- Script llenado de la base de datos

SET SQL_SAFE_UPDATES = 0;

delete from MKPaymentMethods;

ALTER TABLE MKPaymentMethods AUTO_INCREMENT = 1;

SET SQL_SAFE_UPDATES = 1;

-- Usuarios base
INSERT INTO MKUsers (IdUser, name, password, phoneNumber, isActive, createdAt) VALUES
(1, 'Admin Principal', SHA2('admin123', 256), '+506-8888-0000', 1, NOW()),
(2, 'Maria Rodriguez', SHA2('maria123', 256), '+506-8888-0001', 1, NOW()),
(3, 'Carlos Jimenez', SHA2('carlos123', 256), '+506-8888-0002', 1, NOW()),
(4, 'Ana Vargas', SHA2('ana123', 256), '+506-8888-0003', 1, NOW()),
(5, 'Luis Morales', SHA2('luis123', 256), '+506-8888-0004', 1, NOW());

select * from MKUsers;

ALTER TABLE MKUsers AUTO_INCREMENT = 1;

-- Metodos de pago
INSERT INTO MKPaymentMethods (IdPaymentMethod, name, description, createdAt, enabled) VALUES
(1, 'Efectivo', 'Pago en efectivo', NOW(), 1),
(2, 'Tarjeta Débito', 'Pago con tarjeta de débito', NOW(), 1),
(3, 'Tarjeta Crédito', 'Pago con tarjeta de crédito', NOW(), 1),
(4, 'Transferencia', 'Transferencia bancaria', NOW(), 1);

select * from MKPaymentMethods;

-- Paises, Estados y Ciudades
INSERT INTO MKCountries (IdCountry, name, createdAt, updatedAt) VALUES
(1, 'Costa Rica', NOW(), NOW());

select * from MKCountries;

INSERT INTO MKStates (IdState, name, IDCountryFK, createdAt, updatedAt) VALUES
(1, 'Cartago', 1, NOW(), NOW()),
(2, 'San José', 1, NOW(), NOW());

select * from MKStates;

INSERT INTO MKCities (IdCity, name, IDStateFK, createdAt, updatedAt) VALUES
(1, 'Cartago Centro', 1, NOW(), NOW()),
(2, 'San José Centro', 2, NOW(), NOW());

select * from MKCities;

-- Direcciones para los edificios
INSERT INTO MKAddresses (IdAddress, PostalCode, direccion1, direccion2, geolocation, IDCityFK, createdAt, updatedAt) VALUES
(1, '30101', 'Avenida Central', 'Edificio Mercado Central', POINT(-83.9207, 9.8642), 1, NOW(), NOW()),
(2, '10101', 'Calle 5', 'Edificio Plaza Gastronómica', POINT(-84.0817, 9.9344), 2, NOW(), NOW());

select * from MKAddresses;


-- 2. EDIFICIOS

INSERT INTO MKBuilding (IdBuilding, name, IDAddressFK, createdAt, updatedAt) VALUES
(1, 'Mercado Central Cartago', 1, NOW(), NOW()),
(2, 'Plaza Gastronómica San José', 2, NOW(), NOW());

select * from MKBuilding;


-- 3. MERCADOS Y ESPACIOS

-- Mercados (administradores de los edificios)
INSERT INTO MKMercado (IdMercado, name, adminID, createdAt, updatedAt, cedulaJuridica, sociedadAnonima, addressNonFisical) VALUES
(1, 'Mercado Cartaguito', 1, NOW(), NOW(), '3-101-123456', 'Mercados de Cartago S.A.', 'Apartado 1001 Cartago'),
(2, 'Mercado 67', 1, NOW(), NOW(), '3-101-789012', 'Plazas Comerciales S.A.', 'Apartado 2002 San José');

select * from MKMercado;

-- Mercados por edificio
INSERT INTO MKMercadoPerBuilding (IdMercadoPerBuilding, IDMercadoFK, IDBuildingFK, description, deleted, localNumberInBuidling, m2Size) VALUES
(1, 1, 1, 'Local comercial en planta baja grande', 0, 101, 25.50),  -- Edificio 1: 1 espacio
(2, 2, 2, 'Local esquinero con ventanales grande', 0, 201, 30.00),  -- Edificio 2: 2 espacios  
(3, 2, 2, 'Local interior amplio', 0, 202, 28.75);

select * from MKMercadoPerBuilding;

-- Estados y tipos de espacios (estos son los espacios disponibles en el mercado per building)
INSERT INTO MKSpaceStatus (IdSpaceStatus, statusName, description, createdAt) VALUES
(1, 'Disponible', 'Espacio disponible para alquiler', NOW()),
(2, 'Ocupado', 'Espacio actualmente ocupado', NOW()),
(3, 'Mantenimiento', 'Espacio en mantenimiento', NOW());

select * from MKSpaceStatus;

INSERT INTO MKSpaceTypes (IdSpaceType, name, description, createdAt) VALUES
(1, 'Restaurante', 'Espacio para servicio de comidas', NOW()),
(2, 'Cafetería', 'Espacio para bebidas y snacks', NOW()),
(3, 'Tienda', 'Espacio para venta al detalle', NOW());

select * from MKSpaceTypes;

-- Espacios fisicos
INSERT INTO MKSpaces (IdSpace, spaceName, IDSpaceStatusFK, IDSpaceType, number, m2size) VALUES
(1, 'Espacio A-01', 2, 1, 101, 25.50),
(2, 'Espacio B-01', 2, 2, 201, 30.00),
(3, 'Espacio B-02', 2, 3, 202, 28.75);

select * from MKSpaces;

-- 4. Categorias y Estados de Comercios

INSERT INTO MKCommerceCategories (IdCommerceCategory, name, description, createdAt, updatedAt) VALUES
(1, 'Restaurante', 'Servicio completo de comidas', NOW(), NOW()),
(2, 'Cafetería', 'Bebidas y snacks ligeros', NOW(), NOW()),
(3, 'Panadería', 'Productos de panadería y repostería', NOW(), NOW()),
(4, 'Comida Rápida', 'Servicio rápido de comidas', NOW(), NOW()),
(5, 'Jugos Naturales', 'Bebidas naturales y batidos', NOW(), NOW()),
(6, 'Tienda General', 'Productos varios y abarrotes', NOW(), NOW());

select * from MKCommerceCategories;

INSERT INTO MKCommerceStatus (IdCommerceStatus, name, description, createdAt, updatedAt) VALUES
(1, 'Activo', 'Comercio operando normalmente', NOW(), NOW()),
(2, 'Inactivo', 'Comercio temporalmente cerrado', NOW(), NOW()),
(3, 'Suspendido', 'Comercio suspendido por incumplimiento', NOW(), NOW());

select * from MKCommerceStatus;


-- 5. Comercios

-- Espacio 1 (Edificio 1): 5 comercios
INSERT INTO MKCommerces (IdCommerce, name, description, IDCommerceCategoryFK, IDCommerceStatusFK, phoneNumber, emailAddress, schedule, startDate, endDate, isActive, createdAt, updatedAt, IDAddressFK, legalName, legalID) VALUES
(1, 'El Buen Sabor', 'Restaurante de comida típica costarricense', 1, 1, '+506-2222-0001', 'buen.sabor@email.com', 'Lun-Sab 6:00-22:00', '2024-06-01', '2025-05-31', 1, NOW(), NOW(), 1, 'Restaurante El Buen Sabor LTDA', '3-102-111111'),
(2, 'Café Central', 'Cafetería especializada en café gourmet', 2, 1, '+506-2222-0002', 'cafe.central@email.com', 'Lun-Dom 5:00-20:00', '2024-06-01', '2025-05-31', 1, NOW(), NOW(), 1, 'Café Central S.A.', '3-102-222222'),
(3, 'Panadería Doña María', 'Pan fresco y repostería artesanal', 3, 1, '+506-2222-0003', 'dona.maria@email.com', 'Lun-Sab 5:00-19:00', '2024-06-01', '2025-05-31', 1, NOW(), NOW(), 1, 'Panadería Doña María EIRL', '3-102-333333'),
(4, 'Burger Express', 'Hamburguesas y comida rápida', 4, 1, '+506-2222-0004', 'burger.express@email.com', 'Lun-Dom 10:00-23:00', '2024-06-01', '2025-05-31', 1, NOW(), NOW(), 1, 'Burger Express CR LTDA', '3-102-444444'),
(5, 'Jugos Tropicales', 'Jugos naturales y batidos', 5, 1, '+506-2222-0005', 'jugos.tropicales@email.com', 'Lun-Dom 7:00-21:00', '2024-06-01', '2025-05-31', 1, NOW(), NOW(), 1, 'Jugos Tropicales S.A.', '3-102-555555'),

-- Espacio 2 (Edificio 2): 6 comercios
(6, 'Soda La Esquina', 'Comida casera y menús del día', 1, 1, '+506-2233-0001', 'soda.esquina@email.com', 'Lun-Sab 6:00-20:00', '2024-06-15', '2025-06-14', 1, NOW(), NOW(), 2, 'Soda La Esquina EIRL', '3-102-666666'),
(7, 'Café Gourmet Plaza', 'Café de especialidad y postres', 2, 1, '+506-2233-0002', 'cafe.gourmet@email.com', 'Lun-Dom 6:00-22:00', '2024-06-15', '2025-06-14', 1, NOW(), NOW(), 2, 'Café Gourmet Plaza S.A.', '3-102-777777'),
(8, 'Taco Loco', 'Tacos y comida mexicana', 4, 1, '+506-2233-0003', 'taco.loco@email.com', 'Lun-Dom 11:00-23:00', '2024-06-15', '2025-06-14', 1, NOW(), NOW(), 2, 'Taco Loco CR LTDA', '3-102-888888'),
(9, 'Smoothie Bar', 'Batidos y bebidas saludables', 5, 1, '+506-2233-0004', 'smoothie.bar@email.com', 'Lun-Dom 7:00-20:00', '2024-06-15', '2025-06-14', 1, NOW(), NOW(), 2, 'Smoothie Bar S.A.', '3-102-999999'),
(10, 'Pizza Corner', 'Pizzas artesanales y pasta', 1, 1, '+506-2233-0005', 'pizza.corner@email.com', 'Lun-Dom 12:00-23:00', '2024-06-15', '2025-06-14', 1, NOW(), NOW(), 2, 'Pizza Corner LTDA', '3-102-101010'),
(11, 'Mini Market Express', 'Abarrotes y productos básicos', 6, 1, '+506-2233-0006', 'minimarket@email.com', 'Lun-Dom 6:00-22:00', '2024-06-15', '2025-06-14', 1, NOW(), NOW(), 2, 'Mini Market Express EIRL', '3-102-111110'),

-- Espacio 3 (Edificio 2): 4 comercios
(12, 'Comida China Dragón', 'Comida china auténtica', 1, 1, '+506-2244-0001', 'dragon.chino@email.com', 'Lun-Dom 11:00-22:00', '2024-07-01', '2025-06-30', 1, NOW(), NOW(), 2, 'Dragón Dorado S.A.', '3-102-121212'),
(13, 'Helados Artesanales', 'Helados y postres fríos', 2, 1, '+506-2244-0002', 'helados.art@email.com', 'Lun-Dom 10:00-21:00', '2024-07-01', '2025-06-30', 1, NOW(), NOW(), 2, 'Helados Artesanales LTDA', '3-102-131313'),
(14, 'Empanadas del Valle', 'Empanadas y comida rápida', 4, 1, '+506-2244-0003', 'empanadas.valle@email.com', 'Lun-Sab 8:00-20:00', '2024-07-01', '2025-06-30', 1, NOW(), NOW(), 2, 'Empanadas del Valle EIRL', '3-102-141414'),
(15, 'Frutas y Verduras Frescas', 'Productos frescos y naturales', 6, 1, '+506-2244-0004', 'frutas.frescas@email.com', 'Lun-Sab 6:00-18:00', '2024-07-01', '2025-06-30', 1, NOW(), NOW(), 2, 'Frutas Frescas S.A.', '3-102-151515');

select * from MKCommerces;

-- 6. Tipos y Estados de Contratos

INSERT INTO MKContractTypes (IdContractType, name, description, createdAt) VALUES
(1, 'Alquiler Mensual', 'Contrato de alquiler con pago mensual', NOW()),
(2, 'Alquiler + Comisión', 'Contrato con renta base más comisión por ventas', NOW());

select * from MKContractTypes;

INSERT INTO MKContractStatus (IdContractStatus, statusName, description, allowsSales, isActive) VALUES
(1, 'Activo', 'Contrato vigente y operativo', 1, 1),
(2, 'Vencido', 'Contrato vencido pendiente renovación', 0, 0),
(3, 'Suspendido', 'Contrato suspendido por incumplimiento', 0, 1);

select * from MKContractStatus;


-- 7. Contratos para cada comercio

INSERT INTO MKContracts (IdContract, contractNumber, IDContractTypeFK, IDContractStatusFK, startDate, endDate, autoRenewal, renewalDays, createdAt, createdBy, signedDate, lastModified, notes, isActive) VALUES
(1, 2024001, 2, 1, '2024-06-01', '2025-05-31', 1, 30, NOW(), 1, '2024-05-30', CURDATE(), 'Contrato comercio El Buen Sabor', 1),
(2, 2024002, 2, 1, '2024-06-01', '2025-05-31', 1, 30, NOW(), 1, '2024-05-30', CURDATE(), 'Contrato comercio Café Central', 1),
(3, 2024003, 2, 1, '2024-06-01', '2025-05-31', 1, 30, NOW(), 1, '2024-05-30', CURDATE(), 'Contrato comercio Panadería Doña María', 1),
(4, 2024004, 2, 1, '2024-06-01', '2025-05-31', 1, 30, NOW(), 1, '2024-05-30', CURDATE(), 'Contrato comercio Burger Express', 1),
(5, 2024005, 2, 1, '2024-06-01', '2025-05-31', 1, 30, NOW(), 1, '2024-05-30', CURDATE(), 'Contrato comercio Jugos Tropicales', 1),
(6, 2024006, 2, 1, '2024-06-15', '2025-06-14', 1, 30, NOW(), 1, '2024-06-14', CURDATE(), 'Contrato comercio Soda La Esquina', 1),
(7, 2024007, 2, 1, '2024-06-15', '2025-06-14', 1, 30, NOW(), 1, '2024-06-14', CURDATE(), 'Contrato comercio Café Gourmet Plaza', 1),
(8, 2024008, 2, 1, '2024-06-15', '2025-06-14', 1, 30, NOW(), 1, '2024-06-14', CURDATE(), 'Contrato comercio Taco Loco', 1),
(9, 2024009, 2, 1, '2024-06-15', '2025-06-14', 1, 30, NOW(), 1, '2024-06-14', CURDATE(), 'Contrato comercio Smoothie Bar', 1),
(10, 2024010, 2, 1, '2024-06-15', '2025-06-14', 1, 30, NOW(), 1, '2024-06-14', CURDATE(), 'Contrato comercio Pizza Corner', 1),
(11, 2024011, 2, 1, '2024-06-15', '2025-06-14', 1, 30, NOW(), 1, '2024-06-14', CURDATE(), 'Contrato comercio Mini Market Express', 1),
(12, 2024012, 2, 1, '2024-07-01', '2025-06-30', 1, 30, NOW(), 1, '2024-06-30', CURDATE(), 'Contrato comercio Comida China Dragón', 1),
(13, 2024013, 2, 1, '2024-07-01', '2025-06-30', 1, 30, NOW(), 1, '2024-06-30', CURDATE(), 'Contrato comercio Helados Artesanales', 1),
(14, 2024014, 2, 1, '2024-07-01', '2025-06-30', 1, 30, NOW(), 1, '2024-06-30', CURDATE(), 'Contrato comercio Empanadas del Valle', 1),
(15, 2024015, 2, 1, '2024-07-01', '2025-06-30', 1, 30, NOW(), 1, '2024-06-30', CURDATE(), 'Contrato comercio Frutas y Verduras Frescas', 1);

select * from MKContracts;


-- Terminos específicos de cada contrato (renta + comisión)
INSERT INTO MKContractsPerCommerces (IdContractPerCommerce, IDContractFK, IDCommerceFK, IDMercadoPerBuilding, IDSpaceFK, baseMonthlyRent, commisionPercentage, securityDeposit, settlementDay, lateFeePayment, minimunMonthlySales, utilitiesIncluded, isCurrent, createdAt, updatedAt, notes) VALUES
(1, 1, 1, 1, 1, 75000.00, 8.50, 150000.00, '2024-07-05', 25000.00, 500000.00, 1, 1, NOW(), NOW(), 'Contrato El Buen Sabor'),
(2, 2, 2, 1, 1, 50000.00, 10.00, 100000.00, '2024-07-05', 20000.00, 300000.00, 1, 1, NOW(), NOW(), 'Contrato Café Central'),
(3, 3, 3, 1, 1, 60000.00, 7.50, 120000.00, '2024-07-05', 22000.00, 400000.00, 1, 1, NOW(), NOW(), 'Contrato Panadería Doña María'),
(4, 4, 4, 1, 1, 55000.00, 12.00, 110000.00, '2024-07-05', 25000.00, 350000.00, 1, 1, NOW(), NOW(), 'Contrato Burger Express'),
(5, 5, 5, 1, 1, 45000.00, 15.00, 90000.00, '2024-07-05', 18000.00, 250000.00, 1, 1, NOW(), NOW(), 'Contrato Jugos Tropicales'),
(6, 6, 6, 2, 2, 80000.00, 9.00, 160000.00, '2024-07-20', 28000.00, 600000.00, 1, 1, NOW(), NOW(), 'Contrato Soda La Esquina'),
(7, 7, 7, 2, 2, 65000.00, 11.00, 130000.00, '2024-07-20', 24000.00, 450000.00, 1, 1, NOW(), NOW(), 'Contrato Café Gourmet Plaza'),
(8, 8, 8, 2, 2, 70000.00, 10.50, 140000.00, '2024-07-20', 26000.00, 500000.00, 1, 1, NOW(), NOW(), 'Contrato Taco Loco'),
(9, 9, 9, 2, 2, 48000.00, 14.00, 96000.00, '2024-07-20', 20000.00, 280000.00, 1, 1, NOW(), NOW(), 'Contrato Smoothie Bar'),
(10, 10, 10, 2, 2, 85000.00, 8.00, 170000.00, '2024-07-20', 30000.00, 650000.00, 1, 1, NOW(), NOW(), 'Contrato Pizza Corner'),
(11, 11, 11, 2, 2, 40000.00, 5.00, 80000.00, '2024-07-20', 15000.00, 800000.00, 1, 1, NOW(), NOW(), 'Contrato Mini Market Express'),
(12, 12, 12, 3, 3, 72000.00, 9.50, 144000.00, '2024-08-05', 27000.00, 550000.00, 1, 1, NOW(), NOW(), 'Contrato Comida China Dragón'),
(13, 13, 13, 3, 3, 52000.00, 13.00, 104000.00, '2024-08-05', 21000.00, 320000.00, 1, 1, NOW(), NOW(), 'Contrato Helados Artesanales'),
(14, 14, 14, 3, 3, 58000.00, 11.50, 116000.00, '2024-08-05', 23000.00, 380000.00, 1, 1, NOW(), NOW(), 'Contrato Empanadas del Valle'),
(15, 15, 15, 3, 3, 42000.00, 6.00, 84000.00, '2024-08-05', 16000.00, 700000.00, 1, 1, NOW(), NOW(), 'Contrato Frutas y Verduras Frescas');

select * from MKContractsPerCommerces;

-- 8. Categorias y Marcas de Productos

INSERT INTO MKProductCategories (IdProductCategory, name, description, createdAt, unitSystem, updatedAt) VALUES
(1, 'Bebidas', 'Bebidas frías y calientes', NOW(), 'unidad', NOW()),
(2, 'Comidas Principales', 'Platos principales y menús', NOW(), 'unidad', NOW()),
(3, 'Postres', 'Postres y dulces', NOW(), 'unidad', NOW()),
(4, 'Snacks', 'Bocadillos y comida ligera', NOW(), 'unidad', NOW()),
(5, 'Panadería', 'Pan y productos horneados', NOW(), 'unidad', NOW()),
(6, 'Abarrotes', 'Productos básicos y abarrotes', NOW(), 'unidad', NOW());

select * from MKProductCategories;

INSERT INTO MKProductBrand (IdProductBrand, name, description, createdAt, updatedAt) VALUES
(1, 'Casa Especial', 'Productos de la casa', NOW(), NOW()),
(2, 'Coca Cola', 'Bebidas Coca Cola', NOW(), NOW()),
(3, 'Bimbo', 'Productos de panadería', NOW(), NOW()),
(4, 'Dos Pinos', 'Productos lácteos', NOW(), NOW()),
(5, 'Florida', 'Bebidas naturales', NOW(), NOW()),
(6, 'Genérico', 'Productos sin marca específica', NOW(), NOW());

select * from MKProductBrand;

-- 9. Inventarios para 3 comercios especificos

-- Inventarios para Café Central (ID: 2), Burger Express (ID: 4), y Pizza Corner (ID: 10)
INSERT INTO MKInventory (IdInventory, IDCommerceFK, name, description, stockComplete, createdAt, updatedAt, IDMercadoPerBuilding) VALUES
(1, 2, 'Inventario Café Central', 'Bebidas y snacks', 100, NOW(), NOW(), 1),
(2, 4, 'Inventario Burger Express', 'Hamburguesas y comida rápida', 100, NOW(), NOW(), 1),
(3, 10, 'Inventario Pizza Corner', 'Pizzas y pasta', 100, NOW(), NOW(), 2);

select * from MKInventory;


-- 10. Productos con demanda alta

-- Productos para Café Central (Bebidas)
INSERT INTO MKProducts (IdProduct, IDProductCategory, IDProductBrand, name, description, status, quantity, expires, expirationDate, deleted, enabled, IDInventoryFK, IDMercadoPerBuilding) VALUES
(1, 1, 1, 'Café Americano', 'Café negro tradicional', 'AVAILABLE', 500, 0, '2030-12-31', 0, 1, 1, 1),
(2, 1, 1, 'Café con Leche', 'Café con leche fresca', 'AVAILABLE', 500, 0, '2030-12-31', 0, 1, 1, 1),
(3, 1, 1, 'Cappuccino', 'Café espresso con espuma de leche', 'AVAILABLE', 300, 0, '2030-12-31', 0, 1, 1, 1),
(4, 1, 2, 'Coca Cola', 'Refresco de cola 350ml', 'AVAILABLE', 200, 1, '2025-12-31', 0, 1, 1, 1),
(5, 3, 1, 'Queque de Chocolate', 'Porción de queque casero', 'AVAILABLE', 100, 1, '2024-12-31', 0, 1, 1, 1),
(6, 4, 1, 'Emparedado Mixto', 'Jamón y queso', 'AVAILABLE', 150, 1, '2024-12-31', 0, 1, 1, 1),

-- Productos para Burger Express (Comida rápida)
(7, 2, 1, 'Hamburguesa Clásica', 'Carne, lechuga, tomate, queso', 'AVAILABLE', 300, 0, '2030-12-31', 0, 1, 2, 1),
(8, 2, 1, 'Hamburguesa Doble', 'Doble carne con todos los vegetales', 'AVAILABLE', 200, 0, '2030-12-31', 0, 1, 2, 1),
(9, 4, 1, 'Papas Fritas', 'Porción mediana de papas', 'AVAILABLE', 400, 0, '2030-12-31', 0, 1, 2, 1),
(10, 1, 2, 'Refresco 500ml', 'Bebida gaseosa surtida', 'AVAILABLE', 250, 1, '2025-12-31', 0, 1, 2, 1),
(11, 2, 1, 'Chicken Nuggets', '6 piezas de pollo empanizado', 'AVAILABLE', 180, 0, '2030-12-31', 0, 1, 2, 1),
(12, 4, 1, 'Aros de Cebolla', 'Porción de aros de cebolla', 'AVAILABLE', 120, 0, '2030-12-31', 0, 1, 2, 1),

-- Productos para Pizza Corner (Pizza y pasta)
(13, 2, 1, 'Pizza Margarita', 'Pizza con tomate, mozzarella y albahaca', 'AVAILABLE', 150, 0, '2030-12-31', 0, 1, 3, 2),
(14, 2, 1, 'Pizza Pepperoni', 'Pizza con pepperoni y queso', 'AVAILABLE', 150, 0, '2030-12-31', 0, 1, 3, 2),
(15, 2, 1, 'Pizza Hawaiana', 'Pizza con jamón y piña', 'AVAILABLE', 120, 0, '2030-12-31', 0, 1, 3, 2),
(16, 2, 1, 'Pasta Bolognesa', 'Pasta con salsa de carne', 'AVAILABLE', 100, 0, '2030-12-31', 0, 1, 3, 2),
(17, 2, 1, 'Pasta Alfredo', 'Pasta con salsa blanca', 'AVAILABLE', 100, 0, '2030-12-31', 0, 1, 3, 2),
(18, 1, 2, 'Limonada Natural', 'Bebida de limón natural 400ml', 'AVAILABLE', 180, 1, '2025-12-31', 0, 1, 3, 2);

select * from MKProducts;

-- 11. Precios de Productos

INSERT INTO MKProductsPerMercadoPerBuilding (IdProductsInMercadoBuilding, IDProductFK, IDMercadoPerBuildingFK, createdAt, updatedAt) VALUES
(1, 1, 1, NOW(), NOW()), (2, 2, 1, NOW(), NOW()), (3, 3, 1, NOW(), NOW()),
(4, 4, 1, NOW(), NOW()), (5, 5, 1, NOW(), NOW()), (6, 6, 1, NOW(), NOW()),
(7, 7, 1, NOW(), NOW()), (8, 8, 1, NOW(), NOW()), (9, 9, 1, NOW(), NOW()),
(10, 10, 1, NOW(), NOW()), (11, 11, 1, NOW(), NOW()), (12, 12, 1, NOW(), NOW()),
(13, 13, 2, NOW(), NOW()), (14, 14, 2, NOW(), NOW()), (15, 15, 2, NOW(), NOW()),
(16, 16, 2, NOW(), NOW()), (17, 17, 2, NOW(), NOW()), (18, 18, 2, NOW(), NOW());

select * from MKProductsPerMercadoPerBuilding;

INSERT INTO MKProductPrices (IdProductPrices, price, startDate, endDate, createdAt, updatedAt, IDProductsInMercadoBuilding) VALUES
-- Precios Café Central
(1, 1200.00, '2024-06-01', '2025-05-31', NOW(), NOW(), 1),  -- Café Americano
(2, 1500.00, '2024-06-01', '2025-05-31', NOW(), NOW(), 2),  -- Café con Leche
(3, 2200.00, '2024-06-01', '2025-05-31', NOW(), NOW(), 3),  -- Cappuccino
(4, 800.00, '2024-06-01', '2025-05-31', NOW(), NOW(), 4),   -- Coca Cola
(5, 1800.00, '2024-06-01', '2025-05-31', NOW(), NOW(), 5),  -- Queque Chocolate
(6, 2500.00, '2024-06-01', '2025-05-31', NOW(), NOW(), 6),  -- Emparedado Mixto

-- Precios Burger Express
(7, 3500.00, '2024-06-01', '2025-05-31', NOW(), NOW(), 7),  -- Hamburguesa Clásica
(8, 4500.00, '2024-06-01', '2025-05-31', NOW(), NOW(), 8),  -- Hamburguesa Doble
(9, 1800.00, '2024-06-01', '2025-05-31', NOW(), NOW(), 9),  -- Papas Fritas
(10, 1000.00, '2024-06-01', '2025-05-31', NOW(), NOW(), 10), -- Refresco 500ml
(11, 2800.00, '2024-06-01', '2025-05-31', NOW(), NOW(), 11), -- Chicken Nuggets
(12, 2200.00, '2024-06-01', '2025-05-31', NOW(), NOW(), 12), -- Aros de Cebolla

-- Precios Pizza Corner
(13, 5500.00, '2024-06-15', '2025-06-14', NOW(), NOW(), 13), -- Pizza Margarita
(14, 6200.00, '2024-06-15', '2025-06-14', NOW(), NOW(), 14), -- Pizza Pepperoni
(15, 6800.00, '2024-06-15', '2025-06-14', NOW(), NOW(), 15), -- Pizza Hawaiana
(16, 4200.00, '2024-06-15', '2025-06-14', NOW(), NOW(), 16), -- Pasta Bolognesa
(17, 4500.00, '2024-06-15', '2025-06-14', NOW(), NOW(), 17), -- Pasta Alfredo
(18, 1200.00, '2024-06-15', '2025-06-14', NOW(), NOW(), 18); -- Limonada Natural

select * from MKProductPrices;

-- 12. Ventas historicas 4 meses

-- Configuracion de transacciones y tipos de entidades para liquidaciones
INSERT INTO MKTransactionTypes (IdTransactionType, typeName, typeDescription, transactionFlow, isActive) VALUES
(1, 'Ingreso por Comisión', 'Comisión recibida de comercios', 'INCOME', 1),
(2, 'Pago Renta Base', 'Pago de renta base mensual', 'INCOME', 1),
(3, 'Gasto Operativo', 'Gastos operativos del mercado', 'EXPENSE', 1);

select * from MKTransactionTypes;

INSERT INTO MKRelatedEntityType (idRelatedEntityType, nameEntity, description, createdAt, updatedAt) VALUES
(1, 'Comercio', 'Entidad relacionada con comercios', NOW(), NOW()),
(2, 'Liquidación', 'Entidad relacionada con liquidaciones', NOW(), NOW());

select * from MKRelatedEntityType;

INSERT INTO MKTransactionSubTypes (IdTransactionSubTypes, name, description, createdAt, updatedAt) VALUES
(1, 'Liquidación Mensual', 'Liquidación mensual de comercio', NOW(), NOW()),
(2, 'Pago Regular', 'Pago regular de servicios', NOW(), NOW());

select * from MKTransactionSubTypes;

-- Variables para controlar la generación de ventas
SET @sale_id = 1;
SET @detail_id = 1;
SET @start_date = DATE_SUB(CURDATE(), INTERVAL 4 MONTH);
SET @current_date = @start_date;

-- VENTAS MASIVAS PARA CAFÉ CENTRAL (Comercio ID: 2)

SET SQL_SAFE_UPDATES = 0;

delete from MKSales;

ALTER TABLE MKSales AUTO_INCREMENT = 1;

SET SQL_SAFE_UPDATES = 1;


-- Limpiar ventas previas para regenerar
DELETE FROM MKSalesDetails WHERE IDSaleFK IN (SELECT IdSale FROM MKSales WHERE IDCommerceFK2 IN (2, 4, 10));
DELETE FROM MKSales WHERE IDCommerceFK2 IN (2, 4, 10);
DELETE FROM MKInventoryMovements WHERE IDProduct IN (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18);

-- Resetear inventarios a niveles altos
UPDATE MKProducts SET quantity = 1000 WHERE IdProduct IN (1,2,3,4,5,6);    -- Café Central
UPDATE MKProducts SET quantity = 800 WHERE IdProduct IN (7,8,9,10,11,12);  -- Burger Express  
UPDATE MKProducts SET quantity = 600 WHERE IdProduct IN (13,14,15,16,17,18); -- Pizza Corner

-- Procedimientos para generar ventas aleatorias

DELIMITER $$

DROP PROCEDURE IF EXISTS GenerateRandomSales$$

CREATE PROCEDURE GenerateRandomSales()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE commerce_id INT;
    DECLARE commerce_name VARCHAR(100);
    DECLARE month_start DATE;
    DECLARE month_end DATE;
    DECLARE sales_target INT;
    DECLARE sales_created INT;
    DECLARE current_sale_id INT DEFAULT 1;
    DECLARE current_detail_id INT DEFAULT 1;
    
    -- Variables para venta individual
    DECLARE sale_date DATETIME;
    DECLARE sale_day INT;
    DECLARE sale_hour INT;
    DECLARE sale_minute INT;
    DECLARE product_count INT;
    DECLARE i INT;
    DECLARE random_product_id INT;
    DECLARE random_quantity INT;
    DECLARE product_price DECIMAL(10,2);
    DECLARE current_stock INT;
    DECLARE subtotal DECIMAL(10,2);
    DECLARE tax_amount DECIMAL(10,2);
    DECLARE total_amount DECIMAL(10,2);
    DECLARE reference_number VARCHAR(60);
    DECLARE payment_method INT;
    DECLARE line_total DECIMAL(10,2);
    
    -- Arrays de productos por comercio
    DECLARE cafe_products VARCHAR(20) DEFAULT '1,2,3,4,5,6';
    DECLARE burger_products VARCHAR(20) DEFAULT '7,8,9,10,11,12'; 
    DECLARE pizza_products VARCHAR(20) DEFAULT '13,14,15,16,17,18';
    
    DECLARE comercios CURSOR FOR 
        SELECT IdCommerce, name 
        FROM MKCommerces 
        WHERE IdCommerce IN (2, 4, 10) 
        AND isActive = 1;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- =====================================================
    -- GENERAR VENTAS PARA CADA COMERCIO Y CADA MES
    -- =====================================================
    
    OPEN comercios;
    
    comercio_loop: LOOP
        FETCH comercios INTO commerce_id, commerce_name;
        IF done THEN
            LEAVE comercio_loop;
        END IF;
        
        -- =====================================================
        -- MES 1: JUNIO 2024
        -- =====================================================
        SET month_start = '2024-06-01';
        SET month_end = '2024-06-30';
        SET sales_target = 50 + FLOOR(RAND() * 21); -- Random entre 50-70
        SET sales_created = 0;
        
        WHILE sales_created < sales_target DO
            -- Generar fecha aleatoria en el mes
            SET sale_day = 1 + FLOOR(RAND() * 30);
            SET sale_hour = 7 + FLOOR(RAND() * 14); -- 7 AM a 9 PM
            SET sale_minute = FLOOR(RAND() * 60);
            SET sale_date = DATE_ADD(month_start, INTERVAL sale_day - 1 DAY);
            SET sale_date = DATE_ADD(sale_date, INTERVAL sale_hour HOUR);
            SET sale_date = DATE_ADD(sale_date, INTERVAL sale_minute MINUTE);
            
            -- Generar número de referencia único
            SET reference_number = CONCAT('VTA-', LPAD(commerce_id, 4, '0'), '-', LPAD(current_sale_id, 6, '0'), '-', DATE_FORMAT(sale_date, '%Y%m%d%H%i%s'));
            
            -- Método de pago aleatorio
            SET payment_method = 1 + FLOOR(RAND() * 4);
            
            -- Generar productos para esta venta (1-4 productos por venta)
            SET product_count = 1 + FLOOR(RAND() * 4);
            SET subtotal = 0;
            SET i = 0;
            
            -- Insertar venta principal (placeholder)
            INSERT INTO MKSales (
                IdSale, IDCommerceFK2, saleDate, saleStatus, subTotalAmount,
                discountAmount, taxAmount, totalAmount, paymentStatus,
                invoiceRequired, receiptGenerated, IDPaymentMethodFK,
                IDcashierUserFK, referenceNumber, createdAt, updatedAt, checksum
            ) VALUES (
                current_sale_id, commerce_id, sale_date, 'COMPLETED', 0,
                0, 0, 0, 'COMPLETED', 0, 1, payment_method,
                2, reference_number, NOW(), NOW(), SHA2(CONCAT('sale_', current_sale_id), 256)
            );
            
            -- Generar detalles de productos
            WHILE i < product_count DO
                -- Seleccionar producto aleatorio según comercio
                IF commerce_id = 2 THEN -- Café Central
                    SET random_product_id = 1 + FLOOR(RAND() * 6); -- Productos 1-6
                ELSEIF commerce_id = 4 THEN -- Burger Express
                    SET random_product_id = 7 + FLOOR(RAND() * 6); -- Productos 7-12
                ELSEIF commerce_id = 10 THEN -- Pizza Corner
                    SET random_product_id = 13 + FLOOR(RAND() * 6); -- Productos 13-18
                END IF;
                
                -- Verificar stock disponible
                SELECT quantity INTO current_stock 
                FROM MKProducts 
                WHERE IdProduct = random_product_id;
                
                -- Solo continuar si hay stock
                IF current_stock > 0 THEN
                    -- Cantidad aleatoria (1-3, pero sin exceder stock)
                    SET random_quantity = 1 + FLOOR(RAND() * 3);
                    IF random_quantity > current_stock THEN
                        SET random_quantity = current_stock;
                    END IF;
                    
                    -- Obtener precio del producto
                    SELECT pp.price INTO product_price
                    FROM MKProductPrices pp
                    INNER JOIN MKProductsPerMercadoPerBuilding pmpb ON pp.IDProductsInMercadoBuilding = pmpb.IdProductsInMercadoBuilding
                    WHERE pmpb.IDProductFK = random_product_id
                    LIMIT 1;
                    
                    SET line_total = product_price * random_quantity;
                    SET subtotal = subtotal + line_total;
                    
                    -- Insertar detalle de venta
                    INSERT INTO MKSalesDetails (
                        IdSaleDetails, IDSaleFK, IDProductFK3, productName,
                        quantitySold, unitMeasure, unitPrice, listPrice,
                        costPrice, lineTotal, inventoryUpdated, createdAt
                    ) VALUES (
                        current_detail_id, current_sale_id, random_product_id, 
                        (SELECT name FROM MKProducts WHERE IdProduct = random_product_id),
                        random_quantity, 'unidad', product_price, product_price,
                        product_price * 0.5, line_total, 1, NOW()
                    );
                    
                    -- Actualizar inventario
                    UPDATE MKProducts 
                    SET quantity = quantity - random_quantity 
                    WHERE IdProduct = random_product_id;
                    
                    -- Registrar movimiento de inventario
                    INSERT INTO MKInventoryMovements (
                        IdInventoryMovement, movementType, quantity, movementDate,
                        notes, createdAt, updatedAt, IDProduct, userId, computer
                    ) VALUES (
                        current_detail_id, 'EXIT', random_quantity, sale_date,
                        CONCAT('Venta ID: ', current_sale_id), NOW(), NOW(),
                        random_product_id, '2', 'SYSTEM'
                    );
                    
                    SET current_detail_id = current_detail_id + 1;
                END IF;
                
                SET i = i + 1;
            END WHILE;
            
            -- Calcular totales finales
            SET tax_amount = subtotal * 0.13;
            SET total_amount = subtotal + tax_amount;
            
            -- Actualizar venta con totales correctos
            UPDATE MKSales 
            SET subTotalAmount = subtotal,
                taxAmount = tax_amount,
                totalAmount = total_amount,
                updatedAt = NOW()
            WHERE IdSale = current_sale_id;
            
            SET current_sale_id = current_sale_id + 1;
            SET sales_created = sales_created + 1;
        END WHILE;
        
        -- =====================================================
        -- MES 2: JULIO 2024
        -- =====================================================
        SET month_start = '2024-07-01';
        SET month_end = '2024-07-31';
        SET sales_target = 50 + FLOOR(RAND() * 21);
        SET sales_created = 0;
        
        WHILE sales_created < sales_target DO
            -- (Repetir misma lógica para julio)
            SET sale_day = 1 + FLOOR(RAND() * 31);
            SET sale_hour = 7 + FLOOR(RAND() * 14);
            SET sale_minute = FLOOR(RAND() * 60);
            SET sale_date = DATE_ADD(month_start, INTERVAL sale_day - 1 DAY);
            SET sale_date = DATE_ADD(sale_date, INTERVAL sale_hour HOUR);
            SET sale_date = DATE_ADD(sale_date, INTERVAL sale_minute MINUTE);
            
            SET reference_number = CONCAT('VTA-', LPAD(commerce_id, 4, '0'), '-', LPAD(current_sale_id, 6, '0'), '-', DATE_FORMAT(sale_date, '%Y%m%d%H%i%s'));
            SET payment_method = 1 + FLOOR(RAND() * 4);
            SET product_count = 1 + FLOOR(RAND() * 4);
            SET subtotal = 0;
            SET i = 0;
            
            INSERT INTO MKSales (
                IdSale, IDCommerceFK2, saleDate, saleStatus, subTotalAmount,
                discountAmount, taxAmount, totalAmount, paymentStatus,
                invoiceRequired, receiptGenerated, IDPaymentMethodFK,
                IDcashierUserFK, referenceNumber, createdAt, updatedAt, checksum
            ) VALUES (
                current_sale_id, commerce_id, sale_date, 'COMPLETED', 0,
                0, 0, 0, 'COMPLETED', 0, 1, payment_method,
                2, reference_number, NOW(), NOW(), SHA2(CONCAT('sale_', current_sale_id), 256)
            );
            
            WHILE i < product_count DO
                IF commerce_id = 2 THEN
                    SET random_product_id = 1 + FLOOR(RAND() * 6);
                ELSEIF commerce_id = 4 THEN
                    SET random_product_id = 7 + FLOOR(RAND() * 6);
                ELSEIF commerce_id = 10 THEN
                    SET random_product_id = 13 + FLOOR(RAND() * 6);
                END IF;
                
                SELECT quantity INTO current_stock FROM MKProducts WHERE IdProduct = random_product_id;
                
                IF current_stock > 0 THEN
                    SET random_quantity = 1 + FLOOR(RAND() * 3);
                    IF random_quantity > current_stock THEN
                        SET random_quantity = current_stock;
                    END IF;
                    
                    SELECT pp.price INTO product_price
                    FROM MKProductPrices pp
                    INNER JOIN MKProductsPerMercadoPerBuilding pmpb ON pp.IDProductsInMercadoBuilding = pmpb.IdProductsInMercadoBuilding
                    WHERE pmpb.IDProductFK = random_product_id LIMIT 1;
                    
                    SET line_total = product_price * random_quantity;
                    SET subtotal = subtotal + line_total;
                    
                    INSERT INTO MKSalesDetails (
                        IdSaleDetails, IDSaleFK, IDProductFK3, productName,
                        quantitySold, unitMeasure, unitPrice, listPrice,
                        costPrice, lineTotal, inventoryUpdated, createdAt
                    ) VALUES (
                        current_detail_id, current_sale_id, random_product_id, 
                        (SELECT name FROM MKProducts WHERE IdProduct = random_product_id),
                        random_quantity, 'unidad', product_price, product_price,
                        product_price * 0.5, line_total, 1, NOW()
                    );
                    
                    UPDATE MKProducts SET quantity = quantity - random_quantity WHERE IdProduct = random_product_id;
                    
                    INSERT INTO MKInventoryMovements (
                        IdInventoryMovement, movementType, quantity, movementDate,
                        notes, createdAt, updatedAt, IDProduct, userId, computer
                    ) VALUES (
                        current_detail_id, 'EXIT', random_quantity, sale_date,
                        CONCAT('Venta ID: ', current_sale_id), NOW(), NOW(),
                        random_product_id, '2', 'SYSTEM'
                    );
                    
                    SET current_detail_id = current_detail_id + 1;
                END IF;
                SET i = i + 1;
            END WHILE;
            
            SET tax_amount = subtotal * 0.13;
            SET total_amount = subtotal + tax_amount;
            
            UPDATE MKSales 
            SET subTotalAmount = subtotal, taxAmount = tax_amount, totalAmount = total_amount, updatedAt = NOW()
            WHERE IdSale = current_sale_id;
            
            SET current_sale_id = current_sale_id + 1;
            SET sales_created = sales_created + 1;
        END WHILE;
        
        -- =====================================================
        -- MES 3: AGOSTO 2024 (Repetir lógica)
        -- =====================================================
        SET month_start = '2024-08-01';
        SET month_end = '2024-08-31';
        SET sales_target = 50 + FLOOR(RAND() * 21);
        SET sales_created = 0;
        
        WHILE sales_created < sales_target DO
            SET sale_day = 1 + FLOOR(RAND() * 31);
            SET sale_hour = 7 + FLOOR(RAND() * 14);
            SET sale_minute = FLOOR(RAND() * 60);
            SET sale_date = DATE_ADD(month_start, INTERVAL sale_day - 1 DAY);
            SET sale_date = DATE_ADD(sale_date, INTERVAL sale_hour HOUR);
            SET sale_date = DATE_ADD(sale_date, INTERVAL sale_minute MINUTE);
            
            SET reference_number = CONCAT('VTA-', LPAD(commerce_id, 4, '0'), '-', LPAD(current_sale_id, 6, '0'), '-', DATE_FORMAT(sale_date, '%Y%m%d%H%i%s'));
            SET payment_method = 1 + FLOOR(RAND() * 4);
            SET product_count = 1 + FLOOR(RAND() * 4);
            SET subtotal = 0;
            SET i = 0;
            
            INSERT INTO MKSales (
                IdSale, IDCommerceFK2, saleDate, saleStatus, subTotalAmount,
                discountAmount, taxAmount, totalAmount, paymentStatus,
                invoiceRequired, receiptGenerated, IDPaymentMethodFK,
                IDcashierUserFK, referenceNumber, createdAt, updatedAt, checksum
            ) VALUES (
                current_sale_id, commerce_id, sale_date, 'COMPLETED', 0,
                0, 0, 0, 'COMPLETED', 0, 1, payment_method,
                2, reference_number, NOW(), NOW(), SHA2(CONCAT('sale_', current_sale_id), 256)
            );
            
            WHILE i < product_count DO
                IF commerce_id = 2 THEN
                    SET random_product_id = 1 + FLOOR(RAND() * 6);
                ELSEIF commerce_id = 4 THEN
                    SET random_product_id = 7 + FLOOR(RAND() * 6);
                ELSEIF commerce_id = 10 THEN
                    SET random_product_id = 13 + FLOOR(RAND() * 6);
                END IF;
                
                SELECT quantity INTO current_stock FROM MKProducts WHERE IdProduct = random_product_id;
                
                IF current_stock > 0 THEN
                    SET random_quantity = 1 + FLOOR(RAND() * 3);
                    IF random_quantity > current_stock THEN
                        SET random_quantity = current_stock;
                    END IF;
                    
                    SELECT pp.price INTO product_price
                    FROM MKProductPrices pp
                    INNER JOIN MKProductsPerMercadoPerBuilding pmpb ON pp.IDProductsInMercadoBuilding = pmpb.IdProductsInMercadoBuilding
                    WHERE pmpb.IDProductFK = random_product_id LIMIT 1;
                    
                    SET line_total = product_price * random_quantity;
                    SET subtotal = subtotal + line_total;
                    
                    INSERT INTO MKSalesDetails (
                        IdSaleDetails, IDSaleFK, IDProductFK3, productName,
                        quantitySold, unitMeasure, unitPrice, listPrice,
                        costPrice, lineTotal, inventoryUpdated, createdAt
                    ) VALUES (
                        current_detail_id, current_sale_id, random_product_id, 
                        (SELECT name FROM MKProducts WHERE IdProduct = random_product_id),
                        random_quantity, 'unidad', product_price, product_price,
                        product_price * 0.5, line_total, 1, NOW()
                    );
                    
                    UPDATE MKProducts SET quantity = quantity - random_quantity WHERE IdProduct = random_product_id;
                    
                    INSERT INTO MKInventoryMovements (
                        IdInventoryMovement, movementType, quantity, movementDate,
                        notes, createdAt, updatedAt, IDProduct, userId, computer
                    ) VALUES (
                        current_detail_id, 'EXIT', random_quantity, sale_date,
                        CONCAT('Venta ID: ', current_sale_id), NOW(), NOW(),
                        random_product_id, '2', 'SYSTEM'
                    );
                    
                    SET current_detail_id = current_detail_id + 1;
                END IF;
                SET i = i + 1;
            END WHILE;
            
            SET tax_amount = subtotal * 0.13;
            SET total_amount = subtotal + tax_amount;
            
            UPDATE MKSales 
            SET subTotalAmount = subtotal, taxAmount = tax_amount, totalAmount = total_amount, updatedAt = NOW()
            WHERE IdSale = current_sale_id;
            
            SET current_sale_id = current_sale_id + 1;
            SET sales_created = sales_created + 1;
        END WHILE;
        
        -- =====================================================
        -- MES 4: SEPTIEMBRE 2024 (Repetir lógica)
        -- =====================================================
        SET month_start = '2024-09-01';
        SET month_end = '2024-09-30';
        SET sales_target = 50 + FLOOR(RAND() * 21);
        SET sales_created = 0;
        
        WHILE sales_created < sales_target DO
            SET sale_day = 1 + FLOOR(RAND() * 30);
            SET sale_hour = 7 + FLOOR(RAND() * 14);
            SET sale_minute = FLOOR(RAND() * 60);
            SET sale_date = DATE_ADD(month_start, INTERVAL sale_day - 1 DAY);
            SET sale_date = DATE_ADD(sale_date, INTERVAL sale_hour HOUR);
            SET sale_date = DATE_ADD(sale_date, INTERVAL sale_minute MINUTE);
            
            SET reference_number = CONCAT('VTA-', LPAD(commerce_id, 4, '0'), '-', LPAD(current_sale_id, 6, '0'), '-', DATE_FORMAT(sale_date, '%Y%m%d%H%i%s'));
            SET payment_method = 1 + FLOOR(RAND() * 4);
            SET product_count = 1 + FLOOR(RAND() * 4);
            SET subtotal = 0;
            SET i = 0;
            
            INSERT INTO MKSales (
                IdSale, IDCommerceFK2, saleDate, saleStatus, subTotalAmount,
                discountAmount, taxAmount, totalAmount, paymentStatus,
                invoiceRequired, receiptGenerated, IDPaymentMethodFK,
                IDcashierUserFK, referenceNumber, createdAt, updatedAt, checksum
            ) VALUES (
                current_sale_id, commerce_id, sale_date, 'COMPLETED', 0,
                0, 0, 0, 'COMPLETED', 0, 1, payment_method,
                2, reference_number, NOW(), NOW(), SHA2(CONCAT('sale_', current_sale_id), 256)
            );
            
            WHILE i < product_count DO
                IF commerce_id = 2 THEN
                    SET random_product_id = 1 + FLOOR(RAND() * 6);
                ELSEIF commerce_id = 4 THEN
                    SET random_product_id = 7 + FLOOR(RAND() * 6);
                ELSEIF commerce_id = 10 THEN
                    SET random_product_id = 13 + FLOOR(RAND() * 6);
                END IF;
                
                SELECT quantity INTO current_stock FROM MKProducts WHERE IdProduct = random_product_id;
                
                IF current_stock > 0 THEN
                    SET random_quantity = 1 + FLOOR(RAND() * 3);
                    IF random_quantity > current_stock THEN
                        SET random_quantity = current_stock;
                    END IF;
                    
                    SELECT pp.price INTO product_price
                    FROM MKProductPrices pp
                    INNER JOIN MKProductsPerMercadoPerBuilding pmpb ON pp.IDProductsInMercadoBuilding = pmpb.IdProductsInMercadoBuilding
                    WHERE pmpb.IDProductFK = random_product_id LIMIT 1;
                    
                    SET line_total = product_price * random_quantity;
                    SET subtotal = subtotal + line_total;
                    
                    INSERT INTO MKSalesDetails (
                        IdSaleDetails, IDSaleFK, IDProductFK3, productName,
                        quantitySold, unitMeasure, unitPrice, listPrice,
                        costPrice, lineTotal, inventoryUpdated, createdAt
                    ) VALUES (
                        current_detail_id, current_sale_id, random_product_id, 
                        (SELECT name FROM MKProducts WHERE IdProduct = random_product_id),
                        random_quantity, 'unidad', product_price, product_price,
                        product_price * 0.5, line_total, 1, NOW()
                    );
                    
                    UPDATE MKProducts SET quantity = quantity - random_quantity WHERE IdProduct = random_product_id;
                    
                    INSERT INTO MKInventoryMovements (
                        IdInventoryMovement, movementType, quantity, movementDate,
                        notes, createdAt, updatedAt, IDProduct, userId, computer
                    ) VALUES (
                        current_detail_id, 'EXIT', random_quantity, sale_date,
                        CONCAT('Venta ID: ', current_sale_id), NOW(), NOW(),
                        random_product_id, '2', 'SYSTEM'
                    );
                    
                    SET current_detail_id = current_detail_id + 1;
                END IF;
                SET i = i + 1;
            END WHILE;
            
            SET tax_amount = subtotal * 0.13;
            SET total_amount = subtotal + tax_amount;
            
            UPDATE MKSales 
            SET subTotalAmount = subtotal, taxAmount = tax_amount, totalAmount = total_amount, updatedAt = NOW()
            WHERE IdSale = current_sale_id;
            
            SET current_sale_id = current_sale_id + 1;
            SET sales_created = sales_created + 1;
        END WHILE;
        
        -- Reset del flag done para el siguiente comercio
        SET done = FALSE;
    END LOOP;
    
    CLOSE comercios;
END$$

DELIMITER ;

CALL GenerateRandomSales();

SELECT 
    c.name as Comercio,
    COUNT(s.IdSale) as 'Total Ventas',
    DATE_FORMAT(MIN(s.saleDate), '%Y-%m') as 'Primer Mes',
    DATE_FORMAT(MAX(s.saleDate), '%Y-%m') as 'Último Mes',
    FORMAT(SUM(s.totalAmount), 2) as 'Total Vendido (₡)',
    FORMAT(AVG(s.totalAmount), 2) as 'Promedio por Venta (₡)'
FROM MKCommerces c
INNER JOIN MKSales s ON c.IdCommerce = s.IDCommerceFK2
WHERE c.IdCommerce IN (2, 4, 10)
GROUP BY c.IdCommerce, c.name
ORDER BY COUNT(s.IdSale) DESC;

SELECT 
    c.name as Comercio,
    DATE_FORMAT(s.saleDate, '%Y-%m') as Mes,
    COUNT(s.IdSale) as 'Ventas del Mes',
    FORMAT(SUM(s.totalAmount), 2) as 'Total del Mes (₡)'
FROM MKCommerces c
INNER JOIN MKSales s ON c.IdCommerce = s.IDCommerceFK2
WHERE c.IdCommerce IN (2, 4, 10)
GROUP BY c.IdCommerce, c.name, DATE_FORMAT(s.saleDate, '%Y-%m')
ORDER BY c.name, Mes;

SELECT 
    p.name as Producto,
    c.name as Comercio,
    p.quantity as 'Stock Restante',
    CASE 
        WHEN p.quantity > 100 THEN '✅ Stock Alto'
        WHEN p.quantity > 50 THEN '⚠️ Stock Medio'
        WHEN p.quantity > 0 THEN '🔴 Stock Bajo'
        ELSE '❌ Sin Stock'
    END as Estado
FROM MKProducts p
INNER JOIN MKInventory i ON p.IDInventoryFK = i.IdInventory
INNER JOIN MKCommerces c ON i.IDCommerceFK = c.IdCommerce
WHERE c.IdCommerce IN (2, 4, 10)
ORDER BY c.name, p.name;

-- Limpiar procedimiento temporal
DROP PROCEDURE GenerateRandomSales;

-- 16. Datos de Log y demas

-- Códigos de barras para algunos productos principales
INSERT INTO MKBarcode (IdBarcode, IDProductFK2, barcode, createdAt, updatedAt) VALUES
(1, 1, '7501234567890', NOW(), NOW()),  -- Café Americano
(2, 4, '7501234567891', NOW(), NOW()),  -- Coca Cola
(3, 7, '7501234567892', NOW(), NOW()),  -- Hamburguesa Clásica
(4, 13, '7501234567893', NOW(), NOW()); -- Pizza Margarita

select * from MKBarcode;

-- Log severities, sources y types para auditoría
INSERT INTO MKLogSeverities (IdLogSeverity, name, level, priority, createdAt) VALUES
(1, 'INFO', 'Information', 1, NOW()),
(2, 'WARNING', 'Warning', 2, NOW()),
(3, 'ERROR', 'Error', 3, NOW()),
(4, 'CRITICAL', 'Critical', 4, NOW());

select * from MKLogSeverities;

INSERT INTO MKLogSource (IdLogSource, name, description, createdAt) VALUES
(1, 'API', 'Aplicación API REST', NOW()),
(2, 'WEB', 'Aplicación Web', NOW()),
(3, 'MOBILE', 'Aplicación Móvil', NOW()),
(4, 'SYSTEM', 'Sistema Interno', NOW());

select * from MKLogSource;

INSERT INTO MKLogType (IdLogType, name, description, createdAt) VALUES
(1, 'SALE', 'Operaciones de ventas', NOW()),
(2, 'SETTLEMENT', 'Operaciones de liquidación', NOW()),
(3, 'AUTH', 'Autenticación y autorización', NOW()),
(4, 'SYSTEM', 'Operaciones del sistema', NOW());

select * from MKLogType;

select * from MKSales;

select * from MKSalesDetails;

SELECT COUNT(*) as 'Total Ventas Creadas' FROM MKSales;
SELECT COUNT(*) as 'Total Comercios Creados' FROM MKCommerces;
SELECT COUNT(*) as 'Total Productos con Inventory' FROM MKProducts WHERE IDInventoryFK IS NOT NULL;