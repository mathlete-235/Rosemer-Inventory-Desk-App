import sqlite3 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog,
                             QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QSplitter, QDialogButtonBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QRegExpValidator 
from PyQt5.QtCore import QRegExp
#from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QSize

currency_symbol = "\u20B5"

class ManageCustomersWindow(QWidget):
    def __init__(self, database, main_window):
        super().__init__()
        self.setWindowTitle("Manage Customers")
        self.data = database
        self.main_window = main_window
        self.setGeometry(200, 200, 900, 500)  # Increased width to accommodate both tables
        self.initUI()

    def initUI(self):
        self.splitter = QSplitter(Qt.Horizontal)
        left_layout = QVBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, location, or contact")
        self.search_input.textChanged.connect(self.load_customers)

        self.customer_records_table = QTableWidget()
        self.customer_records_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.customer_records_table.setColumnCount(3)
        self.customer_records_table.setHorizontalHeaderLabels(["Customer Name", "Location", "Contact"])
        self.customer_records_table.setSortingEnabled(True)
        self.customer_records_table.itemSelectionChanged.connect(self.view_transaction_history)

        self.add_button = QPushButton("Add Customer")
        self.edit_button = QPushButton("Edit Customer")
        self.delete_button = QPushButton("Delete Customer")
        #self.history_button = QPushButton("View Transaction History")
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        #button_layout.addWidget(self.history_button)

        self.add_button.clicked.connect(self.add_customer)
        self.edit_button.clicked.connect(self.edit_customer)
        self.delete_button.clicked.connect(self.delete_customer)
        self.load_customers()

        left_layout.addWidget(self.search_input)
        left_layout.addWidget(self.customer_records_table)
        left_layout.addLayout(button_layout) 
        
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        self.splitter.addWidget(left_widget)
        
        right_layout = QVBoxLayout()
        self.history_label = QLabel("Transaction History")
        self.history_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.history_label.setAlignment(Qt.AlignCenter)
        self.history_label.setVisible(False)
        
        self.transaction_history_table = QTableWidget()
        self.transaction_history_table.setColumnCount(6)
        self.transaction_history_table.setHorizontalHeaderLabels([
            "Transaction ID", "Item(s)", f"Amount Paid {currency_symbol}", f"Total Owed {currency_symbol}", f"Remaining Debt {currency_symbol}", "Date"
        ])
        self.transaction_history_table.setFont(QFont("Courier New", 10))  # Monospaced font for alignment
        self.transaction_history_table.setVisible(False)
        #self.splitter.addWidget(self.transaction_history_table)
        
        right_layout.addWidget(self.history_label)
        right_layout.addWidget(self.transaction_history_table)
        
        self.right_widget = QWidget()
        self.right_widget.setLayout(right_layout)
        self.splitter.addWidget(self.right_widget)
        # Set the stretch factors
        #self.splitter.setStretchFactor(0, 1)  # Customer table gets 1 part
        self.splitter.setStretchFactor(1, 3)  # Transaction table gets 2 parts
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.splitter)
        self.setLayout(main_layout)
        
        self.setMouseTracking(True)

    def add_customer(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Customer")
        layout = QVBoxLayout()

        name_input = QLineEdit()
        location_input = QLineEdit()
        contact_input = QLineEdit()
        # Set validator to allow exactly 10 digits
        contact_validator = QRegExpValidator(QRegExp(r"^\d{10}$"), contact_input)
        contact_input.setValidator(contact_validator)
        name_input.setPlaceholderText("Name")
        location_input.setPlaceholderText("Location")
        contact_input.setPlaceholderText("Contact")

        layout.addWidget(QLabel("Customer Name:"))
        layout.addWidget(name_input)
        layout.addWidget(QLabel("Location:"))
        layout.addWidget(location_input)
        layout.addWidget(QLabel("Contact:"))
        layout.addWidget(contact_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        if dialog.exec_() == QDialog.Accepted:
            name, location, contact = name_input.text(), location_input.text(), contact_input.text()
            if name and location and contact:
                conn = sqlite3.connect(self.data)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO customers_data (name, location, contact) VALUES (?, ?, ?)", (name, location, contact))
                conn.commit()
                conn.close()
                self.load_customers()

    def edit_customer(self):
        selected_row = self.customer_records_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a customer to edit.")
            return

        name = self.customer_records_table.item(selected_row, 0).text()
        location = self.customer_records_table.item(selected_row, 1).text()
        contact = self.customer_records_table.item(selected_row, 2).text()

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Customer")
        layout = QVBoxLayout()

        name_input = QLineEdit(name)
        location_input = QLineEdit(location)
        contact_input = QLineEdit(contact)
        # Set validator to allow exactly 10 digits
        contact_validator = QRegExpValidator(QRegExp(r"^\d{10}$"), contact_input)
        contact_input.setValidator(contact_validator)

        layout.addWidget(QLabel("Customer Name:"))
        layout.addWidget(name_input)
        layout.addWidget(QLabel("Location:"))
        layout.addWidget(location_input)
        layout.addWidget(QLabel("Contact:"))
        layout.addWidget(contact_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        if dialog.exec_() == QDialog.Accepted:
            new_name, new_location, new_contact = name_input.text(), location_input.text(), contact_input.text()
            if new_name and new_location and new_contact:
                conn = sqlite3.connect(self.data)
                cursor = conn.cursor()
                cursor.execute("UPDATE customers_data SET name = ?, location = ?, contact = ? WHERE name = ?", (new_name, new_location, new_contact, name))
                conn.commit()
                conn.close()
                self.load_customers()

    def delete_customer(self):
        selected_row = self.customer_records_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a customer to delete.")
            return
        name = self.customer_records_table.item(selected_row, 0).text()
        confirm = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete {name}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            conn = sqlite3.connect(self.data)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers_data WHERE name = ?", (name,))
            conn.commit()
            conn.close()
            self.load_customers()

    def load_customers(self):
        search_text = self.search_input.text().strip()
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        query = "SELECT name, location, contact FROM customers_data"
        params = ()

        if search_text:
            query += " WHERE name LIKE ? OR location LIKE ? OR contact LIKE ?"
            params = (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%")

        cursor.execute(query, params)
        rows = cursor.fetchall()
        self.customer_records_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.customer_records_table.setItem(i, j, QTableWidgetItem(str(value)))
        conn.close()

    def view_transaction_history(self):
        selected_row = self.customer_records_table.currentRow()
        if selected_row == -1:
            self.transaction_history_table.setVisible(False)
            self.history_label.setVisible(False)
            return
        
        name = self.customer_records_table.item(selected_row, 0).text()
        self.history_label.setText(f"Transaction History of {name}")
        self.load_transactions(name)
        self.transaction_history_table.setVisible(True)
        self.history_label.setVisible(True) 
        self.main_window.adjust_window_size()
        

    def format_products_and_quantities(self, products, quantities):
        product_list = products.split(", ")
        quantity_list = quantities.split(", ")
        formatted_text = "\n".join(f"{p.ljust(20)} - {q.rjust(3)}" for p, q in zip(product_list, quantity_list))
        return formatted_text

    def load_transactions(self, customer_name):
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT transaction_id, product_name, quantity, total_paid, total_owed, remaining_debt, transaction_date 
            FROM customers WHERE name = ? ORDER BY transaction_id
        """, (customer_name,))
        transactions = cursor.fetchall()
        
        all_rows = []
        for transaction in transactions:
            transaction_id, product_name, quantity, total_paid, total_owed, remaining_debt, date = transaction
            formatted_products = self.format_products_and_quantities(product_name, quantity)
            
            all_rows.append((transaction_id, formatted_products, total_paid, total_owed, remaining_debt, date))
            
            cursor.execute("""
                SELECT item_name, amount_paid, transaction_date
                FROM payments WHERE transaction_id = ?
            """, (transaction_id,))
            payments = cursor.fetchall()
            
            if payments:
                payment_products = ", ".join([p[0] for p in payments])
                formatted_payment_products = self.format_products_and_quantities(payment_products, quantity)
                for payment in payments:
                    item_name, amount_paid, payment_date = payment
                    all_rows.append((transaction_id, formatted_payment_products, amount_paid, '', '', payment_date))
        
        self.transaction_history_table.setRowCount(len(all_rows))
        for i, row in enumerate(all_rows):
            for j, value in enumerate(row):
                self.transaction_history_table.setItem(i, j, QTableWidgetItem(str(value)))
        
        self.transaction_history_table.resizeColumnsToContents()
        self.transaction_history_table.resizeRowsToContents()
        conn.close()
    
    def mousePressEvent(self, event):
        if self.transaction_history_table.isVisible():
            index = self.transaction_history_table.indexAt(event.pos())
            if not index.isValid():  # If the click is outside any cell
                self.transaction_history_table.setVisible(False)
                self.history_label.setVisible(False) 
                self.main_window.adjust_window_size()
        else:            
            if not self.transaction_history_table.geometry().contains(event.pos()):
                self.transaction_history_table.setVisible(False)
                self.history_label.setVisible(False) 
                self.main_window.adjust_window_size()
        super().mousePressEvent(event) 