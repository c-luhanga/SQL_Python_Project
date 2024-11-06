BakeryBase Database Simulation
=============================

This project simulates customer purchasing activity in a bakery using a MySQL database. It generates purchase receipts, line items, and customer reviews, allowing for realistic database traffic and performance testing. The simulation aims to create 100,000 line items within 10 minutes, making it an ideal project for testing and optimizing database operations.

Features
--------

- **Customer Activity Simulation**: Each customer has a configurable probability of making purchases, a range for the number of products they buy, and a chance of reviewing products.
- **Database Schema Management**: Initializes and normalizes tables, including products, customers, receipts, line items, reviews, and inventory.
- **Efficient Data Generation**: Inserts records in batches to optimize database transactions, enabling high-volume line item generation.
- **Automatic Inventory Management**: Automatically adjusts inventory (`Lot` quantities) and creates new lots as needed for continuous product availability.

Database Schema
---------------

The main tables include:

- **Customer**: Stores customer information.
- **Product**: Contains bakery product details.
- **Receipt**: Records customer transactions.
- **LineItem**: Details each product purchased within a receipt.
- **Rating**: Stores customer reviews of products.
- **Lot**: Manages inventory with batch tracking.
- **Inventory**: Tracks lot sizes and current lot IDs for each product.

Setup Instructions
------------------

1. **Clone the Repository**:
    ```
    git clone https://github.com/yourusername/BakeryBase.git
    cd BakeryBase
    ```

2. **Install MySQL**: Ensure that MySQL is installed and running on your system.

3. **Create the Database and Tables**:
    - Use the provided SQL script (`BakeryBase.sql`) to set up the `BakeryBase` database schema:
    ```
    mysql -u your_username -p < BakeryBase.sql
    ```

4. **Python Environment**:
    - Install necessary Python libraries:
    ```
    pip install mysql-connector-python
    ```

5. **Configure Database Connection**:
    - In `PythonDBExample.py`, update the database connection parameters with your MySQL username and password.

Running the Simulation
----------------------

The script simulates customer activity over a specified date range and generates receipts, line items, and reviews.

1. **Run the Script**:
    ```
    python PythonDBExample.py 2023-10-01 2023-10-07
    ```
   - Replace `2023-10-01` and `2023-10-07` with your desired start and end dates.

2. **Target Simulation**: The script will continue generating line items until it reaches 100,000 entries.

Key Classes and Functions
-------------------------

- **Customer Class**: Manages customer information, purchases, and reviews.
  - `insert()`: Adds a customer to the database.
  - `do_one_day()`: Simulates a day of customer activity, generating receipts and line items.
  - `addReceipt()` and `addLineItem()`: Helper methods to insert records into the `Receipt` and `LineItem` tables.

- **Simulation Functions**:
  - `run_simulation()`: Runs the simulation until 100,000 line items are generated.
  - `normalize()`: Normalizes the database schema, creating `Kind` and `Flavor` tables and linking them with products.
  - `verify_changes()`: Verifies schema adjustments and displays database content for debugging.

Performance Optimization
------------------------

To achieve the target of generating 100,000 line items within 10 minutes, the script employs:

- **Batch Commits**: Batches multiple inserts and commits them together to reduce transaction overhead.
- **Bulk Inserts**: Accumulates `LineItem` records for each receipt, then inserts them in a single operation.
- **Minimal Logging**: Limits output during large simulations to improve runtime performance.

Testing
-------

To verify the simulation, you can check the number of line items created:
