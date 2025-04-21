
import sqlite3 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, QTextEdit, QDialog, QSpinBox, QDateEdit, QDialogButtonBox, QCheckBox, QMenuBar, QMenu, QFileDialog)

from PyQt5.QtCore import Qt, QTimer, QDate, QStringListModel
from PyQt5.QtWidgets import QGridLayout,QInputDialog, QHBoxLayout, QTextEdit, QGroupBox, QAction, QSizePolicy, QCompleter
from PyQt5.QtGui import QPalette, QFont ,QIntValidator
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

class ManageCustomersWindow(QWidget):
    def __init__(self, database, main_window):
        super().__init__()
        self.setWindowTitle("Manage Customers")
        self.data = database
        self.main_window = main_window
        self.setGeometry(200, 200, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, location, or contact")
        self.search_input.textChanged.connect(self.load_customers)

        self.customer_records_table = QTableWidget()
        self.customer_records_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.customer_records_table.setColumnCount(3)
        self.customer_records_table.setHorizontalHeaderLabels(["Customer Name", "Location", "Contact"])
        self.customer_records_table.setSortingEnabled(True)
        self.load_customers()

        self.add_button = QPushButton("Add Customer")
        self.edit_button = QPushButton("Edit Customer")
        self.delete_button = QPushButton("Delete Customer")
        self.history_button = QPushButton("View Transaction History")

        self.add_button.clicked.connect(self.add_customer)
        self.edit_button.clicked.connect(self.edit_customer)
        self.delete_button.clicked.connect(self.delete_customer)
        self.history_button.clicked.connect(self.view_transaction_history)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.history_button)

        layout.addWidget(self.search_input)
        layout.addWidget(self.customer_records_table)
        layout.addLayout(button_layout)
        self.setLayout(layout)

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

    def view_transaction_history(self):
        selected_row = self.customer_records_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a customer to view history.")
            return
        name = self.customer_records_table.item(selected_row, 0).text()
        history_window = TransactionHistoryWindow(self.data, name)
        history_window.exec_()




class TransactionHistoryWindow(QDialog):
    def __init__(self, database, customer_name):
        super().__init__()
        self.setWindowTitle(f"Transaction History - {customer_name}")
        self.data = database
        self.customer_name = customer_name
        self.setGeometry(300, 300, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Transaction ID", "Item(s)", "Amount Paid", "Total Owed", "Remaining Debt", "Date"
        ])
        self.history_table.setFont(QFont("Courier New", 10))  # Monospaced font for alignment
        self.history_table.resizeColumnsToContents()  # Auto resize columns
        self.history_table.resizeRowsToContents()  # Auto resize rows
        self.load_transactions()
        layout.addWidget(self.history_table)
        self.setLayout(layout)

    def format_products_and_quantities(self, products, quantities):
        product_list = products.split(", ")
        quantity_list = quantities.split(", ")
        formatted_text = "\n".join(f"{p.ljust(20)} {q}" for p, q in zip(product_list, quantity_list))
        return formatted_text

    def load_transactions(self):
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        
        # Query to get all transactions from the customers table for the given customer
        cursor.execute("""
            SELECT transaction_id, product_name, quantity, total_paid, total_owed, remaining_debt, transaction_date 
            FROM customers WHERE name = ? ORDER BY transaction_id
        """, (self.customer_name,))
        transactions = cursor.fetchall()
        
        all_rows = []
        
        for transaction in transactions:
            transaction_id, product_name, quantity, total_paid, total_owed, remaining_debt, date = transaction
            formatted_products = self.format_products_and_quantities(product_name, quantity)
            
            # Add customer transaction row first
            all_rows.append((transaction_id, formatted_products, total_paid, total_owed, remaining_debt, date))
            
            # Query to get all payments related to this transaction_id from the payments table
            cursor.execute("""
                SELECT item_name, amount_paid, transaction_date
                FROM payments WHERE transaction_id = ?
            """, (transaction_id,))
            payments = cursor.fetchall()
            
            # Assign quantities to payment products if transaction_id matches
            if payments:
                payment_products = ", ".join([p[0] for p in payments])  # Extract item names
                formatted_payment_products = self.format_products_and_quantities(payment_products, quantity)
                for payment in payments:
                    item_name, amount_paid, payment_date = payment
                    all_rows.append((transaction_id, formatted_payment_products, amount_paid, '', '', payment_date))
        
        self.history_table.setRowCount(len(all_rows))
        
        for i, row in enumerate(all_rows):
            for j, value in enumerate(row):
                self.history_table.setItem(i, j, QTableWidgetItem(str(value)))
        
        self.history_table.resizeColumnsToContents()  # Adjust column width after inserting data
        self.history_table.resizeRowsToContents()  # Adjust row height after inserting data
        conn.close()


