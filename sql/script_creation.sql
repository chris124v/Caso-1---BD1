-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema Caso1
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Caso1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Caso1` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `Caso1` ;

-- -----------------------------------------------------
-- Table `Caso1`.`MKUsers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKUsers` (
  `IdUser` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `password` VARBINARY(160) NOT NULL,
  `phoneNumber` VARCHAR(25) NOT NULL,
  `isActive` BIT(1) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdUser`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKRoles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKRoles` (
  `IdRole` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `description` VARCHAR(200) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdRole`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKPermissions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKPermissions` (
  `IdPermission` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `description` VARCHAR(120) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  `code` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`IdPermission`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKUserRoles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKUserRoles` (
  `IdUserRole` INT NOT NULL AUTO_INCREMENT,
  `IDUserFK` INT NOT NULL,
  `IDRoleFK` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdUserRole`),
  INDEX `fk_MKUserRoles_MKUsers1_idx` (`IDUserFK` ASC) VISIBLE,
  INDEX `fk_MKUserRoles_MKRoles1_idx` (`IDRoleFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKUserRoles_MKUsers1`
    FOREIGN KEY (`IDUserFK`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKUserRoles_MKRoles1`
    FOREIGN KEY (`IDRoleFK`)
    REFERENCES `Caso1`.`MKRoles` (`IdRole`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKRolePermissions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKRolePermissions` (
  `IdRolePermission` INT NOT NULL AUTO_INCREMENT,
  `IDPermissionFK` INT NOT NULL,
  `IDRoleFK` INT NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdRolePermission`),
  INDEX `fk_MKRolePermissions_MKPermissions1_idx` (`IDPermissionFK` ASC) VISIBLE,
  INDEX `fk_MKRolePermissions_MKRoles1_idx` (`IDRoleFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKRolePermissions_MKPermissions1`
    FOREIGN KEY (`IDPermissionFK`)
    REFERENCES `Caso1`.`MKPermissions` (`IdPermission`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKRolePermissions_MKRoles1`
    FOREIGN KEY (`IDRoleFK`)
    REFERENCES `Caso1`.`MKRoles` (`IdRole`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKCountries`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKCountries` (
  `IdCountry` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdCountry`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKStates`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKStates` (
  `IdState` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `IDCountryFK` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdState`),
  INDEX `fk_MKStates_MKCountries1_idx` (`IDCountryFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKStates_MKCountries1`
    FOREIGN KEY (`IDCountryFK`)
    REFERENCES `Caso1`.`MKCountries` (`IdCountry`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKCities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKCities` (
  `IdCity` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `IDStateFK` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdCity`),
  INDEX `fk_MKCities_MKStates1_idx` (`IDStateFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKCities_MKStates1`
    FOREIGN KEY (`IDStateFK`)
    REFERENCES `Caso1`.`MKStates` (`IdState`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKAddresses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKAddresses` (
  `IdAddress` INT NOT NULL AUTO_INCREMENT,
  `PostalCode` VARCHAR(10) NOT NULL,
  `direccion1` VARCHAR(100) NOT NULL,
  `direccion2` VARCHAR(150) NOT NULL,
  `geolocation` POINT NOT NULL,
  `IDCityFK` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdAddress`),
  INDEX `fk_MKAddresses_MKCities1_idx` (`IDCityFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKAddresses_MKCities1`
    FOREIGN KEY (`IDCityFK`)
    REFERENCES `Caso1`.`MKCities` (`IdCity`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKContractTypes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKContractTypes` (
  `IdContractType` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `description` VARCHAR(100) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdContractType`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKContractStatus`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKContractStatus` (
  `IdContractStatus` INT NOT NULL,
  `statusName` VARCHAR(60) NOT NULL,
  `description` VARCHAR(200) NOT NULL,
  `allowsSales` BIT(1) NOT NULL,
  `isActive` BIT(1) NOT NULL,
  PRIMARY KEY (`IdContractStatus`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKContracts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKContracts` (
  `IdContract` INT NOT NULL AUTO_INCREMENT,
  `contractNumber` INT NOT NULL,
  `IDContractTypeFK` INT NOT NULL,
  `IDContractStatusFK` INT NOT NULL,
  `startDate` DATETIME NOT NULL,
  `endDate` DATETIME NOT NULL,
  `autoRenewal` BIT(1) NOT NULL DEFAULT 0,
  `renewalDays` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `createdBy` INT NOT NULL,
  `signedDate` DATE NOT NULL,
  `lastModified` DATE NOT NULL,
  `notes` VARCHAR(250) NOT NULL,
  `isActive` BIT(1) NOT NULL,
  PRIMARY KEY (`IdContract`),
  UNIQUE INDEX `contractNumber_UNIQUE` (`contractNumber` ASC) VISIBLE,
  INDEX `fk_MKContracts_MKContractTypes1_idx` (`IDContractTypeFK` ASC) VISIBLE,
  INDEX `fk_MKContracts_MKUsers1_idx` (`createdBy` ASC) VISIBLE,
  INDEX `fk_MKContracts_MKContractStatus1_idx` (`IDContractStatusFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKContracts_MKContractTypes1`
    FOREIGN KEY (`IDContractTypeFK`)
    REFERENCES `Caso1`.`MKContractTypes` (`IdContractType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKContracts_MKUsers1`
    FOREIGN KEY (`createdBy`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKContracts_MKContractStatus1`
    FOREIGN KEY (`IDContractStatusFK`)
    REFERENCES `Caso1`.`MKContractStatus` (`IdContractStatus`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKContractTerms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKContractTerms` (
  `IdContractTerms` INT NOT NULL AUTO_INCREMENT,
  `IdContractFK` INT NOT NULL,
  `termCategory` ENUM("PAYMENT", "OPERATIONAL", "LEGAL", "SPECIAL") NOT NULL,
  `termName` VARCHAR(60) NOT NULL,
  `description` VARCHAR(250) NOT NULL,
  `isMandatory` BIT(1) NOT NULL DEFAULT 1,
  `penaltyAmount` DECIMAL(10,2) NOT NULL,
  `isActive` BIT(1) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdContractTerms`),
  INDEX `fk_MKContractTerms_MKContracts1_idx` (`IdContractFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKContractTerms_MKContracts1`
    FOREIGN KEY (`IdContractFK`)
    REFERENCES `Caso1`.`MKContracts` (`IdContract`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKCommerceCategories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKCommerceCategories` (
  `IdCommerceCategory` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `description` VARCHAR(100) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdCommerceCategory`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKCommerceStatus`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKCommerceStatus` (
  `IdCommerceStatus` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `description` VARCHAR(100) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdCommerceStatus`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKCommerces`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKCommerces` (
  `IdCommerce` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `description` VARCHAR(200) NOT NULL,
  `IDCommerceCategoryFK` INT NOT NULL,
  `IDCommerceStatusFK` INT NOT NULL,
  `phoneNumber` VARCHAR(20) NOT NULL,
  `emailAddress` VARCHAR(30) NOT NULL,
  `schedule` VARCHAR(200) NOT NULL,
  `startDate` DATE NOT NULL,
  `endDate` DATE NOT NULL,
  `isActive` BIT(1) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  `IDAddressFK` INT NOT NULL,
  `legalName` VARCHAR(60) NOT NULL,
  `legalID` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`IdCommerce`),
  INDEX `fk_MKCommerces_MKCommerceCategories1_idx` (`IDCommerceCategoryFK` ASC) VISIBLE,
  INDEX `fk_MKCommerces_MKCommerceStatus1_idx` (`IDCommerceStatusFK` ASC) VISIBLE,
  INDEX `fk_MKCommerces_MKAddresses1_idx` (`IDAddressFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKCommerces_MKCommerceCategories1`
    FOREIGN KEY (`IDCommerceCategoryFK`)
    REFERENCES `Caso1`.`MKCommerceCategories` (`IdCommerceCategory`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKCommerces_MKCommerceStatus1`
    FOREIGN KEY (`IDCommerceStatusFK`)
    REFERENCES `Caso1`.`MKCommerceStatus` (`IdCommerceStatus`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKCommerces_MKAddresses1`
    FOREIGN KEY (`IDAddressFK`)
    REFERENCES `Caso1`.`MKAddresses` (`IdAddress`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKMercado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKMercado` (
  `IdMercado` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `adminID` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  `cedulaJuridica` VARCHAR(20) NOT NULL,
  `sociedadAnonima` VARCHAR(60) NOT NULL,
  `addressNonFisical` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`IdMercado`),
  INDEX `fk_MKMercado_MKUsers1_idx` (`adminID` ASC) VISIBLE,
  CONSTRAINT `fk_MKMercado_MKUsers1`
    FOREIGN KEY (`adminID`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKBuilding`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKBuilding` (
  `IdBuilding` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `IDAddressFK` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdBuilding`),
  INDEX `fk_MKBuilding_MKAddresses1_idx` (`IDAddressFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKBuilding_MKAddresses1`
    FOREIGN KEY (`IDAddressFK`)
    REFERENCES `Caso1`.`MKAddresses` (`IdAddress`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKMercadoPerBuilding`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKMercadoPerBuilding` (
  `IdMercadoPerBuilding` INT NOT NULL AUTO_INCREMENT,
  `IDMercadoFK` INT NOT NULL,
  `IDBuildingFK` INT NOT NULL,
  `description` VARCHAR(200) NOT NULL,
  `deleted` BIT(1) NOT NULL,
  `localNumberInBuidling` INT NOT NULL,
  `m2Size` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`IdMercadoPerBuilding`),
  INDEX `fk_MKMercadoPerBuilding_MKMercado1_idx` (`IDMercadoFK` ASC) VISIBLE,
  INDEX `fk_MKMercadoPerBuilding_MKBuilding1_idx` (`IDBuildingFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKMercadoPerBuilding_MKMercado1`
    FOREIGN KEY (`IDMercadoFK`)
    REFERENCES `Caso1`.`MKMercado` (`IdMercado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKMercadoPerBuilding_MKBuilding1`
    FOREIGN KEY (`IDBuildingFK`)
    REFERENCES `Caso1`.`MKBuilding` (`IdBuilding`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKSpaceStatus`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKSpaceStatus` (
  `IdSpaceStatus` INT NOT NULL AUTO_INCREMENT,
  `statusName` VARCHAR(30) NOT NULL,
  `description` VARCHAR(100) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdSpaceStatus`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKSpaceTypes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKSpaceTypes` (
  `IdSpaceType` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `description` VARCHAR(200) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdSpaceType`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKSpaces`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKSpaces` (
  `IdSpace` INT NOT NULL AUTO_INCREMENT,
  `spaceName` VARCHAR(60) NOT NULL,
  `IDSpaceStatusFK` INT NOT NULL,
  `IDSpaceType` INT NOT NULL,
  `number` INT NOT NULL,
  `m2size` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`IdSpace`),
  INDEX `fk_MKSpaces_MKSpaceStatus1_idx` (`IDSpaceStatusFK` ASC) VISIBLE,
  INDEX `fk_MKSpaces_MKSpaceTypes1_idx` (`IDSpaceType` ASC) VISIBLE,
  CONSTRAINT `fk_MKSpaces_MKSpaceStatus1`
    FOREIGN KEY (`IDSpaceStatusFK`)
    REFERENCES `Caso1`.`MKSpaceStatus` (`IdSpaceStatus`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKSpaces_MKSpaceTypes1`
    FOREIGN KEY (`IDSpaceType`)
    REFERENCES `Caso1`.`MKSpaceTypes` (`IdSpaceType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKContractsPerCommerces`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKContractsPerCommerces` (
  `IdContractPerCommerce` INT NOT NULL AUTO_INCREMENT,
  `IDContractFK` INT NOT NULL,
  `IDCommerceFK` INT NOT NULL,
  `IDMercadoPerBuilding` INT NOT NULL,
  `IDSpaceFK` INT NOT NULL,
  `baseMonthlyRent` DECIMAL(10,2) NOT NULL,
  `commisionPercentage` DECIMAL(5,2) NOT NULL,
  `securityDeposit` DECIMAL(10,2) NOT NULL,
  `settlementDay` DATE NOT NULL,
  `lateFeePayment` DECIMAL(10,2) NOT NULL,
  `minimunMonthlySales` DECIMAL(10,2) NOT NULL,
  `utilitiesIncluded` BIT(1) NOT NULL,
  `isCurrent` BIT(1) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  `notes` TEXT NOT NULL,
  PRIMARY KEY (`IdContractPerCommerce`),
  INDEX `fk_MKContractsPerCommerces_MKContracts1_idx` (`IDContractFK` ASC) VISIBLE,
  INDEX `fk_MKContractsPerCommerces_MKCommerces1_idx` (`IDCommerceFK` ASC) VISIBLE,
  INDEX `fk_MKContractsPerCommerces_MKMercadoPerBuilding1_idx` (`IDMercadoPerBuilding` ASC) VISIBLE,
  INDEX `fk_MKContractsPerCommerces_MKSpaces1_idx` (`IDSpaceFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKContractsPerCommerces_MKContracts1`
    FOREIGN KEY (`IDContractFK`)
    REFERENCES `Caso1`.`MKContracts` (`IdContract`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKContractsPerCommerces_MKCommerces1`
    FOREIGN KEY (`IDCommerceFK`)
    REFERENCES `Caso1`.`MKCommerces` (`IdCommerce`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKContractsPerCommerces_MKMercadoPerBuilding1`
    FOREIGN KEY (`IDMercadoPerBuilding`)
    REFERENCES `Caso1`.`MKMercadoPerBuilding` (`IdMercadoPerBuilding`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKContractsPerCommerces_MKSpaces1`
    FOREIGN KEY (`IDSpaceFK`)
    REFERENCES `Caso1`.`MKSpaces` (`IdSpace`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKContractRenewals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKContractRenewals` (
  `IdContractRenewal` INT NOT NULL AUTO_INCREMENT,
  `IDOriginalContractFK` INT NOT NULL,
  `IDNewContractFK` INT NOT NULL,
  `renewalType` ENUM("AUTOMATIC", "MANUAL", "NEGOTIATED") NOT NULL,
  `renewalDate` DATE NOT NULL,
  `renewalPeriodMonths` INT NOT NULL,
  `rentIncreasePercentage` DECIMAL(10,2) NOT NULL,
  `newComissionPercentage` DECIMAL(10,2) NOT NULL,
  `termsModified` BIT(1) NOT NULL,
  `notes` TEXT NOT NULL,
  `approvedByUserFK` INT NOT NULL,
  `approvedDate` DATE NOT NULL,
  `tenantAccepted` BIT(1) NOT NULL,
  PRIMARY KEY (`IdContractRenewal`),
  INDEX `fk_MKContractRenewals_MKContracts1_idx` (`IDOriginalContractFK` ASC) VISIBLE,
  INDEX `fk_MKContractRenewals_MKContracts2_idx` (`IDNewContractFK` ASC) VISIBLE,
  INDEX `fk_MKContractRenewals_MKUsers1_idx` (`approvedByUserFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKContractRenewals_MKContracts1`
    FOREIGN KEY (`IDOriginalContractFK`)
    REFERENCES `Caso1`.`MKContracts` (`IdContract`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKContractRenewals_MKContracts2`
    FOREIGN KEY (`IDNewContractFK`)
    REFERENCES `Caso1`.`MKContracts` (`IdContract`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKContractRenewals_MKUsers1`
    FOREIGN KEY (`approvedByUserFK`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKPaymentMethods`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKPaymentMethods` (
  `IdPaymentMethod` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `description` VARCHAR(100) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `enabled` BIT(1) NOT NULL,
  PRIMARY KEY (`IdPaymentMethod`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKSales`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKSales` (
  `IdSale` INT NOT NULL AUTO_INCREMENT,
  `IDCommerceFK2` INT NOT NULL,
  `saleDate` DATETIME NOT NULL,
  `saleStatus` ENUM("PENDING", "COMPLETED", "CANCELED", "REFUNDED") NOT NULL,
  `subTotalAmount` DECIMAL(10,2) NOT NULL,
  `discountAmount` DECIMAL(10,2) NOT NULL,
  `taxAmount` DECIMAL(10,2) NOT NULL,
  `totalAmount` DECIMAL(10,2) NOT NULL,
  `paymentStatus` ENUM("PENDING", "PARTIAL", "COMPLETED", "FAILED") NOT NULL,
  `invoiceRequired` BIT(1) NOT NULL,
  `receiptGenerated` BIT(1) NOT NULL,
  `IDPaymentMethodFK` INT NOT NULL,
  `IDcashierUserFK` INT NOT NULL,
  `referenceNumber` VARCHAR(60) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  `checksum` VARBINARY(160) NOT NULL,
  PRIMARY KEY (`IdSale`),
  INDEX `fk_MKSales_MKUsers1_idx` (`IDcashierUserFK` ASC) VISIBLE,
  INDEX `fk_MKSales_MKCommerces1_idx` (`IDCommerceFK2` ASC) VISIBLE,
  INDEX `fk_MKSales_MKPaymentMethods1_idx` (`IDPaymentMethodFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKSales_MKUsers1`
    FOREIGN KEY (`IDcashierUserFK`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKSales_MKCommerces1`
    FOREIGN KEY (`IDCommerceFK2`)
    REFERENCES `Caso1`.`MKCommerces` (`IdCommerce`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKSales_MKPaymentMethods1`
    FOREIGN KEY (`IDPaymentMethodFK`)
    REFERENCES `Caso1`.`MKPaymentMethods` (`IdPaymentMethod`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKProductCategories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKProductCategories` (
  `IdProductCategory` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `description` VARCHAR(200) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `unitSystem` VARCHAR(60) NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdProductCategory`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKProductBrand`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKProductBrand` (
  `IdProductBrand` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `description` VARCHAR(200) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdProductBrand`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKInventory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKInventory` (
  `IdInventory` INT NOT NULL AUTO_INCREMENT,
  `IDCommerceFK` INT NOT NULL,
  `name` VARCHAR(60) NOT NULL,
  `description` VARCHAR(200) NOT NULL,
  `stockComplete` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  `IDMercadoPerBuilding` INT NOT NULL,
  PRIMARY KEY (`IdInventory`),
  INDEX `fk_MKInventory_MKCommerces1_idx` (`IDCommerceFK` ASC) VISIBLE,
  INDEX `fk_MKInventory_MKMercadoPerBuilding1_idx` (`IDMercadoPerBuilding` ASC) VISIBLE,
  CONSTRAINT `fk_MKInventory_MKCommerces1`
    FOREIGN KEY (`IDCommerceFK`)
    REFERENCES `Caso1`.`MKCommerces` (`IdCommerce`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKInventory_MKMercadoPerBuilding1`
    FOREIGN KEY (`IDMercadoPerBuilding`)
    REFERENCES `Caso1`.`MKMercadoPerBuilding` (`IdMercadoPerBuilding`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKProducts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKProducts` (
  `IdProduct` INT NOT NULL AUTO_INCREMENT,
  `IDProductCategory` INT NOT NULL,
  `IDProductBrand` INT NOT NULL,
  `name` VARCHAR(60) NOT NULL,
  `description` VARCHAR(200) NOT NULL,
  `status` ENUM("AVAILABLE", "NOT_AVAILABLE") NOT NULL,
  `quantity` INT NOT NULL,
  `expires` BIT(1) NOT NULL,
  `expirationDate` DATE NOT NULL,
  `deleted` BIT(1) NOT NULL,
  `enabled` BIT(1) NOT NULL,
  `IDInventoryFK` INT NOT NULL,
  `IDMercadoPerBuilding` INT NOT NULL,
  PRIMARY KEY (`IdProduct`),
  INDEX `fk_MKProducts_MKProductCategories1_idx` (`IDProductCategory` ASC) VISIBLE,
  INDEX `fk_MKProducts_MKProductBrand1_idx` (`IDProductBrand` ASC) VISIBLE,
  INDEX `fk_MKProducts_MKInventory1_idx` (`IDInventoryFK` ASC) VISIBLE,
  INDEX `fk_MKProducts_MKMercadoPerBuilding1_idx` (`IDMercadoPerBuilding` ASC) VISIBLE,
  CONSTRAINT `fk_MKProducts_MKProductCategories1`
    FOREIGN KEY (`IDProductCategory`)
    REFERENCES `Caso1`.`MKProductCategories` (`IdProductCategory`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKProducts_MKProductBrand1`
    FOREIGN KEY (`IDProductBrand`)
    REFERENCES `Caso1`.`MKProductBrand` (`IdProductBrand`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKProducts_MKInventory1`
    FOREIGN KEY (`IDInventoryFK`)
    REFERENCES `Caso1`.`MKInventory` (`IdInventory`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKProducts_MKMercadoPerBuilding1`
    FOREIGN KEY (`IDMercadoPerBuilding`)
    REFERENCES `Caso1`.`MKMercadoPerBuilding` (`IdMercadoPerBuilding`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKSalesDetails`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKSalesDetails` (
  `IdSaleDetails` INT NOT NULL AUTO_INCREMENT,
  `IDSaleFK` INT NOT NULL,
  `IDProductFK3` INT NOT NULL,
  `productName` VARCHAR(60) NOT NULL,
  `quantitySold` INT NOT NULL,
  `unitMeasure` VARCHAR(60) NOT NULL,
  `unitPrice` DECIMAL(10,2) NOT NULL,
  `listPrice` DECIMAL(10,2) NOT NULL,
  `costPrice` DECIMAL(10,2) NOT NULL,
  `lineTotal` DECIMAL(10,2) NOT NULL,
  `inventoryUpdated` BIT(1) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdSaleDetails`),
  INDEX `fk_MKSalesDetails_MKSales1_idx` (`IDSaleFK` ASC) VISIBLE,
  INDEX `fk_MKSalesDetails_MKProducts1_idx` (`IDProductFK3` ASC) VISIBLE,
  CONSTRAINT `fk_MKSalesDetails_MKSales1`
    FOREIGN KEY (`IDSaleFK`)
    REFERENCES `Caso1`.`MKSales` (`IdSale`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKSalesDetails_MKProducts1`
    FOREIGN KEY (`IDProductFK3`)
    REFERENCES `Caso1`.`MKProducts` (`IdProduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKInvoices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKInvoices` (
  `IdInvoice` INT NOT NULL AUTO_INCREMENT,
  `IDSaleFK` INT NOT NULL,
  `invoiceNumber` VARCHAR(50) NOT NULL,
  `customerTaxId` VARCHAR(20) NOT NULL,
  `customerName` VARCHAR(100) NOT NULL,
  `invoiceDate` DATE NOT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL,
  `totalTax` DECIMAL(10,2) NOT NULL,
  `totalInvoice` DECIMAL(10,2) NOT NULL,
  `checksum` VARBINARY(160) NOT NULL,
  `invoiceStatus` ENUM("ISSUED", "PAID", "CANCELED") NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  `issuedByUser` INT NOT NULL,
  PRIMARY KEY (`IdInvoice`),
  INDEX `fk_MKInvoices_MKSales1_idx` (`IDSaleFK` ASC) VISIBLE,
  INDEX `fk_MKInvoices_MKUsers1_idx` (`issuedByUser` ASC) VISIBLE,
  CONSTRAINT `fk_MKInvoices_MKSales1`
    FOREIGN KEY (`IDSaleFK`)
    REFERENCES `Caso1`.`MKSales` (`IdSale`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKInvoices_MKUsers1`
    FOREIGN KEY (`issuedByUser`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKInvoiceDetails`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKInvoiceDetails` (
  `IdInvoiceDetail` INT NOT NULL AUTO_INCREMENT,
  `IDInvoiceFK` INT NOT NULL,
  `IDSaleDetailFK` INT NOT NULL,
  `productDescription` VARCHAR(100) NOT NULL,
  `quantity` DECIMAL(8,3) NOT NULL,
  `unitPrice` DECIMAL(10,2) NOT NULL,
  `lineSubtotal` DECIMAL(10,2) NOT NULL,
  `taxRate` DECIMAL(4,2) NOT NULL,
  `taxAmount` DECIMAL(10,2) NOT NULL,
  `lineTotal` DECIMAL(10,2) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdInvoiceDetail`),
  INDEX `fk_MKInvoiceDetails_MKInvoices1_idx` (`IDInvoiceFK` ASC) VISIBLE,
  INDEX `fk_MKInvoiceDetails_MKSalesDetails1_idx` (`IDSaleDetailFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKInvoiceDetails_MKInvoices1`
    FOREIGN KEY (`IDInvoiceFK`)
    REFERENCES `Caso1`.`MKInvoices` (`IdInvoice`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKInvoiceDetails_MKSalesDetails1`
    FOREIGN KEY (`IDSaleDetailFK`)
    REFERENCES `Caso1`.`MKSalesDetails` (`IdSaleDetails`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKReceipts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKReceipts` (
  `IdReceipt` INT NOT NULL AUTO_INCREMENT,
  `IDSaleFK` INT NOT NULL,
  `receiptNumber` VARCHAR(70) NOT NULL,
  `receiptType` ENUM("PRINTED", "EMAIL") NOT NULL,
  `receiptDate` DATETIME NOT NULL,
  `subTotal` DECIMAL(10,2) NOT NULL,
  `taxAmount` DECIMAL(10,2) NOT NULL,
  `discountAmount` DECIMAL(10,2) NOT NULL,
  `taxPercentage` DECIMAL(5,2) NOT NULL,
  `totalAmount` DECIMAL(10,2) NOT NULL,
  `printed` BIT(1) NOT NULL,
  `emailed` BIT(1) NOT NULL,
  `emailAddress` VARCHAR(30) NOT NULL,
  `promotionsApplied` VARCHAR(200) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  `checksum` VARBINARY(160) NOT NULL,
  `issuedBy` INT NOT NULL,
  PRIMARY KEY (`IdReceipt`),
  INDEX `fk_MKReceipts_MKSales1_idx` (`IDSaleFK` ASC) VISIBLE,
  INDEX `fk_MKReceipts_MKUsers1_idx` (`issuedBy` ASC) VISIBLE,
  CONSTRAINT `fk_MKReceipts_MKSales1`
    FOREIGN KEY (`IDSaleFK`)
    REFERENCES `Caso1`.`MKSales` (`IdSale`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKReceipts_MKUsers1`
    FOREIGN KEY (`issuedBy`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKSaleDiscounts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKSaleDiscounts` (
  `IdSaleDiscounts` INT NOT NULL AUTO_INCREMENT,
  `IDSaleFK` INT NOT NULL,
  `IDSaleDetail` INT NOT NULL,
  `authorizedBy` INT NOT NULL,
  `discountType` ENUM("PERCENTAGE", "FIXEDAMOUNT", "PROMOTION") NOT NULL,
  `discountReason` VARCHAR(100) NOT NULL,
  `discountName` VARCHAR(60) NOT NULL,
  `discountValue` DECIMAL(5,2) NOT NULL,
  `discountAmount` DECIMAL(10,2) NOT NULL,
  `validFrom` DATETIME NOT NULL,
  `validTo` DATETIME NOT NULL,
  `notes` VARCHAR(100) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdSaleDiscounts`),
  INDEX `fk_MKSaleDiscounts_MKSales1_idx` (`IDSaleFK` ASC) VISIBLE,
  INDEX `fk_MKSaleDiscounts_MKSalesDetails1_idx` (`IDSaleDetail` ASC) VISIBLE,
  INDEX `fk_MKSaleDiscounts_MKUsers1_idx` (`authorizedBy` ASC) VISIBLE,
  CONSTRAINT `fk_MKSaleDiscounts_MKSales1`
    FOREIGN KEY (`IDSaleFK`)
    REFERENCES `Caso1`.`MKSales` (`IdSale`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKSaleDiscounts_MKSalesDetails1`
    FOREIGN KEY (`IDSaleDetail`)
    REFERENCES `Caso1`.`MKSalesDetails` (`IdSaleDetails`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKSaleDiscounts_MKUsers1`
    FOREIGN KEY (`authorizedBy`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKInitialInvestment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKInitialInvestment` (
  `IdInitialInvestment` INT NOT NULL AUTO_INCREMENT,
  `IDMercadoPerBuildingFK` INT NOT NULL,
  `createdByOwner` INT NOT NULL,
  `InvestmentType` ENUM("REMODELING", "EQUIPMENT", "PERMITS", "OTHER") NOT NULL,
  `investmentDescription` VARCHAR(200) NOT NULL,
  `investedAmount` DECIMAL(10,2) NOT NULL,
  `investmentDate` DATE NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `notes` TEXT NOT NULL,
  PRIMARY KEY (`IdInitialInvestment`),
  INDEX `fk_MKInitialInvestment_MKUsers1_idx` (`createdByOwner` ASC) VISIBLE,
  INDEX `fk_MKInitialInvestment_MKMercadoPerBuilding1_idx` (`IDMercadoPerBuildingFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKInitialInvestment_MKUsers1`
    FOREIGN KEY (`createdByOwner`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKInitialInvestment_MKMercadoPerBuilding1`
    FOREIGN KEY (`IDMercadoPerBuildingFK`)
    REFERENCES `Caso1`.`MKMercadoPerBuilding` (`IdMercadoPerBuilding`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKTransactionTypes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKTransactionTypes` (
  `IdTransactionType` INT NOT NULL AUTO_INCREMENT,
  `typeName` VARCHAR(50) NOT NULL,
  `typeDescription` VARCHAR(200) NOT NULL,
  `transactionFlow` ENUM("INCOME", "EXPENSE") NOT NULL,
  `isActive` BIT(1) NOT NULL,
  PRIMARY KEY (`IdTransactionType`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKCommerceSettlement`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKCommerceSettlement` (
  `IdCommerceSettlement` INT NOT NULL AUTO_INCREMENT,
  `IDCommerceFK6` INT NOT NULL,
  `totalSalesAmount` DECIMAL(10,2) NOT NULL,
  `settlementPeriodStart` DATETIME NOT NULL,
  `settlementPeriodEnd` DATETIME NOT NULL,
  `totalRent` DECIMAL(10,2) NOT NULL,
  `totalCommission` DECIMAL(10,2) NOT NULL,
  `totalSettlementAmount` DECIMAL(10,2) NOT NULL,
  `settlementDate` DATE NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `UpdatedAt` DATETIME NOT NULL,
  `MKContractsPerCommerces_IdContractPerCommerce` INT NOT NULL,
  `MKMercadoPerBuilding_IdMercadoPerBuilding` INT NOT NULL,
  PRIMARY KEY (`IdCommerceSettlement`),
  INDEX `fk_MKCommerceSettlement_MKCommerces1_idx` (`IDCommerceFK6` ASC) VISIBLE,
  INDEX `fk_MKCommerceSettlement_MKContractsPerCommerces1_idx` (`MKContractsPerCommerces_IdContractPerCommerce` ASC) VISIBLE,
  INDEX `fk_MKCommerceSettlement_MKMercadoPerBuilding1_idx` (`MKMercadoPerBuilding_IdMercadoPerBuilding` ASC) VISIBLE,
  CONSTRAINT `fk_MKCommerceSettlement_MKCommerces1`
    FOREIGN KEY (`IDCommerceFK6`)
    REFERENCES `Caso1`.`MKCommerces` (`IdCommerce`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKCommerceSettlement_MKContractsPerCommerces1`
    FOREIGN KEY (`MKContractsPerCommerces_IdContractPerCommerce`)
    REFERENCES `Caso1`.`MKContractsPerCommerces` (`IdContractPerCommerce`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKCommerceSettlement_MKMercadoPerBuilding1`
    FOREIGN KEY (`MKMercadoPerBuilding_IdMercadoPerBuilding`)
    REFERENCES `Caso1`.`MKMercadoPerBuilding` (`IdMercadoPerBuilding`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKRelatedEntityType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKRelatedEntityType` (
  `idRelatedEntityType` INT NOT NULL,
  `nameEntity` VARCHAR(60) NOT NULL,
  `description` VARCHAR(100) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`idRelatedEntityType`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKTransactionSubTypes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKTransactionSubTypes` (
  `IdTransactionSubTypes` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `description` VARCHAR(100) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdTransactionSubTypes`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKFinancialTransactions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKFinancialTransactions` (
  `IdFinancialTransaction` INT NOT NULL,
  `IDTransactionTypeFK` INT NOT NULL,
  `IDRelatedEntityTypeFK` INT NOT NULL,
  `transactionNumber` VARCHAR(50) NOT NULL,
  `transactionDate` DATE NOT NULL,
  `transactionAmount` DECIMAL(10,2) NOT NULL,
  `transactionDescription` VARCHAR(200) NOT NULL,
  `referenceNumber` VARCHAR(100) NOT NULL,
  `refID` BIGINT NOT NULL,
  `checksum` VARBINARY(160) NOT NULL,
  `transactionStatus` ENUM("PENDING", "COMPLETED", "CANCELLED") NOT NULL,
  `notes` TEXT NOT NULL,
  `IDInitialInvestmentFK` INT NULL,
  `IDCommerceSettlementFK` INT NULL,
  `IDMercadoPerBuildingFK` INT NULL,
  `IDCommerceFK` INT NULL,
  `IDSpaceFK` INT NULL,
  `IDTransactionSubTypesFK` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdFinancialTransaction`),
  INDEX `fk_MKFinancialTransactions_MKTransactionTypes1_idx` (`IDTransactionTypeFK` ASC) VISIBLE,
  INDEX `fk_MKFinancialTransactions_MKInitialInvestment1_idx` (`IDInitialInvestmentFK` ASC) VISIBLE,
  INDEX `fk_MKFinancialTransactions_MKCommerceSettlement1_idx` (`IDCommerceSettlementFK` ASC) VISIBLE,
  INDEX `fk_MKFinancialTransactions_MKMercadoPerBuilding1_idx` (`IDMercadoPerBuildingFK` ASC) VISIBLE,
  INDEX `fk_MKFinancialTransactions_MKCommerces1_idx` (`IDCommerceFK` ASC) VISIBLE,
  INDEX `fk_MKFinancialTransactions_MKSpaces1_idx` (`IDSpaceFK` ASC) VISIBLE,
  INDEX `fk_MKFinancialTransactions_MKRelatedEntityType1_idx` (`IDRelatedEntityTypeFK` ASC) VISIBLE,
  INDEX `fk_MKFinancialTransactions_MKTransactionSubTypes1_idx` (`IDTransactionSubTypesFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKFinancialTransactions_MKTransactionTypes1`
    FOREIGN KEY (`IDTransactionTypeFK`)
    REFERENCES `Caso1`.`MKTransactionTypes` (`IdTransactionType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKFinancialTransactions_MKInitialInvestment1`
    FOREIGN KEY (`IDInitialInvestmentFK`)
    REFERENCES `Caso1`.`MKInitialInvestment` (`IdInitialInvestment`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKFinancialTransactions_MKCommerceSettlement1`
    FOREIGN KEY (`IDCommerceSettlementFK`)
    REFERENCES `Caso1`.`MKCommerceSettlement` (`IdCommerceSettlement`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKFinancialTransactions_MKMercadoPerBuilding1`
    FOREIGN KEY (`IDMercadoPerBuildingFK`)
    REFERENCES `Caso1`.`MKMercadoPerBuilding` (`IdMercadoPerBuilding`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKFinancialTransactions_MKCommerces1`
    FOREIGN KEY (`IDCommerceFK`)
    REFERENCES `Caso1`.`MKCommerces` (`IdCommerce`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKFinancialTransactions_MKSpaces1`
    FOREIGN KEY (`IDSpaceFK`)
    REFERENCES `Caso1`.`MKSpaces` (`IdSpace`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKFinancialTransactions_MKRelatedEntityType1`
    FOREIGN KEY (`IDRelatedEntityTypeFK`)
    REFERENCES `Caso1`.`MKRelatedEntityType` (`idRelatedEntityType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKFinancialTransactions_MKTransactionSubTypes1`
    FOREIGN KEY (`IDTransactionSubTypesFK`)
    REFERENCES `Caso1`.`MKTransactionSubTypes` (`IdTransactionSubTypes`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKCommissionCalculatios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKCommissionCalculatios` (
  `IdCommissionCalculations` INT NOT NULL,
  `IDCommerceFK5` INT NOT NULL,
  `calculationPeriod` VARCHAR(7) NOT NULL,
  `totalSalesAmount` DECIMAL(10,2) NOT NULL,
  `commissionPercentage` DECIMAL(5,2) NOT NULL,
  `calculatedCommission` DECIMAL(10,2) NOT NULL,
  `calculationDate` DATE NOT NULL,
  `calculationStatus` ENUM("DRAFT", "CONFIRMED", "BILLED") NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `notes` TEXT NOT NULL,
  `createdBy` INT NOT NULL,
  PRIMARY KEY (`IdCommissionCalculations`),
  INDEX `fk_MKCommissionCalculatios_MKCommerces1_idx` (`IDCommerceFK5` ASC) VISIBLE,
  INDEX `fk_MKCommissionCalculatios_MKUsers1_idx` (`createdBy` ASC) VISIBLE,
  CONSTRAINT `fk_MKCommissionCalculatios_MKCommerces1`
    FOREIGN KEY (`IDCommerceFK5`)
    REFERENCES `Caso1`.`MKCommerces` (`IdCommerce`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKCommissionCalculatios_MKUsers1`
    FOREIGN KEY (`createdBy`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKLogSeverities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKLogSeverities` (
  `IdLogSeverity` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `level` VARCHAR(60) NOT NULL,
  `priority` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdLogSeverity`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKLogSource`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKLogSource` (
  `IdLogSource` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `description` VARCHAR(100) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdLogSource`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKLogType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKLogType` (
  `IdLogType` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `description` VARCHAR(100) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdLogType`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKLogs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKLogs` (
  `IdLog` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(255) NOT NULL,
  `postTime` DATETIME NOT NULL,
  `computer` VARCHAR(100) NOT NULL,
  `username` VARCHAR(100) NOT NULL,
  `trace` VARCHAR(255) NOT NULL,
  `referenceID1` BIGINT NOT NULL,
  `referenceID2` BIGINT NOT NULL,
  `value1` VARCHAR(100) NOT NULL,
  `value2` VARCHAR(100) NOT NULL,
  `checksum` VARBINARY(160) NOT NULL,
  `lastUpdate` DATETIME NOT NULL,
  `IDLogSeverityFK` INT NOT NULL,
  `IDLogSourceFK` INT NOT NULL,
  `IDLogTypeFK` INT NOT NULL,
  `IDUserFK2` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdLog`),
  INDEX `fk_MKLog_MKLogSeverities1_idx` (`IDLogSeverityFK` ASC) VISIBLE,
  INDEX `fk_MKLog_MKLogSource1_idx` (`IDLogSourceFK` ASC) VISIBLE,
  INDEX `fk_MKLog_MKLogType1_idx` (`IDLogTypeFK` ASC) VISIBLE,
  INDEX `fk_MKLogs_MKUsers1_idx` (`IDUserFK2` ASC) VISIBLE,
  CONSTRAINT `fk_MKLog_MKLogSeverities1`
    FOREIGN KEY (`IDLogSeverityFK`)
    REFERENCES `Caso1`.`MKLogSeverities` (`IdLogSeverity`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKLog_MKLogSource1`
    FOREIGN KEY (`IDLogSourceFK`)
    REFERENCES `Caso1`.`MKLogSource` (`IdLogSource`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKLog_MKLogType1`
    FOREIGN KEY (`IDLogTypeFK`)
    REFERENCES `Caso1`.`MKLogType` (`IdLogType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKLogs_MKUsers1`
    FOREIGN KEY (`IDUserFK2`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKSpaceAttributes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKSpaceAttributes` (
  `IdSpaceAttributes` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `description` VARCHAR(100) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `SpaceID` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`IdSpaceAttributes`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKInventoryMovements`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKInventoryMovements` (
  `IdInventoryMovement` INT NOT NULL AUTO_INCREMENT,
  `movementType` ENUM("ENTRY", "EXIT", "UPDATED") NOT NULL,
  `quantity` INT NOT NULL,
  `movementDate` DATETIME NOT NULL,
  `notes` VARCHAR(200) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` VARCHAR(45) NOT NULL,
  `IDProduct` INT NOT NULL,
  `userId` VARCHAR(45) NULL,
  `computer` VARCHAR(45) NULL,
  PRIMARY KEY (`IdInventoryMovement`),
  INDEX `fk_MKInventoryMovements_MKProducts1_idx` (`IDProduct` ASC) VISIBLE,
  CONSTRAINT `fk_MKInventoryMovements_MKProducts1`
    FOREIGN KEY (`IDProduct`)
    REFERENCES `Caso1`.`MKProducts` (`IdProduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKProductsPerMercadoPerBuilding`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKProductsPerMercadoPerBuilding` (
  `IdProductsInMercadoBuilding` INT NOT NULL AUTO_INCREMENT,
  `IDProductFK` INT NOT NULL,
  `IDMercadoPerBuildingFK` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdProductsInMercadoBuilding`),
  INDEX `fk_MKProductsPerMercadoPerBuilding_MKProducts1_idx` (`IDProductFK` ASC) VISIBLE,
  INDEX `fk_MKProductsPerMercadoPerBuilding_MKMercadoPerBuilding1_idx` (`IDMercadoPerBuildingFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKProductsPerMercadoPerBuilding_MKProducts1`
    FOREIGN KEY (`IDProductFK`)
    REFERENCES `Caso1`.`MKProducts` (`IdProduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKProductsPerMercadoPerBuilding_MKMercadoPerBuilding1`
    FOREIGN KEY (`IDMercadoPerBuildingFK`)
    REFERENCES `Caso1`.`MKMercadoPerBuilding` (`IdMercadoPerBuilding`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKProductPrices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKProductPrices` (
  `IdProductPrices` INT NOT NULL AUTO_INCREMENT,
  `price` DECIMAL(10,2) NOT NULL,
  `startDate` DATE NOT NULL,
  `endDate` DATE NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  `IDProductsInMercadoBuilding` INT NOT NULL,
  PRIMARY KEY (`IdProductPrices`),
  INDEX `fk_MKProductPrices_MKProductsPerMercadoPerBuilding1_idx` (`IDProductsInMercadoBuilding` ASC) VISIBLE,
  CONSTRAINT `fk_MKProductPrices_MKProductsPerMercadoPerBuilding1`
    FOREIGN KEY (`IDProductsInMercadoBuilding`)
    REFERENCES `Caso1`.`MKProductsPerMercadoPerBuilding` (`IdProductsInMercadoBuilding`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKBarcode`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKBarcode` (
  `IdBarcode` INT NOT NULL AUTO_INCREMENT,
  `IDProductFK2` INT NOT NULL,
  `barcode` VARCHAR(60) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdBarcode`),
  INDEX `fk_MKBarcode_MKProducts1_idx` (`IDProductFK2` ASC) VISIBLE,
  CONSTRAINT `fk_MKBarcode_MKProducts1`
    FOREIGN KEY (`IDProductFK2`)
    REFERENCES `Caso1`.`MKProducts` (`IdProduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKCommerceSettlementDetail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKCommerceSettlementDetail` (
  `IdCommerceSettlementDetail` INT NOT NULL AUTO_INCREMENT,
  `IDCommerceSettlementFK` INT NOT NULL,
  `IDSaleFK` INT NOT NULL,
  `saleDate` DATETIME NOT NULL,
  `saleAmount` DECIMAL(10,2) NOT NULL,
  `commisionPercentage` DECIMAL(5,2) NOT NULL,
  `commissionAmount` DECIMAL(10,2) NOT NULL,
  `includedInSettlement` BIT(1) NOT NULL,
  `status` ENUM("INCLUDED", "EXCLUDED") NOT NULL,
  `proccesedDate` DATETIME NOT NULL,
  `notes` TEXT NOT NULL,
  `originalSaleTotal` DECIMAL(10,2) NOT NULL,
  `createdAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdCommerceSettlementDetail`),
  INDEX `fk_MKCommerceSettlementDetail_MKCommerceSettlement1_idx` (`IDCommerceSettlementFK` ASC) VISIBLE,
  INDEX `fk_MKCommerceSettlementDetail_MKSales1_idx` (`IDSaleFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKCommerceSettlementDetail_MKCommerceSettlement1`
    FOREIGN KEY (`IDCommerceSettlementFK`)
    REFERENCES `Caso1`.`MKCommerceSettlement` (`IdCommerceSettlement`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKCommerceSettlementDetail_MKSales1`
    FOREIGN KEY (`IDSaleFK`)
    REFERENCES `Caso1`.`MKSales` (`IdSale`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKSpacesPerSpaceAttributes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKSpacesPerSpaceAttributes` (
  `IdSpacePerSpaceAttributes` INT NOT NULL AUTO_INCREMENT,
  `IDSpaceAttributesFK` INT NOT NULL,
  `IDSpaceFK` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdSpacePerSpaceAttributes`),
  INDEX `fk_MKSpacesPerSpaceAttributes_MKSpaceAttributes1_idx` (`IDSpaceAttributesFK` ASC) VISIBLE,
  INDEX `fk_MKSpacesPerSpaceAttributes_MKSpaces1_idx` (`IDSpaceFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKSpacesPerSpaceAttributes_MKSpaceAttributes1`
    FOREIGN KEY (`IDSpaceAttributesFK`)
    REFERENCES `Caso1`.`MKSpaceAttributes` (`IdSpaceAttributes`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKSpacesPerSpaceAttributes_MKSpaces1`
    FOREIGN KEY (`IDSpaceFK`)
    REFERENCES `Caso1`.`MKSpaces` (`IdSpace`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKUsersPerMercado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKUsersPerMercado` (
  `IdUsersPerMercado` INT NOT NULL AUTO_INCREMENT,
  `IDMercadoFK` INT NOT NULL,
  `IDUser` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdUsersPerMercado`),
  INDEX `fk_MKUsersPerMercado_MKMercado1_idx` (`IDMercadoFK` ASC) VISIBLE,
  INDEX `fk_MKUsersPerMercado_MKUsers1_idx` (`IDUser` ASC) VISIBLE,
  CONSTRAINT `fk_MKUsersPerMercado_MKMercado1`
    FOREIGN KEY (`IDMercadoFK`)
    REFERENCES `Caso1`.`MKMercado` (`IdMercado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKUsersPerMercado_MKUsers1`
    FOREIGN KEY (`IDUser`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKUsersPerCommerce`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKUsersPerCommerce` (
  `IdUsersPerCommerce` INT NOT NULL AUTO_INCREMENT,
  `IDCommerce` INT NOT NULL,
  `IDUser` INT NOT NULL,
  `IDMercadoPerBuilding` INT NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `updatedAt` DATETIME NOT NULL,
  PRIMARY KEY (`IdUsersPerCommerce`),
  INDEX `fk_MKUsersPerCommerce_MKCommerces1_idx` (`IDCommerce` ASC) VISIBLE,
  INDEX `fk_MKUsersPerCommerce_MKUsers1_idx` (`IDUser` ASC) VISIBLE,
  INDEX `fk_MKUsersPerCommerce_MKMercadoPerBuilding1_idx` (`IDMercadoPerBuilding` ASC) VISIBLE,
  CONSTRAINT `fk_MKUsersPerCommerce_MKCommerces1`
    FOREIGN KEY (`IDCommerce`)
    REFERENCES `Caso1`.`MKCommerces` (`IdCommerce`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKUsersPerCommerce_MKUsers1`
    FOREIGN KEY (`IDUser`)
    REFERENCES `Caso1`.`MKUsers` (`IdUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKUsersPerCommerce_MKMercadoPerBuilding1`
    FOREIGN KEY (`IDMercadoPerBuilding`)
    REFERENCES `Caso1`.`MKMercadoPerBuilding` (`IdMercadoPerBuilding`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Caso1`.`MKCommissionCalculationsDetails`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Caso1`.`MKCommissionCalculationsDetails` (
  `IdCommissionCalculationsDetails` INT NOT NULL AUTO_INCREMENT,
  `IDCommissionCalculationsFK` INT NOT NULL,
  `IDProductFK` INT NOT NULL,
  `IDProductCategoryFK` INT NOT NULL,
  `totalProduct` DECIMAL(10,2) NOT NULL,
  `commissionPercentage` DECIMAL(5,2) NOT NULL,
  `calculatedCommission` DECIMAL(10,2) NOT NULL,
  `calculationDate` DATE NOT NULL,
  `createdAt` DATETIME NOT NULL,
  `notes` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`IdCommissionCalculationsDetails`),
  INDEX `fk_MKCommissionCalculationsDetails_MKCommissionCalculatios1_idx` (`IDCommissionCalculationsFK` ASC) VISIBLE,
  INDEX `fk_MKCommissionCalculationsDetails_MKProducts1_idx` (`IDProductFK` ASC) VISIBLE,
  INDEX `fk_MKCommissionCalculationsDetails_MKProductCategories1_idx` (`IDProductCategoryFK` ASC) VISIBLE,
  CONSTRAINT `fk_MKCommissionCalculationsDetails_MKCommissionCalculatios1`
    FOREIGN KEY (`IDCommissionCalculationsFK`)
    REFERENCES `Caso1`.`MKCommissionCalculatios` (`IdCommissionCalculations`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKCommissionCalculationsDetails_MKProducts1`
    FOREIGN KEY (`IDProductFK`)
    REFERENCES `Caso1`.`MKProducts` (`IdProduct`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MKCommissionCalculationsDetails_MKProductCategories1`
    FOREIGN KEY (`IDProductCategoryFK`)
    REFERENCES `Caso1`.`MKProductCategories` (`IdProductCategory`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
