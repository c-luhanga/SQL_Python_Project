DROP DATABASE IF EXISTS BakeryBase;
CREATE DATABASE BakeryBase;
USE BakeryBase;

/* Schema */

CREATE TABLE `Customer` (
   `id` INT(11) PRIMARY KEY Auto_Increment,
   `lastName` VARCHAR(30) NOT NULL,
   `firstName` VARCHAR(30) DEFAULT NULL,
   `age` INT(11) DEFAULT NULL,
   `gender` CHAR(1) DEFAULT NULL,
   `street` VARCHAR(50) DEFAULT NULL,
   `city` VARCHAR(50) DEFAULT NULL,
   `state` CHAR(2) DEFAULT NULL,
   `favorites` VARCHAR(255) DEFAULT NULL,
   `lastVisit` DATE DEFAULT NULL
);

CREATE TABLE `Product` (
   `id` VARCHAR(20) Primary Key,
   `flavor` VARCHAR(30) DEFAULT NULL,
   `kind` VARCHAR(30) DEFAULT NULL,
   `price` DECIMAL(6,2) NOT NULL,
   `lotSize` INT(11) DEFAULT NULL,
   `currentLotId` INT(11) DEFAULT NULL,
   INDEX `INprice` (price)
);

CREATE TABLE `Lot` (
   `id` INT(11) Primary Key Auto_Increment,
   `productId` VARCHAR(20) NOT NULL,
   `quantity` INT(11) DEFAULT NULL,
   `expirationDate` DATE DEFAULT NULL,
   CONSTRAINT `FKLot_productId` FOREIGN KEY (`productId`) 
      REFERENCES `Product` (`id`)
);

alter table Product
   ADD CONSTRAINT `FKProduct_currentLotId` FOREIGN KEY (`currentLotId`) 
      REFERENCES `Lot` (`id`);

CREATE TABLE `Receipt` (
   `id` INT(11) PRIMARY KEY AUTO_INCREMENT,
   `purchaseDate` DATE DEFAULT NULL,
   `customerId` INT(11) NOT NULL,
   `total` DECIMAL(10,2) DEFAULT NULL,
   CONSTRAINT `FKReceipt_customerId` FOREIGN KEY (`customerId`)
      REFERENCES `Customer` (`id`)
);

/* New LineItem */
CREATE TABLE `LineItem` (
   `receiptId` INT(11) NOT NULL,
   `lineNum` INT(11) NOT NULL DEFAULT 1,
   `productId` VARCHAR(20) NOT NULL,
   `lotId` INT(11) DEFAULT NULL,
   `qty` int(11) DEFAULT NULL,
   `extPrice` decimal(10,2) DEFAULT NULL,
   PRIMARY KEY (`receiptId`, `lineNum`),
   CONSTRAINT `FKLineItem_receiptId` FOREIGN KEY (`receiptId`)
      REFERENCES `Receipt` (`id`),
   CONSTRAINT `FKLineItem_productId` FOREIGN KEY (`productId`) 
      REFERENCES `Product` (`id`),
   CONSTRAINT `FKLineItem_lotId` FOREIGN KEY (`lotId`) 
      REFERENCES `Lot` (`id`)
);

CREATE TABLE `Rating` (
   `customerId` INT(11) DEFAULT NULL,
   `productId` VARCHAR(20) NOT NULL,
   `score` INT(11) DEFAULT NULL,
   `comment` VARCHAR(1024) DEFAULT NULL,
   UNIQUE KEY UKcustomerId_productId (customerId, productId),
   CONSTRAINT `FKRating_customerId` FOREIGN KEY (`customerId`) 
      REFERENCES `Customer` (`id`),
   CONSTRAINT `FKRating_productId` FOREIGN KEY (`productId`) 
      REFERENCES `Product` (`id`)
);

CREATE TABLE `Discount` (
   `id` INT(11) PRIMARY KEY AUTO_INCREMENT,
   `startDate` DATE DEFAULT NULL,
   `endDate` DATE DEFAULT NULL,
   `percentOff` INT(11) NOT NULL
);

CREATE TABLE `DiscountXProduct` (
   `discountId` INT(11) NOT NULL,
   `productId` VARCHAR(20) NOT NULL,
   CONSTRAINT `FKDiscountXProduct_discountId` FOREIGN KEY (`discountId`) 
      REFERENCES `Discount` (`id`),
   CONSTRAINT `FKDiscountXProduct_productId` FOREIGN KEY (`productId`) 
      REFERENCES `Product` (`id`)
);

