
import sqlite3 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, QTextEdit, QDialog, QSpinBox, QDateEdit, QDialogButtonBox, QCheckBox, QMenuBar, QMenu, QFileDialog)

from PyQt5.QtCore import Qt, QTimer, QDate, QStringListModel
from PyQt5.QtWidgets import QGridLayout,QInputDialog, QHBoxLayout, QTextEdit, QGroupBox, QAction, QSizePolicy, QCompleter
from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import payment
import edit_inventory #import EditTransactionWindow
import datetime
#from manage_customer import ManageCustomersWindow
from customer_manage import ManageCustomersWindow

currency_symbol = "\u20B5"

def log_text(text):
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Open the file in append mode (creates the file if it doesn't exist)
    with open("log.txt", "a") as file:
        # Write the timestamp followed by the input text
        file.write(f"[{timestamp}] {text}\n")


class CustomersWindow(QWidget ):
    def __init__(self, database, main_window):
        super().__init__()
        self.setWindowTitle("Customer  - {}".format(database))
        self.data = database
        self.setGeometry(200, 200, 600, 400)
        self.main_window = main_window
        #self.main_window.setWindowTitle("Customers")
        self.initUI() 
    
    def initUI(self):
        layout = QVBoxLayout()
        self.customer_table = QTableWidget()
        self.customer_table.setColumnCount(9)
        self.customer_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.customer_table.setHorizontalHeaderLabels(["Customer","Transaction ID", "Contact", "Location", "Items Bought",  f"Total Owed {currency_symbol}", f"Total Paid {currency_symbol} ", f"Remaining Debt {currency_symbol}","Transaction Date"])
        
        # Enable sorting
        self.customer_table.setSortingEnabled(True)
        
        self.checkbox_debtors = QCheckBox("Show only debtors")
        self.checkbox_debtors.stateChanged.connect(self.load_customers)
               
        # Filter Section
        filter_layout = QHBoxLayout()
        self.customer_filter = QLineEdit()
        self.customer_filter.setPlaceholderText("Search by Customer Name")
        self.product_filter = QLineEdit()
        self.product_filter.setPlaceholderText("Search by Product")

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-10))  

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())   

        self.load_customers()
        self.customer_filter.textChanged.connect(self.load_search)
        self.product_filter.textChanged.connect(self.load_search)
        self.start_date.dateChanged.connect(self.load_search)
        self.end_date.dateChanged.connect(self.load_search)

        filter_layout.addWidget(QLabel("Customer:"))
        filter_layout.addWidget(self.customer_filter)
        filter_layout.addWidget(QLabel("Product:"))
        filter_layout.addWidget(self.product_filter)
        filter_layout.addWidget(QLabel("Start Date:"))
        filter_layout.addWidget(self.start_date)
        filter_layout.addWidget(QLabel("End Date:"))
        filter_layout.addWidget(self.end_date)
        filter_layout.addWidget(self.checkbox_debtors)
        layout.addLayout(filter_layout)
        
                
        self.payment_button = QPushButton("Make Payment", self)
        #self.payment_button.setFixedSize(150, 20)  # Width: 100, Height: 50
        self.payment_button.clicked.connect(self.open_payment_window)
        
        
        # === User Management Button (Admins Only) ===
        if self.main_window.user_manager.logged_in_role == "Administrator":
            self.edit_transaction_button = QPushButton("Transaction Edit", self)
            #self.edit_transaction_button.setFixedSize(150, 20)  # Width: 100, Height: 50
            self.edit_transaction_button.clicked.connect(self.open_edit_transaction_window) 
            
            self.trans_reverse = QPushButton("Reverse Transaction", self)
            #self.trans_reverse.setFixedSize(150, 20)  # Width: 100, Height: 50
            self.trans_reverse.clicked.connect(self.reverse_transaction)        
         
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.payment_button)  
        # === User Management Button (Admins Only) ===
        if self.main_window.user_manager.logged_in_role == "Administrator":
            h_layout.addWidget(self.edit_transaction_button)
            h_layout.addWidget(self.trans_reverse)
            
        # Adding Manage Customers Button in CustomersWindow
        #self.manage_customers_button = QPushButton("Customer Database")
        #self.manage_customers_button.clicked.connect(self.open_manage_customers)
        #h_layout.addWidget(self.manage_customers_button)
         
        layout.addWidget(self.customer_table)
        # Summary Section
        self.summary_label = QLabel(f"Total Paid: {currency_symbol}  0 | Total Outstanding: {currency_symbol}  0 |Sales Value: {currency_symbol}  0")
        layout.addWidget(self.summary_label)
        layout.addLayout(h_layout)
        #layout.addWidget(self.btn_view_history)
        #layout.addLayout(button_layout)
        #layout.addWidget(self.customer_table)
        self.setLayout(layout)
        self.load_customers() 
        self.load_search()
        
        
        # Define open_manage_customers function in CustomersWindow
    def open_manage_customers(self):
        self.manage_window = ManageCustomersWindow(self.data, self.main_window)
        self.manage_window.show()       
    
    def open_edit_transaction_window(self):
        """Open a pop-up window to edit the selected transaction."""
        selected_row = self.customer_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a transaction to edit.")
            return

        trans_id = self.customer_table.item(selected_row, 1).text()  # Transaction ID

        # Admin Authentication
        password, ok = QInputDialog.getText(self, "Admin Authentication", "Enter Your Password:", QLineEdit.Password)
        auth = self.main_window.user_manager.validate_user(self.main_window.user_manager.logged_in_user, password)
        if not ok or not auth:
            QMessageBox.warning(self, "Access Denied", "Invalid password.")
            return

        # Fetch transaction details
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, location, contact, unit_price, product_name,  quantity, bulk_discount, total_paid, transaction_id, entry_date_and_time
            FROM customers WHERE transaction_id = ?
        """, (trans_id,))
        transaction_data = cursor.fetchone()
        conn.close()

        if not transaction_data:
            QMessageBox.warning(self, "Error", "Transaction not found.")
            return

        # Open Edit Transaction Window
        self.edit_window = edit_inventory.EditTransactionWindow(self.data, trans_id, transaction_data, self.main_window)
        self.edit_window.exec_()
        self.load_customers()
        self.load_search()


    def load_search(self):        
        """Load payments based on filters and update summary statistics."""
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        
        cursor.execute("SELECT item_name FROM inventory")
        itemss = cursor.fetchall()
        longest_pro_name = max(len(p[0]) for p in itemss) if itemss else 1

        customer = self.customer_filter.text().strip()
        product = self.product_filter.text().strip()
        
        query = """SELECT name, transaction_id, contact, location, product_name, 
                quantity, total_owed, total_paid, remaining_debt, transaction_date 
        FROM customers"""
        conditions = []
        params = []

        if customer and customer != "All Customers":
            conditions.append("name LIKE ?")
            params.append(f'%{customer}%')
            
        if product:
            conditions.append("product_name LIKE ?")
            params.append(f"%{product}%")

        if conditions:
            filters = " WHERE " + " AND ".join(conditions)
            query += filters
        else:
            filters = ""

        query += " ORDER BY transaction_id DESC"
        cursor.execute(query, params)
        records = cursor.fetchall()

        monospaced_font = QFont("Courier New", 10)  # Use a monospaced font consolas
        self.customer_table.setRowCount(len(records)) 
        self.customer_table.setWordWrap(True)  # Enable word wrap

        for i, row in enumerate(records):
            for j, value in enumerate(row):
                if j == 4:  # Index 4 corresponds to 'product_name'
                    try:                        
                        product_names = value.split(", ")
                        quantities = row[5].split(", ")

                        # Ensure lists are the same length
                        if len(product_names) != len(quantities):
                            continue  # Skip this row if there's a mismatch

                        # Format product names and quantities for alignment
                        formatted_lines = [
                            f"{p.ljust(longest_pro_name)}  -  {q.rjust(3)}"
                            for p, q in zip(product_names, quantities)
                        ]
                        combined_text = "\n".join(formatted_lines)

                        cell_value = QTableWidgetItem(combined_text)
                        cell_value.setFont(monospaced_font)  # Set monospaced font
                        cell_value.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        
                        # Allow cell to expand vertically
                        self.customer_table.setItem(i, j, cell_value)
                    
                    except:
                        pass

                elif j == 5:  # Skip quantity column (index 5)
                    continue
                else:
                    if j > 5:
                        j -= 1
                    cell_value = QTableWidgetItem(str(value))
                    self.customer_table.setItem(i, j, cell_value)

        # Resize row heights to fit contents
        self.customer_table.resizeRowsToContents()

        cursor.execute("SELECT SUM(remaining_debt) FROM customers"+filters, params)
        result = cursor.fetchone()
        total_outstanding = result[0] if result and result[0] else 0

        cursor.execute("SELECT SUM(total_paid) FROM customers"+filters, params)
        result = cursor.fetchone()
        total_paid = result[0] if result and result[0] else 0

        self.summary_label.setText(f"<b> <font color='blue' size =3> Total Paid: {currency_symbol} {total_paid:.2f} </font> | <font color='red' size =3 >Total Outstanding: {currency_symbol} {total_outstanding:.2f} </font>  | <font size=3 color='green' >Total Sales Value: {currency_symbol} {total_outstanding+total_paid:.2f}</font></b>")

        conn.close()

        
        
    def open_payment_window(self):
        payment_window = payment.PaymentWindow(self.data, self.main_window)
        payment_window.exec_()
        self.load_customers()
         

    def load_customers(self):
        """ Fetch customer records and update the table """ 
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()

        cursor.execute("SELECT item_name FROM inventory")
        itemss = cursor.fetchall()
        longest_pro_name = max(len(p[0]) for p in itemss) if itemss else 1

        try:
            if self.checkbox_debtors.isChecked():
                cursor.execute("SELECT name, transaction_id, contact, location, product_name, quantity, total_owed, total_paid, remaining_debt, transaction_date FROM customers WHERE remaining_debt > 0 ORDER BY remaining_debt DESC")
            else:
                cursor.execute("SELECT name, transaction_id, contact, location, product_name, quantity, total_owed, total_paid, remaining_debt, transaction_date FROM customers ORDER BY name ASC")

            rows = cursor.fetchall()
            self.customer_table.setRowCount(len(rows))

            monospaced_font = QFont("Courier New", 10)  # Use a monospaced font

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    if j == 4:  # Index 4 corresponds to 'product_name'
                        try:                            
                            product_names = value.split(", ")
                            quantities = row[5].split(", ")

                            # Ensure lists are the same length
                            if len(product_names) != len(quantities):
                                continue  # Skip this row if there's a mismatch

                            # Format product names and quantities for alignment
                            formatted_lines = [
                                f"{p.ljust(longest_pro_name)}  -  {q.rjust(3)}"
                                for p, q in zip(product_names, quantities)
                            ]
                            combined_text = "\n".join(formatted_lines)

                            cell_value = QTableWidgetItem(combined_text)
                            cell_value.setFont(monospaced_font)  # Set monospaced font
                            cell_value.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                            self.customer_table.setItem(i, j, cell_value)
                        except:
                            pass

                    elif j == 5:  # Skip quantity column (index 5)
                        continue
                    else:
                        if j > 5:
                            j -= 1
                        cell_value = QTableWidgetItem(str(value))
                        self.customer_table.setItem(i, j, cell_value)

            self.customer_table.viewport().update()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error loading customers: {str(e)}")

        finally:
            conn.close()

    
    
    def reverse_transaction(self):
        """ Reverse a selected transaction and restore previous state. """
        selected_row = self.customer_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a payment to reverse.")
            return

        trans_id = self.customer_table.item(selected_row, 1).text()  # Get transaction ID and payment date 
        customer = self.customer_table.item(selected_row, 0).text()  # Get customer name
        amount_paid = float(self.customer_table.item(selected_row, 6).text())  # Get paid amount 

        # Admin Authentication
        password, ok = QInputDialog.getText(self, "Admin Authentication", "Enter Your Password:", QLineEdit.Password)
        auth = self.main_window.user_manager.validate_user(self.main_window.user_manager.logged_in_user, password)
        if not ok or not auth:
            QMessageBox.warning(self, "Access Denied", "Invalid password.")
            return

        # Confirmation Dialog
        confirm = QMessageBox.question(self, "Confirm Reversal",
                                    f"Are you sure you want to reverse Transaction {trans_id} by {customer} of an amount of {amount_paid}?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return

        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        
        
        #fetch quantity and product name from customers table 
        cursor.execute("SELECT * FROM customers WHERE transaction_id = ?", (trans_id,))
        cus = cursor.fetchone()
        product, quantity = cus[5], cus[7] 
        # update inventory by adding back the quantity
        # first check if customer bought multiple products 
        try:
            product = product.split(", ")  # split products
            quantity = list(map(int, quantity.split(", ")))
            #unit_cost = list(map(float, unit_cost.split(", ")))
            for i, item in enumerate(product):
                cursor.execute("""UPDATE inventory SET  quantity_issued = quantity_issued - ?,
                            quantity_remaining = quantity_remaining + ?
                            WHERE item_name = ?""", 
                            (quantity[i], quantity[i], item)
                            )
                log = f"{self.main_window.user_manager.logged_in_user} updated inventories owing to reverse of transaction transaction id: {trans_id}."
                log_text(log)
        except:
            pass
            
        # delete customer record
        cursor.execute("DELETE FROM customers WHERE transaction_id = ?", (trans_id,))
        # delete payment record
        cursor.execute("DELETE FROM payments WHERE transaction_id =  ?", (trans_id,))
        conn.commit()
        conn.close()
        
        log = f"{self.main_window.user_manager.logged_in_user} reversed transaction id: {trans_id}."
        log_text(log)
        self.load_customers()  # Refresh table
        QMessageBox.information(self, "Success", "Transaction reversed successfully.")
        return
          
        
    def add_column_if_not_exists(self, table_name, column_name, column_type):
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        
        # Check if the column exists
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [column[1] for column in cursor.fetchall()]  # Extract column names

        if column_name not in columns:
            # Add column if it doesn't exist
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")
            conn.commit()
            print(f"Column '{column_name}' added to '{table_name}'.")
        else:
            pass # print(f"Column '{column_name}' already exists in '{table_name}'.")

        conn.close()        