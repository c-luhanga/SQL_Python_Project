import mysql.connector
from mysql.connector import Error
import datetime
import random

"""
Database Schema for BakeryBase, on which the code below operates

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
   `price` DECIMAL(6,2),
   INDEX `INprice` (price)
);

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
   `qty` int(11) DEFAULT NULL,
   `extPrice` decimal(10,2) DEFAULT NULL,
   PRIMARY KEY (`receiptId`, `lineNum`),
   CONSTRAINT `FKLineItem_receiptId` FOREIGN KEY (`receiptId`)
      REFERENCES `Receipt` (`id`),
   CONSTRAINT `FKLineItem_productId` FOREIGN KEY (`productId`) 
      REFERENCES `Product` (`id`)
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

CREATE TABLE `Lot` (
   `id` INT(11) Primary Key Auto_Increment,
   `productId` VARCHAR(20) NOT NULL,
   `quantity` INT(11) DEFAULT NULL,
   `expirationDate` DATE DEFAULT NULL,
   CONSTRAINT `FKLot_productId` FOREIGN KEY (`productId`) 
      REFERENCES `Product` (`id`)
);

CREATE TABLE `Inventory` (
   `productId` VARCHAR(20) Primary Key,
   `lotSize` INT(11) DEFAULT NULL,
   `currentLotId` INT(11) DEFAULT NULL,
   CONSTRAINT `FKInventory_productId` FOREIGN KEY (`productId`) 
      REFERENCES `Product` (`id`),
   CONSTRAINT `FKInventory_currentLotId` FOREIGN KEY (`currentLotId`) 
      REFERENCES `Lot` (`id`)
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
   ('20-BC-C-10','Chocolate','Cake',8.95),
   ('20-BC-L-10','Lemon','Cake',8.95),
   ('20-CA-7.5','Casino','Cake',15.95),
   ('24-8x10','Opera','Cake',15.95),
   ('25-STR-9','Strawberry','Cake',11.95),
   ('26-8x10','Truffle','Cake',15.95),
   ('45-CH','Chocolate','Eclair',3.25),
   ('45-CO','Coffee','Eclair',3.5),
   ('45-VA','Vanilla','Eclair',3.25),
   ('46-11','Napoleon','Cake',13.49),
   ('90-ALM-I','Almond','Tart',3.75),
   ('90-APIE-10','Apple','Pie',5.25),
   ('90-APP-11','Apple','Tart',3.25),
   ('90-APR-PF','Apricot','Tart',3.25),
   ('90-BER-11','Berry','Tart',3.25),
   ('90-BLK-PF','Blackberry','Tart',3.25),
   ('90-BLU-11','Blueberry','Tart',3.25),
   ('90-CH-PF','Chocolate','Tart',3.75),
   ('90-CHR-11','Cherry','Tart',3.25),
   ('90-LEM-11','Lemon','Tart',3.25),
   ('90-PEC-11','Pecan','Tart',3.75),
   ('70-GA','Ganache','Cookie',1.15),
   ('70-GON','Gongolais','Cookie',1.15),
   ('70-R','Raspberry','Cookie',1.09),
   ('70-LEM','Lemon','Cookie',0.79),
   ('70-M-CH-DZ','Chocolate','Meringue',1.25),
   ('70-M-VA-SM-DZ','Vanilla','Meringue',1.15),
   ('70-MAR','Marzipan','Cookie',1.25),
   ('70-TU','Tuile','Cookie',1.25),
   ('70-W','Walnut','Cookie',0.79),
   ('50-ALM','Almond','Croissant',1.45),
   ('50-APP','Apple','Croissant',1.45),
   ('50-APR','Apricot','Croissant',1.45),
   ('50-CHS','Cheese','Croissant',1.75),
   ('50-CH','Chocolate','Croissant',1.75),
   ('51-APR','Apricot','Danish',1.15),
   ('51-APP','Apple','Danish',1.15),
   ('51-ATW','Almond','Twist',1.15),
   ('51-BC','Almond','Bear Claw',1.95),
   ('51-BLU','Blueberry','Danish',1.15);

"""

# Example Code saved from the original generated code
def sampleQueries(connection):
    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Example Query 1: SELECT query
    cursor.execute("SELECT * FROM Customer LIMIT 5")

    # Fetching the results
    print("Results from SELECT query:")
    for row in cursor.fetchall():
        print(row)

    # Example Query 2: INSERT query as prepared statement
    # Do NOT use string formatting to insert data into query, e.g.
    # insert_query = f"INSERT INTO your_table (column1, column2) VALUES
    # ('{value1}', '{value2}')"
    prep_stmt = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
    data = ('value1', 'value2')
    cursor.execute(prep_stmt, data)
    connection.commit()

    # Commit the transaction
    connection.commit()
    print("Data inserted successfully")