INSERT INTO `Customer` VALUES
   (1,'Logan','Juliet', 17, 'F', '402 Paradise Rd', 'Harrisburg', 'OR', 'Napoleon, Carrot, Cake', '2008-12-23'),
   (2,'Arzt','Terrell', 18, 'M', '8101 72nd Ave', 'Phoenix', 'AZ', 'Apricot, Strawberry, Cookie', '2013-11-02'),
   (3,'Esposita','Travis', 87, 'M', '1819 Monument Way', 'Walnut Creek', 'CA', 'Cheese, Strawberry, Cake', '2013-01-13'),
   (4,'Engley','Sixta', 18, 'F', '192 Lexington St', 'Fort Pierce', 'FL', 'Truffle, Eclair', '2012-01-13'),
   (5,'Dunlow','Travis', 13, 'M', '6500 Filbert Ct', 'Campbell', 'OH', 'Chocolate, Bear Claw', '2009-02-02'),
   (6,'Slingland','Josette', 14, 'F', '333 Park Ave', 'Santa Rosa', 'CA', 'Lemon, Tart', '2010-09-20'),
   (7,'Toussand','Sharron', 77, 'F', '2581 Crystal Lake Dr', 'Cedar City', 'UT', 'Lemon, Tart', '2012-07-25'),
   (8,'Esposita','Rupert', 65, 'M', '4531 Westray Dr', 'Orange', 'CA', 'Blackberry, Cookie', '2013-03-08'),
   (9,'Hafferkamp','Cuc', 46, 'F', '2832 Amerson Way', 'Bend', 'OR', 'Vanilla, Appl, Blueberry, Cake', '2013-09-18'),
   (10,'Dukelow','Coretta', 78, 'F', '314 Pecan St', 'Eugene', 'OR', 'Almond, Croissant', '2011-05-09'),
   (11,'Stadick','Migdalia', 16, 'F', '24816 20Th Ave', 'Bellevue', 'WA', 'Chocolate, Cake', '2011-05-22'),
   (12,'McMahan','Mellie', 65, 'F', '90 Creekside Dr', 'Redmond', 'WA', 'Vanilla, Cassino, Strawberry Twist', '2012-10-19'),
   (13,'Arnn','Kip', 28, 'M', '1654 Pine Valley Dr', 'Hilo', 'HI', 'Casino, Danish', '2013-09-30'),
   (14,'Sopko','Rayford', 64, 'M', '148 Blackburn St', 'Rock Springs', 'WY', 'Casino, Opera, Croissant, Twist', '2012-02-24'),
   (15,'Callendar','David', 67, 'M', '27 Mildred Rd', 'Sterling', 'AK', 'Chocolate, Berry, Cake', '2012-03-01'),
   (16,'Cruzen','Ariane', 17, 'F', '700 Midland Ave', 'Fulton', 'NY', 'Pecan, Berry, Danish, Strawberry, Meringue', '2011-01-06'),
   (17,'Mesdaq','Charlene', 17, 'F', '650 Spruce St', 'Fulton', 'NY', 'Almond, Strawberry, Cookie', '2013-01-01'),
   (18,'Domkowski','Almeta', 15, 'F', '11 Philadelphia St', 'Providence', 'RI', 'Strawberry, Coffee, Cookie', '2012-12-31'),
   (19,'Stenz','Natacha', 34, 'F', '30 Bank St', 'Chico', 'CA', 'Berry, Apple, Chocolate, Pie, Tart', '2013-12-29'),
   (20,'Zeme','Stephen', 18, 'M', '3133 Maple Ct', 'Walnut Creek', 'CA', 'Lemon, Pecan, Tart, Eclair', '2012-03-04'),
   (21,'Cheap', 'Joe', 20, 'M', '123 Skinflint Dr', 'Fulton', 'CA', '', NULL);

INSERT INTO `Product` VALUES
   ('20-BC-C-10','Chocolate','Cake',8.95, 30, NULL),
   ('20-BC-L-10','Lemon','Cake',8.95, 40, NULL),
   ('20-CA-7.5','Casino','Cake',15.95, 50, NULL),
   ('24-8x10','Opera','Cake',15.95, 50, NULL),
   ('25-STR-9','Strawberry','Cake',11.95, 50, NULL),
   ('26-8x10','Truffle','Cake',15.95, 40, NULL),
   ('45-CH','Chocolate','Eclair',3.25, 50, NULL),
   ('45-CO','Coffee','Eclair',3.5, 50, NULL),
   ('45-VA','Vanilla','Eclair',3.25, 50, NULL),
   ('46-11','Napoleon','Cake',13.49, 50, NULL),
   ('90-ALM-I','Almond','Tart',3.75, 50, NULL),
   ('90-APIE-10','Apple','Pie',5.25, 50, NULL),
   ('90-APP-11','Apple','Tart',3.25, 50, NULL),
   ('90-APR-PF','Apricot','Tart',3.25, 50, NULL),
   ('90-BER-11','Berry','Tart',3.25, 50, NULL),
   ('90-BLK-PF','Blackberry','Tart',3.25, 50, NULL),
   ('90-BLU-11','Blueberry','Tart',3.25, 50, NULL),
   ('90-CH-PF','Chocolate','Tart',3.75, 50, NULL),
   ('90-CHR-11','Cherry','Tart',3.25, 50, NULL),
   ('90-LEM-11','Lemon','Tart',3.25, 50, NULL),
   ('90-PEC-11','Pecan','Tart',3.75, 50, NULL),
   ('70-GA','Ganache','Cookie',1.15, 50, NULL),
   ('70-GON','Gongolais','Cookie',1.15, 50, NULL),
   ('70-R','Raspberry','Cookie',1.09, 50, NULL),
   ('70-LEM','Lemon','Cookie',0.79, 50, NULL),
   ('70-M-CH-DZ','Chocolate','Meringue',1.25, 50, NULL),
   ('70-M-VA-SM-DZ','Vanilla','Meringue',1.15, 50, NULL),
   ('70-MAR','Marzipan','Cookie',1.25, 50, NULL),
   ('70-TU','Tuile','Cookie',1.25, 50, NULL),
   ('70-W','Walnut','Cookie',0.79, 50, NULL),
   ('50-ALM','Almond','Croissant',1.45, 50, NULL),
   ('50-APP','Apple','Croissant',1.45, 50, NULL),
   ('50-APR','Apricot','Croissant',1.45, 50, NULL),
   ('50-CHS','Cheese','Croissant',1.75, 50, NULL),
   ('50-CH','Chocolate','Croissant',1.75, 50, NULL),
   ('51-APR','Apricot','Danish',1.15, 50, NULL),
   ('51-APP','Apple','Danish',1.15, 50, NULL),
   ('51-ATW','Almond','Twist',1.15, 50, NULL),
   ('51-BC','Almond','Bear Claw',1.95, 50, NULL),
   ('51-BLU','Blueberry','Danish',1.15, 30, NULL);
