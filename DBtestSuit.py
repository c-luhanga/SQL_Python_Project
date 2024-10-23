import unittest
import mysql.connector
from PythonDBExample import Customer, main

class TestPythonDBExample(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Establish the connection
        cls.connection = mysql.connector.connect(
            host='localhost',
            database='BakeryBase',
            user='root',
            password='Th1s1smydatabase'
        )
        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(cls):
        # Close the cursor and connection
        if cls.connection.is_connected():
            cls.cursor.close()
            cls.connection.close()

    def setUp(self):
        # Start a transaction
        self.connection.start_transaction()

    def tearDown(self):
        # Rollback the transaction
        self.connection.rollback()

    def test_generate_customers(self):
        customers = Customer.generateCustomers()
        self.assertTrue(len(customers) > 0, "No customers generated")

    def test_insert_customer(self):
        customer = Customer(1, 0.5, 1, 5, 1, 3, 0.2)
        customer.insert(self.connection)
        self.cursor.execute("SELECT * FROM Customer WHERE id = %s", (customer.id,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Customer not inserted")

    def test_normalize(self):
        Customer.normalize(self.connection)
        self.cursor.execute("SHOW TABLES LIKE 'Kind'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Table 'Kind' not created")

    def test_add_inventory(self):
        Customer.addInventory(self.connection)
        self.cursor.execute("SHOW TABLES LIKE 'lotSize'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Table 'lotSize' not created")

    def test_verify_changes(self):
        Customer.verify_changes(self.connection)
        # Add assertions based on what verify_changes is supposed to do

    def test_do_one_day(self):
        customer = Customer(1, 0.5, 1, 5, 1, 3, 0.2)
        products = [1, 2, 3]
        rng = random.Random()
        customer.do_one_day(self.connection, "2023-10-01", products, rng)
        self.cursor.execute("SELECT * FROM Receipt WHERE customerId = %s", (customer.id,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Receipt not created")

    def test_main(self):
        main()
        # Add assertions based on what main is supposed to do

if __name__ == '__main__':
    unittest.main()