"""
Customer class represents a customer in the bakery database. The customer's behavior is modeled by the following attributes:
*Likelihood of purchase per day 
* min/max number of product purchased per receipt
* Min/max repeats per product 
* liklihood of a review per day 
*pick random product they just purchased and review if not already reviewed. Random score with standard comment
""" 
class Customer:
   def __init__(self, lastName, firstName, purchaseProb, minProd, maxProd, minRepeat, 
   maxRepeat, reviewProb, age, street, city, state):
      self.lastName = lastName
      self.firstName = firstName
      self.purchaseProb = purchaseProb
      self.minProd = minProd
      self.maxProd = maxProd
      self.minRepeat = minRepeat
      self.maxRepeat = maxRepeat
      self.reviewProb = reviewProb
      self.favorites = []
      self.lastVisit = None
      self.age = age
      self.street = street
      self.city = city
      self.state = state


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
   # and a min/max range of how many of each product they'll buy. Finally, they have a probability of reviewing each product on their 
   # receipt. For each customer, generate a day's activity thus:

   def do_one_day(self, connection, date, products, rng):
        cursor = connection.cursor()

        # Check if the customer will make a purchase today
        if rng.random() <= self.purchaseProb:
            # Generate a receipt
            cursor.execute("INSERT INTO Receipt (customerId, date) VALUES (%s, %s)", (self.id, date))
            receiptID = cursor.lastrowid

            # Determine the number of products to purchase
            num_products = rng.randint(self.minProducts, self.maxProducts)

            for _ in range(num_products):
                # Choose a random product ID and quantity
                product_id = rng.choice(products)
                quantity = rng.randint(self.minQuantity, self.maxQuantity)

                # Calculate the extended price (assuming price is fetched from the Product table)
                cursor.execute("SELECT price FROM Product WHERE id = %s", (product_id,))
                price = cursor.fetchone()[0]
                extended_price = price * quantity

                # Add line item to the receipt
                cursor.execute(
                    "INSERT INTO LineItem (receiptId, productId, quantity, extendedPrice) VALUES (%s, %s, %s, %s)",
                    (receiptID, product_id, quantity, extended_price)
                )

                # Update the current Lot for the product (assuming a Lot table exists)
                cursor.execute(
                    "UPDATE Lot SET quantity = quantity - %s WHERE productId = %s AND quantity >= %s LIMIT 1",
                    (quantity, product_id, quantity)
                )
                if cursor.rowcount == 0:
                    # If no lot has enough quantity, create a new lot (assuming default values for new lots)
                    cursor.execute(
                        "INSERT INTO Lot (productId, quantity) VALUES (%s, %s)",
                        (product_id, quantity)
                    )

                # Review the product
                if rng.random() <= self.reviewProb:
                    cursor.execute(
                        "INSERT INTO Review (customerId, productId, date) VALUES (%s, %s, %s)",
                        (self.id, product_id, date)
                    )

            connection.commit()

   #taking connection, startDate, endDate, customers, products as arguments write a function to run the simulation for a number of days
   #for each customer, call doOneDay for each day in the range.
   def runSimulation(connection, startDate, endDate, customers, products):
      rng = random.Random()
      rng.seed(100)
      delta = datetime.timedelta(days=1)
      date = startDate
      while date <= endDate:
         for c in customers:
            if rng.random() < c.purchaseProb:
               c.doOneDay(connection, date, products, rng)
            if rng.random() < c.reviewProb:
               c.doReview(connection, products, rng)
         date += delta

   #Write a function to print the top 5 customers by total spending
   def topCustomers(connection):
      cursor = connection.cursor()
      cursor.execute("SELECT c.id, c.lastName, c.firstName, SUM(li.extPrice) AS totalSpending FROM Customer c JOIN Receipt r ON c.id = r.customerId JOIN LineItem li ON r.id = li.receiptId GROUP BY c.id ORDER BY totalSpending DESC LIMIT 5")
      print("Top 5 customers by total spending:")
      for row in cursor.fetchall():
         print(row)

   #Write a function to: 
   # 1. Create Kind and Flavor tables, populating them from Kind and Flavor values in Product
   #2. Replace the Product.kind and Product.flavor fields with FK links to Kind and Flavor
   #3. Add a CustomerXFlavor join table, and a CustomerXKind join table
   #4. Fetch the favorites from the customer. Break this string up into a list of flavors and a list of kinds.  For each flavor and kind, *if* it is among the flavors and kinds in the database, add a row to the
   #appropriate join table. Otherwise, report the missing flavor or kind. Drop Customer.favorites.
   def normalize(connection):
       cursor = connection.cursor()
       cursor.execute("CREATE TABLE Kind (id INT(11) PRIMARY KEY AUTO_INCREMENT, kind VARCHAR(30))")
       cursor.execute("CREATE TABLE Flavor (id INT(11) PRIMARY KEY AUTO_INCREMENT, flavor VARCHAR(30))")
       cursor.execute("SELECT DISTINCT kind FROM Product")
       for row in cursor.fetchall():
           cursor.execute("INSERT INTO Kind (kind) VALUES (%s)", (row[0],))
       cursor.execute("SELECT DISTINCT flavor FROM Product")
       for row in cursor.fetchall():
           cursor.execute("INSERT INTO Flavor (flavor) VALUES (%s)", (row[0],))
       
       # Add missing values to Flavor and Kind tables
       missing_flavors = ["Carrot", "Appl", "Cassino", "Strawberry Twist"]
       for flavor in missing_flavors:
           cursor.execute("INSERT INTO Flavor (flavor) VALUES (%s)", (flavor,))
       
       cursor.execute("ALTER TABLE Product ADD COLUMN kindId INT(11)")
       cursor.execute("ALTER TABLE Product ADD COLUMN flavorId INT(11)")
       cursor.execute("UPDATE Product p JOIN Kind k ON p.kind = k.kind SET p.kindId = k.id")
       cursor.execute("UPDATE Product p JOIN Flavor f ON p.flavor = f.flavor SET p.flavorId = f.id")
       cursor.execute("CREATE TABLE CustomerXFlavor (customerId INT(11), flavorId INT(11), PRIMARY KEY (customerId, flavorId))")
       cursor.execute("CREATE TABLE CustomerXKind (customerId INT(11), kindId INT(11), PRIMARY KEY (customerId, kindId))")
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
       cursor.execute("ALTER TABLE Customer DROP COLUMN favorites")
       connection.commit()

   #5. Add columns lotSize and currentLotId to Product. Set first to random value between 50 and 100. Set second to NULL. Each product will have a current "lot" -- an inventory of that product. As lots are consumed (or if none exists when a product is bought), a new lot is created and drawn from.
   def addInventory(connection):
      cursor = connection.cursor()
      cursor.execute("ALTER TABLE Product ADD COLUMN lotSize INT(11)")
      cursor.execute("ALTER TABLE Product ADD COLUMN currentLotId INT(11)")
      cursor.execute("SELECT id FROM Product")
      for row in cursor.fetchall():
         lotSize = random.randint(50, 100)
         cursor.execute("UPDATE Product SET lotSize = %s, currentLotId = NULL WHERE id = %s", (lotSize, row[0]))
      connection.commit()

   # Generate more random customers, who will do automated purchasing. Each has first/last and age specifically wired into the code, but street, city, and state randomly chosen from small sets of standard street names, with random street number, random city names, and perhaps a dozen representative US states.

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
   try:
      # Establish the connection
      connection = mysql.connector.connect(
         host='localhost',
         database='BakeryBase',
         user='root',
         password='Th1s1smydatabase'
      )

      if not connection.is_connected():
         raise Exception(f"Failed to connect to database")
      print(f"Connected to {connection.get_server_info()} as {connection.user}")


      # create a list of 20 customers
      """customers = [
         Customer("Smith", "John", 0.5, 1, 3, 1, 5, 0.1, 30, "123 Main St", "Chicago", "IL"),
         Customer("Johnson", "Jane", 0.75, 1, 3, 1, 5, 0.1, 25, "456 Elm St", "Kansas City", "MO"),
         Customer("Davis", "Sam", 0.25, 1, 3, 1, 5, 0.1, 40, "789 Oak St", "Houston", "TX"),
         Customer("Wilson", "Mary", 0.9, 1, 3, 1, 5, 0.1, 35, "101 Pine St", "Los Angeles", "CA"),
         Customer("Moore", "Sue", 0.8, 1, 3, 1, 5, 0.1, 28, "202 Maple St", "New York", "NY"),
         Customer("Taylor", "Tom", 0.3, 1, 3, 1, 5, 0.1, 32, "303 Birch St", "Miami", "FL"),
         Customer("Anderson", "Ann", 0.6, 1, 3, 1, 5, 0.1, 27, "404 Cedar St", "Columbus", "OH"),
         Customer("Thomas", "Tim", 0.4, 1, 3, 1, 5, 0.1, 45, "505 Walnut St", "Philadelphia", "PA"),
         Customer("Harris", "Holly", 0.7, 1, 3, 1, 5, 0.1, 33, "606 Chestnut St", "Atlanta", "GA"),
      ]"""



      # add customers generated to the database
      customers = Customer.generateCustomers()
      for c in customers:
         c.insert(connection)
      print("Customers inserted successfully")
      

      # Commit the transaction
      connection.commit()
      print("Data inserted successfully")

      # lets normalize the database and add inventory only once check if the tables are already created
      cursor = connection.cursor()
      cursor.execute("SHOW TABLES")
      tables = cursor.fetchall()
      if ("Kind",) not in tables:
         Customer.normalize(connection)
         print("Database normalized successfully")
      if ("lotSize",) not in tables:
         Customer.addInventory(connection)
         print("Inventory added successfully")
      print("Data is already normalized and inventory is already added")
      

      # Get the list of customers from the database
      cursor = connection.cursor()

      
   except Error as e:
      print(f"Error: {e}")

   finally:
      # Close the cursor and connection
      if connection.is_connected():
         connection.close()
         print("MySQL connection closed")

if __name__ == "__main__":
   main()