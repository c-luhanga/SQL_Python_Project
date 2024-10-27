import argparse
from datetime import datetime, timedelta
import random
import mysql.connector

"""
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

"""

"""
Customer class represents a customer in the bakery database. The customer's behavior is modeled by the following attributes:
*Likelihood of purchase per day 
* min/max number of product purchased per receipt
* Min/max repeats per product 
* liklihood of a review per day 
*pick random product they just purchased and review if not already reviewed. Random score with standard comment
""" 
class Customer:
   def __init__(self, lastName, firstName, purchaseProb, minProducts, maxProducts, minQuantity, maxQuantity, reviewProb, age, street, city, state):
        self.lastName = lastName
        self.firstName = firstName
        self.purchaseProb = purchaseProb
        self.minProducts = minProducts
        self.maxProducts = maxProducts
        self.minQuantity = minQuantity
        self.maxQuantity = maxQuantity
        self.reviewProb = reviewProb
        self.age = age
        self.street = street
        self.city = city
        self.state = state

   def parse_arguments():
      parser = argparse.ArgumentParser(description="Run a full simulation.")
      parser.add_argument("start_date", type=str, help="Start date in YYYY-MM-DD format")
      parser.add_argument("end_date", type=str, help="End date in YYYY-MM-DD format")
      return parser.parse_args()
   

   # insert a new customer into the database
   def insert(self, connection):
      cursor = connection.cursor()
      insert_stmt = "INSERT INTO Customer (lastName, firstName, age, street, city, state) VALUES (%s, %s, %s, %s, %s, %s)"
      data = (self.lastName, self.firstName, self.age, self.street, self.city, self.state)
      cursor.execute(insert_stmt, data)
      connection.commit()
      self.id = cursor.lastrowid

   
   def getProducts(connection):
      cursor = connection.cursor()
      cursor.execute("SELECT id, price FROM Product")
      return cursor.fetchall()

   #write a add Receipt method that will add a receipt to the database for the customer with the given date. It returns the receipt ID
   def addReceipt(connection, date):
      cursor = connection.cursor()
      insert_stmt = "INSERT INTO Receipt (purchaseDate, customerId) VALUES (%s, %s)"
      data = (date, self.id)
      cursor.execute(insert_stmt, data)
      connection.commit()
      return cursor.lastrowid
   
   def initialize_inventory(connection):
    cursor = connection.cursor()

    # Fetch all products from the Product table
    cursor.execute("SELECT id, lotSize FROM Product")
    products = cursor.fetchall()

    for product in products:
        product_id, lot_size = product

        # Create an initial lot for each product
        cursor.execute(
            "INSERT INTO Lot (productId, quantity, expirationDate) VALUES (%s, %s, DATE_ADD(CURDATE(), INTERVAL 5 DAY))",
            (product_id, lot_size)
        )
        lot_id = cursor.lastrowid

        # Update the Product table with the current lot ID
        cursor.execute(
            "UPDATE Product SET currentLotId = %s WHERE id = %s",
            (lot_id, product_id)
        )

    # Commit the transaction
    connection.commit()
    print("Inventory initialized successfully")

   #write a addLineItem method that will add a line item to the database for the given receipt ID, product ID, quantity, and extended price
   def addLineItem(connection, receiptId, productId, qty, extPrice):
      cursor = connection.cursor()
      insert_stmt = "INSERT INTO LineItem (receiptId, productId, qty, extPrice) VALUES (%s, %s, %s, %s)"
      data = (receiptId, productId, qty, extPrice)
      cursor.execute(insert_stmt, data)
      connection.commit()

   #write a do one day method that will simulate a customer's behavior for one day. it gerates a recipet for the customer
   #with likelihood, and adds the receipt to the database, with the given date. It obtains the recieptID and uses it to add a random
   # number of line items to the receipt, choosing products IDs from "products" list. Each product id in turn has a random quantity
   # quantity count count and associated extened price.
   # Paraeters are: connection, date, products, random number generator
   #Each customer also has a per-day likelihood of making a purchase, a min/max range of the number of products they'll randomly purchase, 
   # and a min/max range of how many of`` each product they'll buy. Finally, they have a probability of reviewing each product on their 
   # receipt. For each customer, generate a day's activity thus:

   def do_one_day(self, connection, date, products, rng):
    cursor = connection.cursor()
    
    # Check if the customer will make a purchase today
    if rng.random() <= self.purchaseProb:
        # Generate a receipt
        cursor.execute("INSERT INTO Receipt (customerId, purchaseDate) VALUES (%s, %s)", (self.id, date))
        receiptID = cursor.lastrowid

        # Update the lastVisit column in the Customer table
        cursor.execute("UPDATE Customer SET lastVisit = %s WHERE id = %s", (date, self.id))

        # Determine the number of products to purchase
        num_products = rng.randint(self.minProducts, self.maxProducts) if self.minProducts < self.maxProducts else self.minProducts

        line_num = 1  # Line number for the line items
        total_amount = 0  # Initialize total amount for the receipt

        for _ in range(num_products):
            # Choose a random product ID and quantity
            product_id = rng.choice(products)
            quantity = rng.randint(self.minQuantity, self.maxQuantity) if self.minQuantity < self.maxQuantity else self.minQuantity

            # Calculate the extended price (assuming price is fetched from the Product table)
            cursor.execute("SELECT price, lotSize FROM Product WHERE id = %s", (product_id,))
            product_info = cursor.fetchone()
            price, lot_size = product_info[0], product_info[1]
            extended_price = price * quantity
            total_amount += extended_price  # Add to total amount

            # Track remaining quantity to fulfill
            remaining_quantity = quantity
            line_item_lots = []  # To store (lot_id, quantity) pairs for line item entry

            # Fetch available lots in order for the selected product
            cursor.execute("SELECT id, quantity FROM Lot WHERE productId = %s AND quantity > 0 ORDER BY id", (product_id,))
            lots = cursor.fetchall()
            
            for lot in lots:
                lot_id, lot_quantity = lot
                if remaining_quantity <= lot_quantity:
                    # If the lot has enough quantity to fulfill the remaining quantity
                    line_item_lots.append((lot_id, remaining_quantity))
                    cursor.execute("UPDATE Lot SET quantity = quantity - %s WHERE id = %s", (remaining_quantity, lot_id))
                    remaining_quantity = 0  # Order fulfilled
                    break
                else:
                    # Use the entire lot quantity and continue to the next lot
                    line_item_lots.append((lot_id, lot_quantity))
                    remaining_quantity -= lot_quantity
                    cursor.execute("UPDATE Lot SET quantity = 0 WHERE id = %s", (lot_id,))

            # If there's still remaining quantity, create a new lot
            if remaining_quantity > 0:
                cursor.execute(
                    "INSERT INTO Lot (productId, quantity, expirationDate) VALUES (%s, %s, DATE_ADD(%s, INTERVAL 5 DAY))",
                    (product_id, lot_size, date)
                )
                new_lot_id = cursor.lastrowid
                cursor.execute("UPDATE Product SET currentLotId = %s WHERE id = %s", (new_lot_id, product_id))
                
                # Fulfill the remaining quantity from the new lot
                line_item_lots.append((new_lot_id, remaining_quantity))
                cursor.execute("UPDATE Lot SET quantity = quantity - %s WHERE id = %s", (remaining_quantity, new_lot_id))

            # Insert line items for each lot used in this transaction
            for lot_id, qty in line_item_lots:
                cursor.execute(
                    "INSERT INTO LineItem (receiptId, lineNum, productId, lotId, qty, extPrice) VALUES (%s, %s, %s, %s, %s, %s)",
                    (receiptID, line_num, product_id, lot_id, qty, price * qty)
                )
                line_num += 1

            # Review the product
            if rng.random() <= self.reviewProb:
                cursor.execute("SELECT 1 FROM Rating WHERE customerId = %s AND productId = %s", (self.id, product_id))
                if cursor.fetchone() is None:  # No existing review
                    score = rng.randint(1, 5)  # Random score between 1 and 5
                    comment = "This is a standard review comment."
                    cursor.execute(
                        "INSERT INTO Rating (customerId, productId, score, comment) VALUES (%s, %s, %s, %s)",
                        (self.id, product_id, score, comment)
                    )

        # Update the total amount in the receipt
        cursor.execute("UPDATE Receipt SET total = %s WHERE id = %s", (total_amount, receiptID))

        # Commit transaction for this day's purchases
        connection.commit()

   #taking connection, startDate, endDate, customers, products as arguments write a function to run the simulation for a number of days
   #for each customer, call doOneDay for each day in the range.

   def run_simulation(connection, start_date, end_date, customers, products):
    rng = random.Random()
    current_date = start_date

    while current_date <= end_date:
        for customer in customers:
                customer.do_one_day(connection, current_date, products, rng)

        # Advance to the next day
        current_date += timedelta(days=1)
    
    # print number of lines in the LineItem table
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM LineItem")
    count = cursor.fetchone()[0]
    print(f"Number of line items: {count}")

   #Write a function to: 
   # 1. Create Kind and Flavor tables, populating them from Kind and Flavor values in Product
   #2. Replace the Product.kind and Product.flavor fields with FK links to Kind and Flavor
   #3. Add a CustomerXFlavor join table, and a CustomerXKind join table
   #4. Fetch the favorites from the customer. Break this string up into a list of flavors and a list of kinds.  For each flavor and kind, *if* it is among the flavors and kinds in the database, add a row to the
   #appropriate join table. Otherwise, report the missing flavor or kind. Drop Customer.favorites.
   def normalize(connection):
        cursor = connection.cursor()
        
        # Create Kind and Flavor tables
        cursor.execute("CREATE TABLE Kind (id INT(11) PRIMARY KEY AUTO_INCREMENT, kind VARCHAR(30))")
        cursor.execute("CREATE TABLE Flavor (id INT(11) PRIMARY KEY AUTO_INCREMENT, flavor VARCHAR(30))")
        
        # Populate Kind and Flavor tables from Product
        cursor.execute("SELECT DISTINCT kind FROM Product")
        for row in cursor.fetchall():
            cursor.execute("INSERT INTO Kind (kind) VALUES (%s)", (row[0],))
        cursor.execute("SELECT DISTINCT flavor FROM Product")
        for row in cursor.fetchall():
            cursor.execute("INSERT INTO Flavor (flavor) VALUES (%s)", (row[0],))
        
        # Replace Product.kind and Product.flavor with FK links to Kind and Flavor
        cursor.execute("ALTER TABLE Product ADD COLUMN kindId INT(11)")
        cursor.execute("ALTER TABLE Product ADD COLUMN flavorId INT(11)")
        cursor.execute("UPDATE Product p JOIN Kind k ON p.kind = k.kind SET p.kindId = k.id")
        cursor.execute("UPDATE Product p JOIN Flavor f ON p.flavor = f.flavor SET p.flavorId = f.id")
        
        # Add CustomerXFlavor and CustomerXKind join tables
        cursor.execute("CREATE TABLE CustomerXFlavor (customerId INT(11), flavorId INT(11), PRIMARY KEY (customerId, flavorId))")
        cursor.execute("CREATE TABLE CustomerXKind (customerId INT(11), kindId INT(11), PRIMARY KEY (customerId, kindId))")
        
        # Fetch favorites from Customer and populate join tables
        cursor.execute("SELECT id, favorites FROM Customer")
        for row in cursor.fetchall():
            customerId = row[0]
            favs = row[1]
            if favs:
                fav_list = favs.split(", ")
                for fav in fav_list:
                    cursor.execute("SELECT id FROM Flavor WHERE flavor = %s", (fav,))
                    result = cursor.fetchone()
                    if result:
                        cursor.execute("INSERT INTO CustomerXFlavor (customerId, flavorId) VALUES (%s, %s)", (customerId, result[0]))
                    else:
                        cursor.execute("SELECT id FROM Kind WHERE kind = %s", (fav,))
                        result = cursor.fetchone()
                        if result:
                            cursor.execute("INSERT INTO CustomerXKind (customerId, kindId) VALUES (%s, %s)", (customerId, result[0]))
                        else:
                            print(f"Flavor or Kind {fav} not found in database")
        
        # Drop Customer.favorites column
        cursor.execute("ALTER TABLE Customer DROP COLUMN favorites")
        connection.commit()
    
   # Generate more random customers, who will do automated purchasing. Each has first/last and age specifically wired into the code, but street, city, 
   # and state randomly chosen from small sets of standard street names, with random street number, random city names, and perhaps a dozen representative US states.
   def generateCustomers():
      customers = []
      for i in range(20):
         lastName = random.choice(["Smith", "Johnson", "Davis", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Harris"])
         firstName = random.choice(["John", "Jane", "Sam", "Mary", "Sue", "Tom", "Ann", "Tim", "Holly"])
         purchaseProb = random.uniform(0.1, 0.9)
         minProd = random.randint(1, 3)
         maxProd = random.randint(1, 3)
         minRepeat = random.randint(1, 5)
         maxRepeat = random.randint(1, 5)
         reviewProb = random.uniform(0.1, 0.9)
         age = random.randint(25, 75)
         street = f"{random.randint(100, 999)} {random.choice(['Main', 'Elm', 'Oak', 'Pine', 'Maple', 'Birch', 'Cedar', 'Walnut', 'Chestnut'])} St"
         city = random.choice(["Chicago", "Kansas City", "Houston", "Los Angeles", "New York", "Miami", "Columbus", "Philadelphia", "Atlanta"])
         state = random.choice(["IL", "MO", "TX", "CA", "NY", "FL", "OH", "PA", "GA"])
         customers.append(Customer(lastName, firstName, purchaseProb, minProd, maxProd, minRepeat, maxRepeat, reviewProb, age, street, city, state))
      return customers


def main():
   args = Customer.parse_arguments()
   start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
   end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
   try:
        # Establish the connection
        connection = mysql.connector.connect(
            host='localhost',
            database='BakeryBase',
            user='cLuhanga',
            password='nofunnystuff123'
        )

        if not connection.is_connected():
            raise Exception(f"Failed to connect to database")
        print(f"Connected to {connection.get_server_info()} as {connection.user}")

        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        
        # Normalize the database
        Customer.normalize(connection)
        print("Database normalized successfully")
        
        # Add customers generated to the database
        customers = Customer.generateCustomers()
        for c in customers:
            c.insert(connection)
        print("Customers inserted successfully")

        # Print the number of customers in the database
        cursor.execute("SELECT COUNT(*) FROM Customer")
        count = cursor.fetchone()[0]
        print(f"Number of customers: {count}")

        # Fetch products from the database
        cursor.execute("SELECT id FROM Product")
        products = [row[0] for row in cursor.fetchall()]

        # Initialize the inventory
        Customer.initialize_inventory(connection)
        
        # Run the simulation
        Customer.run_simulation(connection, start_date, end_date, customers, products)
        # Commit the transaction
        connection.commit()

   except mysql.connector.Error as e:
        print(f"Error: {e}")

   finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    main()