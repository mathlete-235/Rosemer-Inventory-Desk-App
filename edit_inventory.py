import sys, csv, pandas as pd
import sqlite3, os, subprocess
import hashlib 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDoubleSpinBox,
                             QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, QTextEdit, QDialog, QSpinBox, QDateEdit, QDialogButtonBox, QCheckBox, QMenuBar, QMenu, QFileDialog)

from PyQt5.QtCore import Qt, QTimer, QDate, QStringListModel
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QTextEdit, QGroupBox, QAction, QSizePolicy, QCompleter
from PyQt5.QtGui import QPalette, QDoubleValidator
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

from datetime import datetime
from contextlib import contextmanager

class TransactionIDGenerator:
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_sequence_table()

    @contextmanager
    def _get_cursor(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA busy_timeout = 5000")  # Handle concurrent access
        try:
            yield conn.cursor()
            conn.commit()
        finally:
            conn.close()

    def _init_sequence_table(self):
        """Create sequence table if not exists"""
        with self._get_cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transaction_sequence (
                    date TEXT PRIMARY KEY,
                    last_sequence INTEGER NOT NULL DEFAULT 0
                )
            """)

    def generate_id(self):
        """Generate unique transaction ID with concurrency safety"""
        today = datetime.now().strftime("%Y%m%d")
        sequence = 0

        with self._get_cursor() as cursor:
            # Start immediate transaction to lock the database
            cursor.execute("BEGIN IMMEDIATE")
            
            # Get or create today's sequence
            cursor.execute("""
                INSERT INTO transaction_sequence (date, last_sequence)
                VALUES (?, 1)
                ON CONFLICT(date) DO UPDATE SET
                    last_sequence = last_sequence + 1
                RETURNING last_sequence
            """, (today,))
            
            sequence = cursor.fetchone()[0]

        return f"INV-{today}-{sequence:05d}"

class EditInventoryDialog(QDialog):
    def __init__(self, item_name, current_quantity, current_price, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Inventory Item")
        self.item_name = item_name
        layout = QVBoxLayout()
        
        self.product = QLabel("Product: {}".format(item_name))
        self.label_quantity = QLabel("New Quantity:")
        self.input_quantity = QSpinBox()
        self.input_quantity.setMaximum(99999)
        self.input_quantity.setValue(current_quantity)
        
        self.label_price = QLabel("New Unit Price:")
        self.input_price = QLineEdit()
        validator = QDoubleValidator(0.0, 999999.99, 2)  # Min 0.0, Max 999999.99, 2 decimal places
        validator.setNotation(QDoubleValidator.StandardNotation)  # Standard notation
        self.input_price.setValidator(validator)
        self.input_price.setText(str(current_price))
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        layout.addWidget(self.product)
        layout.addWidget(self.label_quantity)
        layout.addWidget(self.input_quantity)
        layout.addWidget(self.label_price)
        layout.addWidget(self.input_price)
        layout.addWidget(self.button_box)
        
        self.setLayout(layout)
    
    def get_new_values(self):
        return self.input_quantity.value(), float(self.input_price.text())
    
class EditTransactionWindow(QDialog):
    def __init__(self, database, trans_id, transaction_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Transaction")
        self.database = database
        self.trans_id = trans_id
        self.transaction_data = transaction_data
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Editable fields
        self.customer_name = QLineEdit(self.transaction_data[0])  # Name
        self.customer_location = QLineEdit(self.transaction_data[1])  # Location
        self.customer_contact = QLineEdit(self.transaction_data[2])  # Contact
        # Set validator to allow exactly 10 digits
        contact_validator = QRegExpValidator(QRegExp(r"^\d{10}$"), self.customer_contact)
        self.customer_contact.setValidator(contact_validator)
        self.load_customer_suggestions()
        # Table for multiple products
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(3)
        self.product_table.setHorizontalHeaderLabels(["Product Name",  "Quantity", "Bulk Discount"])
        self.load_products()

        layout.addWidget(QLabel("Customer Name:"))
        layout.addWidget(self.customer_name)
        layout.addWidget(QLabel("Location:"))
        layout.addWidget(self.customer_location)
        layout.addWidget(QLabel("Contact:"))
        layout.addWidget(self.customer_contact)
        layout.addWidget(QLabel("Products:"))
        layout.addWidget(self.product_table)

        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def load_products(self):
        """Load products into table.""" 
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT item_name FROM inventory")
        product_names = [row[0] for row in cursor.fetchall()] 
        
        previous_param = [self.transaction_data[x] for x in range(4,7)]
        previous_selected_products = previous_param[0].split(", ")
        previous_selected_qty = previous_param[1].split(", ")
        previous_selected_bulk_discount = previous_param[2].split(", ") 
                
        # Create a dictionary mapping items in list_two to their corresponding values in list_three
        value_map = dict(zip(previous_selected_products, zip(previous_selected_qty, previous_selected_bulk_discount)))
        #print(value_map)
        # Generate list_four by checking each item in list_one against the mapping
        list_four = [value_map.get(item, [0,0]) for item in product_names]
        self.previous_combination = list_four                                  
        conn.close()

        self.product_table.setRowCount(len(product_names))
        
        for i in range(len(product_names)):
            for j in range(2):                
                quantity_input = QSpinBox()
                if j > 0:
                    quantity_input = QDoubleSpinBox() #discounted prices column as a float
                    quantity_input.setMaximum(9999999.99)
                    quantity_input.setValue(float(list_four[i][j]))
                if j < 1: 
                    quantity_input.setMaximum(99999999) #set maiximum to stock available
                    quantity_input.setValue(int(list_four[i][j]))
                    #quantity_input.setMinimum(0)
                self.product_table.setCellWidget(i, 1+j, quantity_input) 

        for i in range(len(product_names)): 
            product_dropdown = QComboBox()
            product_dropdown.addItems(product_names)
            product_dropdown.setCurrentText(product_names[i])  # Select existing product
            self.product_table.setCellWidget(i,0,product_dropdown)
    
    def get_selected_products(self):
        selected_products = []
        for row in range(self.product_table.rowCount()): 
            item = self.product_table.cellWidget(row, 0).currentText() 
            quantity = self.product_table.cellWidget(row, 1).value()
            bulk_discount = self.product_table.cellWidget(row, 2).value() 

            #if quantity > 0:
            selected_products.append((item, quantity, bulk_discount))
        return selected_products
            
            
    def save_changes(self):
        """Update transaction details and update inventory."""
        name = self.customer_name.text().strip()
        location = self.customer_location.text().strip()
        contact = self.customer_contact.text().strip()

        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        selection = self.get_selected_products()
        total_owed = 0
        insufficient_stock_items = []
        items = ""
        qty = ""
        b_disc = "" 
        u_price = ""  
        
        for i, row in enumerate(selection):
            item, quantity, bulk_discount  = row
            if quantity <=0: continue 
            cursor.execute("SELECT unit_price, quantity_remaining FROM inventory WHERE item_name = ?", (item,))
            result = cursor.fetchone() 
            if quantity > result[1]:
                QMessageBox.warning(self, "Stock Warning", f"Not enough stock for: {', '.join(insufficient_stock_items)}. These items were not added.")     
                conn.close()
                return
                
            if quantity <= result[1]:
                #items.append(item) # json.dumps(items) 
                adder = ", "
                items += item + adder 
                qty += str(quantity) + adder 
                b_disc += str(bulk_discount) + adder 
                u_price += str(result[0]) + adder 
                                        
                if not result:
                    QMessageBox.warning(self, "Error", f"Item '{item}' not found in inventory.")
                    continue
                if quantity <= 0: continue
                
                unit_price, stock_remaining = result
                if quantity > stock_remaining:
                    insufficient_stock_items.append(item)
                    continue  # Skip this item
                
                applied_price = unit_price
                if bulk_discount > 0:
                    applied_price = bulk_discount  
                item_total = quantity * applied_price
                total_owed += item_total  # Accumulate total owed 

                prev_qty = int(self.previous_combination[i][0])
                new_qty = quantity - prev_qty
                cursor.execute("""
                    UPDATE inventory 
                    SET quantity_issued = quantity_issued + ?, quantity_remaining = quantity_remaining - ? 
                    WHERE item_name = ?
                """, (new_qty, new_qty, item)) 


        if insufficient_stock_items:
            QMessageBox.warning(self, "Stock Warning", f"Not enough stock for: {', '.join(insufficient_stock_items)}. These items were not added.")

        remaining_debt = total_owed - int(self.transaction_data[7])
        items,u_price,qty,b_disc = items[:-2],u_price[:-2],qty[:-2], b_disc[:-2]
                
        cursor.execute("""
            UPDATE customers SET name= ?, location=?, contact=?, product_name=?, unit_price=?, quantity=?, bulk_discount=?, total_owed =?,  remaining_debt = ? 
            WHERE transaction_id = ?  
        """, (name, location, contact, items,u_price,qty,b_disc, total_owed, remaining_debt, self.transaction_data[8]))
        
        #update payments table
        '''
        cursor.execute("""
            UPDATE payments SET customer_name= ?, item_name=? 
            WHERE transaction_id = ? AND entry_date_and_time = ?
        """, (name,   items, self.transaction_data[9], self.transaction_data[10]))'''        
        cursor.execute("""
            UPDATE payments SET customer_name= ?, item_name=? 
            WHERE transaction_id = ?
        """, (name,   items, self.transaction_data[8]))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Transaction updated successfully.")
        self.accept()  # Close window

        
    def load_customer_suggestions(self):
        """ Load customer data for auto-completion and set up bi-directional auto-fill """
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT name, location, contact FROM customers_data")
            customers = cursor.fetchall()

            # Store suggestions in dictionaries for quick lookup
            self.customer_dict = {row[0]: (row[1], row[2]) for row in customers}  # name -> (location, contact)
            self.contact_dict = {row[2]: (row[0], row[1]) for row in customers}  # contact -> (name, location)
            self.location_dict = {row[1]: (row[0], row[2]) for row in customers}  # location -> (name, contact)

            # Extract lists for auto-completion
            self.customer_names = list(self.customer_dict.keys())
            self.customer_contacts = list(self.contact_dict.keys())
            self.customer_locations = list(self.location_dict.keys())

            # Setup QCompleter for each field
            name_completer = QCompleter(self.customer_names, self)
            name_completer.setCaseSensitivity(Qt.CaseInsensitive)
            name_completer.setFilterMode(Qt.MatchContains)
            self.customer_name.setCompleter(name_completer)

            location_completer = QCompleter(self.customer_locations, self)
            location_completer.setCaseSensitivity(Qt.CaseInsensitive)
            location_completer.setFilterMode(Qt.MatchContains)
            self.customer_location.setCompleter(location_completer)

            contact_completer = QCompleter(self.customer_contacts, self)
            contact_completer.setCaseSensitivity(Qt.CaseInsensitive)
            contact_completer.setFilterMode(Qt.MatchContains)
            self.customer_contact.setCompleter(contact_completer)

            # Connect signals for bi-directional auto-fill
            self.customer_name.textChanged.connect(self.update_from_name)
            self.customer_contact.textChanged.connect(self.update_from_contact)
            self.customer_location.textChanged.connect(self.update_from_location)

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error loading customers: {str(e)}")

        finally:
            conn.close()

    def update_from_name(self):
        """ Auto-fill contact & location when customer name is changed """
        customer_name = self.customer_name.text().strip()
        
        if customer_name in self.customer_dict:
            location, contact = self.customer_dict[customer_name]
            self.customer_location.setText(location)
            self.customer_contact.setText(contact)

    def update_from_contact(self):
        """ Auto-fill name & location when customer contact is changed """
        customer_contact = self.customer_contact.text().strip()
        
        if customer_contact in self.contact_dict:
            name, location = self.contact_dict[customer_contact]
            self.customer_name.setText(name)
            self.customer_location.setText(location)

    def update_from_location(self):
        """ Auto-fill name & contact when customer location is changed """
        customer_location = self.customer_location.text().strip()
        
        if customer_location in self.location_dict:
            name, contact = self.location_dict[customer_location]
            self.customer_name.setText(name)
            self.customer_contact.setText(contact) 