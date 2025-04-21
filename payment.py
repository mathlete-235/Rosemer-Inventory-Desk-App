import sys
import sqlite3, os, subprocess  
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, QTextEdit, QDialog, QSpinBox, QDateEdit, QDialogButtonBox, QCheckBox, QMenuBar, QMenu, QFileDialog)

from PyQt5.QtCore import Qt, QTimer, QDate, QStringListModel
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QTextEdit, QGroupBox, QAction, QSizePolicy, QCompleter
from PyQt5.QtGui import QPalette, QDoubleValidator
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

from datetime import datetime
import requests


currency_symbol = "\u20B5"

FAYASMS_API_KEY = "your_fayasms_api_key"
FAYASMS_SENDER_ID = "YourBusinessName"


def log_text(text):
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Open the file in append mode (creates the file if it doesn't exist)
    with open("log.txt", "a") as file:
        # Write the timestamp followed by the input text
        file.write(f"[{timestamp}] {text}\n")


class PaymentWindow(QDialog):
    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Make Payment")
        self.data = database
        self.parent_window = parent
        self.transac_id = ""
        layout = QVBoxLayout()
        self.receipt_data = [] 
 
        self.total_debt_label = QLabel("Total Debt: ")
        self.amount_paid = QLineEdit()
        self.amount_paid.setPlaceholderText("Amount Paid")
        validator = QDoubleValidator(0.0, 999999.99, 2)  # Min 0.0, Max 999999.99, 2 decimal places
        validator.setNotation(QDoubleValidator.StandardNotation)  # Standard notation
        self.amount_paid.setValidator(validator)
        self.payment_mode = QComboBox()
        self.payment_mode.addItems(["Cash", "Cheque"])
        self.payment_mode.currentIndexChanged.connect(self.toggle_cheque_details)

        # Customer Name Input with Auto-Suggestions
        self.customer_input = QLineEdit()
        self.customer_input.setPlaceholderText("Enter Customer Name or Transaction ID")
        self.customer_input.textChanged.connect(self.update_customer_suggestions)
        self.customer_completer = QCompleter([])  # Empty at first
        self.customer_completer.setCaseSensitivity(False)
        self.customer_input.setCompleter(self.customer_completer)
        # Transaction ID ComboBox
        self.transaction_combo = QComboBox()
        self.transaction_combo.setPlaceholderText("Select Transaction ID")
        
        layout.addWidget(QLabel("Customer Name / Transaction ID:"))
        layout.addWidget(self.customer_input)
        layout.addWidget(QLabel("Transaction ID (Debts Only):"))
        layout.addWidget(self.transaction_combo)
        
        self.tran_date = QDateEdit()
        self.tran_date.setCalendarPopup(True)
        self.tran_date.setDate(QDate.currentDate())  


        self.cheque_details = QWidget()
        cheque_layout = QVBoxLayout()
        self.cheque_number = QLineEdit()
        self.cheque_number.setPlaceholderText("Cheque Number")
        self.cheque_bank = QLineEdit()
        self.cheque_bank.setPlaceholderText("Bank")
        self.cheque_clearance_date = QDateEdit()
        self.cheque_clearance_date.setDate(QDate.currentDate())  
        self.cheque_clearance_date.setCalendarPopup(True)
        cheque_layout.addWidget(self.cheque_number)
        cheque_layout.addWidget(self.cheque_bank)
        cheque_layout.addWidget(self.cheque_clearance_date)
        self.cheque_details.setLayout(cheque_layout)
        self.cheque_details.setVisible(False)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.record_payment)
        self.button_box.rejected.connect(self.reject)
        self.print_receipt= QCheckBox("Print Receipt")
        self.send_sms = QCheckBox("Send SMS Alert")
 
        layout.addWidget(self.total_debt_label)
        layout.addWidget(QLabel("Transaction Date:"))
        layout.addWidget(self.tran_date)
        layout.addWidget(QLabel("Amount Paid:"))
        layout.addWidget(self.amount_paid)
        layout.addWidget(QLabel("Payment Mode:"))
        layout.addWidget(self.payment_mode)
        layout.addWidget(self.cheque_details)
        layout.addWidget(self.print_receipt)
        layout.addWidget(self.send_sms)
        layout.addWidget(self.button_box)
         
 

        self.setLayout(layout)
        # Load customer suggestions initially
        self.load_customer_and_transaction_data()       
        self.update_total_debt()
        self.customer_input.textChanged.connect(self.update_total_debt) 
        self.transaction_combo.currentIndexChanged.connect(self.update_total_debt)  

            
    def load_customer_and_transaction_data(self):
        """ Load customer names and transaction IDs into the autocomplete list """
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()

        # Load Customer Names
        cursor.execute("SELECT DISTINCT name FROM customers")
        customers = [row[0] for row in cursor.fetchall()]

        # Load Transaction IDs with Debt
        cursor.execute("SELECT transaction_id FROM customers WHERE remaining_debt > 0")
        transactions = [row[0] for row in cursor.fetchall()]

        conn.close()

        # Combine both for Autocomplete
        combined_list = customers + transactions
        model = QStringListModel(combined_list)
        self.customer_completer.setModel(model)
        
    def update_customer_suggestions(self):
        """ When customer name or transaction ID is entered, update transaction list """
        input_text = self.customer_input.text().strip()
        if input_text:
            conn = sqlite3.connect(self.data)
            cursor = conn.cursor()

            if input_text.startswith("INV-".casefold()):  # If transaction ID is entered
                cursor.execute("SELECT name FROM customers WHERE transaction_id LIKE ?",  (f'%{input_text}%',))
                result = cursor.fetchone()
                if result:
                    customer_name = result[0]
                    self.customer_input.setText(customer_name)  # Auto-fill customer name
                    self.transaction_combo.setCurrentText(input_text)  # Select transaction ID
            else:
                cursor.execute("SELECT transaction_id FROM customers WHERE name LIKE ? AND remaining_debt > 0", (f'%{input_text}%',))
                transactions = [row[0] for row in cursor.fetchall()]
                self.transaction_combo.clear()
                self.transaction_combo.addItems(transactions)

            conn.close()

    def update_total_debt(self): 
        customer = self.customer_input.text().strip()
        trans_id =  self.transaction_combo.currentText()
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        if trans_id == "":
            cursor.execute("SELECT SUM(remaining_debt) FROM customers WHERE name = ?", (customer,))
        else:
            cursor.execute("SELECT remaining_debt FROM customers WHERE transaction_id = ?", (trans_id,))
        result = cursor.fetchone()
        total_debt = result[0] if result and result[0] else 0
        self.total_debt_label.setText(f"Total Debt: {total_debt}")
        self.amount_paid.setPlaceholderText(str(total_debt))
        self.owing = total_debt
        conn.close()

    def toggle_cheque_details(self):
        self.cheque_details.setVisible(self.payment_mode.currentText() == "Cheque")
        
    def get_selected_items(self):
        selected_items = []
        for row in range(self.sales_table.rowCount()):  # Assuming a table-based UI
            item = self.sales_table.item(row, 0).text()
            quantity = self.sales_table.cellWidget(row, 1).value()  # Assuming QSpinBox for quantity
            if quantity > 0:
                selected_items.append((item, quantity))
        return selected_items


    def record_payment(self): 
        customer = self.customer_input.text().strip()
        trans_id = self.transaction_combo.currentText()
        amount_paid = float(self.amount_paid.text()) if self.amount_paid.text() else 0.0
        payment_mode = self.payment_mode.currentText()
        tran_date = self.tran_date.date().toString("ddd, dd MMM yyyy")
        cheque_number = self.cheque_number.text() if payment_mode == "Cheque" else None
        cheque_bank = self.cheque_bank.text() if payment_mode == "Cheque" else None
        cheque_clearance_date = self.cheque_clearance_date.date().toString("yyyy-MM-dd") if payment_mode == "Cheque" else None
        self.transac_id = trans_id
        if amount_paid <= 0:
            QMessageBox.warning(self, "Error", "Please enter a valid payment amount.")
            return

        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()

        # Fetch unpaid sales for this customer, ordered by sale date        
        cursor.execute("SELECT  product_name, total_paid, unit_price, quantity, total_owed, remaining_debt, contact FROM customers WHERE name = ? AND transaction_id = ?", (customer,trans_id))
        result = cursor.fetchone()

        if not result:
            QMessageBox.warning(self, "Error", "Customer not found.")
            conn.close()
            return
                
         
        remaining_payment = amount_paid
        
        product, total_paid, unit_price, quantity, total_owed, remaining_debt, contact = result
        
        if amount_paid > remaining_debt:
            QMessageBox.warning(self, "Error", "Amount paid exceeds remaining debt.")
            remaining_payment = remaining_debt
            
        remaining_debt -= remaining_payment
        total_paid += remaining_payment


        
        
        # Update customers table
        cursor.execute("""
            UPDATE customers
            SET  total_paid = ?, remaining_debt = ?
            WHERE transaction_id = ?
        """, ( total_paid, remaining_debt, trans_id))
     

        # Log the payment in the payments table, including product details
        cursor.execute("""
            INSERT INTO payments (transaction_id,customer_name, item_name, amount_paid, payment_mode, cheque_number, cheque_bank, cheque_clearance_date, entry_date_and_time,transaction_date, user_logged)
            VALUES (?, ?,?, ?, ?, ?,  ?, ?, CURRENT_TIMESTAMP,?, ?)
        """, (trans_id, customer,  product, remaining_payment, payment_mode, cheque_number, cheque_bank, cheque_clearance_date, tran_date, self.parent_window.user_manager.logged_in_user))
        log = f"{self.parent_window.user_manager.logged_in_user} received payment of GHS {remaining_payment} from {customer} in respect of transaction id: {trans_id}."
        log_text(log)
        #previous_payment = total_paid 
        self.receipt_data = [trans_id, customer, product,  quantity,  result[5], remaining_payment, remaining_debt, payment_mode,cheque_bank,]
        
        conn.commit()
        conn.close()
        
        if self.send_sms.isChecked():
            company = self.parent_window.company_name
            sms_message = f"GHS {remaining_payment} paid to {company} in respect of {product} purchased."
            if remaining_debt > 0:
                sms_message += f'\nRemaining debt is GHS {remaining_debt}'
                
            self.send_sms_notification(contact,  sms_message)
            #QMessageBox.information(self, "Success", "Sale recorded successfully.")
            
        #show print receipt before closing window
        if self.print_receipt.isChecked():
            self.show_print_dialog()
        self.accept()
        
    def create_sms_table(self):
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sms_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    

    def faya_sms(self, recipient, message):
        url = "https://fayasms.com/api/v1/send"
        data = {
            "key": FAYASMS_API_KEY,
            "sender_id": FAYASMS_SENDER_ID,
            "to": recipient,
            "message": message
        }

        try:
            response = requests.post(url, json=data)
            response_json = response.json()
            if response_json.get("status") == "success":
                return True  # SMS sent successfully
            else:
                return False  # SMS failed
        except requests.exceptions.RequestException:
            return False  # Device is offline
    
    
    def send_sms_notification(self, contact, message):        
        sent = self.faya_sms(contact, message)
        if not sent:
            self.queue_sms(contact, message) 
    
    def queue_sms(self, recipient, message):
        self.create_sms_table()
        
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sms_queue (recipient, message) VALUES (?, ?)", (recipient, message))
        conn.commit()
        conn.close()
        
    def send_queued_sms(self):
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        cursor.execute("SELECT id, recipient, message FROM sms_queue WHERE status = 'pending'")
        queued_sms = cursor.fetchall()

        for sms_id, recipient, message in queued_sms:
            if self.send_sms_notification(recipient, message):  # If SMS is sent successfully
                cursor.execute("DELETE FROM sms_queue WHERE id = ?", (sms_id,))  # Remove from queue

        conn.commit()
        conn.close()

    def show_print_dialog(self):
        self.print_payment_receipt()
        self.accept()
        """ Show receipt print dialog before closing the payment window 
        reply = QMessageBox.question(self, "Print Receipt", "Do you want to print the receipt now?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            self.print_payment_receipt()

        self.accept()  # Now close the window after print confirmation"""
        

        
    def generate_payment_receipt(self):
        """Generate a detailed sales receipt with bulk discounts and prompt payment discounts."""
        # Unpack receipt data
        trans_id, customer, items,  quantity,  past_debt, paid, remaining_debt, payment_mode,cheque_bank, = self.receipt_data 
        sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #{self.parent_window.company_name}
        receipt_text = f"""
        ****** SALES RECEIPT ******  
        =============================
        ROSEMER TRADING ENTERPRISE 
        Suame - Kumasi
        +233549350661 / +233509860256
        P.O. BOX 14821, Adum - Kumasi
        =============================
        -----------------------------------
        Transaction ID: {trans_id}
        Customer: {customer}
        Payment Date: {sale_date}
        Items Purchased:
        -----------------------------------
        """

        items = items.split(", ")
        #unit_price = list(map(float, unit_price.split(", ")))
        quantity = list(map(int, quantity.split(", ")))
        #bulk_discounted_price = list(map(float, bulk_discounted_price.split(", ")))
        #prompt_payment_discount = list(map(float, prompt_payment_discount.split(", ")))
        
        # Handle multiple items
        for i in range(len(items)):
            #original_price = unit_price[i]
            #discounted_price = bulk_discounted_price[i] if bulk_discounted_price[i] > 0 else original_price
            #prompt_discount = prompt_payment_discount[i]

            receipt_text += f"        {items[i]} - {quantity[i]} units\n" if i != 0 else f"{items[i]} - {quantity[i]} units\n"
            #receipt_text += f"        Unit Price: GHS {original_price:.2f}\n"
           
            '''
            if bulk_discounted_price[i] > 0:
                receipt_text += f"        Bulk Discounted Price: GHS {discounted_price:.2f}\n"
            
            if prompt_discount > 0:
                receipt_text += f"        Prompt Payment Discount: GHS {prompt_discount:.2f} applied\n"
            '''

            receipt_text += "        -----------------------------------\n"

        receipt_text += f"""
        Previously Owed: {currency_symbol} {past_debt:.2f}
        Amount Paid: {currency_symbol} {paid:.2f}
        Remaining Debt: {currency_symbol} {remaining_debt:.2f}
        Payment Mode: {payment_mode}
        """

        if payment_mode == "Cheque":
            receipt_text += f"Cheque Bank: {cheque_bank}\n"

        receipt_text += "    -----------------------------------\n"
        receipt_text += f"        Served by: {self.parent_window.user_manager.logged_in_user}\n"
        receipt_text += "        Thank you for your business!\n"

        return receipt_text

            

    def print_payment_receipt(self):
        """ Print the sales receipt or save as PDF if no printer is available """
        receipt_text = self.generate_payment_receipt()

        printer = QPrinter(QPrinter.HighResolution)
        
        try:
            dialog = QPrintDialog(printer, self)
            
            if dialog.exec_() == QDialog.Accepted:
                editor = QTextEdit()
                editor.setText(receipt_text)
                editor.print_(printer)
            else:
                #QMessageBox.information(self, "Print Cancelled", "Printing was cancelled.")
                e = "No Printer Connected"
                QMessageBox.warning(self, "Printer Error", f"Printing failed. Saving as PDF instead.\nError: {e}")
                
                # Fallback: Save as PDF
                pdf_filename  = "sales_receipt.pdf"
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName("sales_receipt.pdf")
                
                editor = QTextEdit()
                editor.setText(receipt_text)
                editor.print_(printer)

                QMessageBox.information(self, "Saved as PDF", "Receipt saved as sales_receipt.pdf")
                # Automatically open the saved PDF
                try:
                    if os.name == "nt":  # Windows
                        os.startfile(pdf_filename)
                    elif sys.platform == "darwin":  # macOS
                        subprocess.run(["open", pdf_filename])
                    else:  # Linux
                        subprocess.run(["xdg-open", pdf_filename])
                except Exception as open_error:
                    QMessageBox.warning(self, "Error Opening PDF", f"Failed to open {pdf_filename}.\nError: {open_error}")                
        
        except Exception as e:
            pass
        
        