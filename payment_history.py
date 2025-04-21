import sys, csv, requests
import sqlite3, os, subprocess 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, QTextEdit, QDialog, QSpinBox, QDateEdit, QDialogButtonBox, QCheckBox, QMenuBar, QMenu, QFileDialog)

from PyQt5.QtCore import Qt, QTimer, QDate, QStringListModel
from PyQt5.QtWidgets import QInputDialog,QGridLayout, QHBoxLayout, QTextEdit, QGroupBox, QAction, QSizePolicy, QCompleter
from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

import math

import datetime
from csv_to_pdf import csv_to_pdf

FAYASMS_API_KEY = "your_fayasms_api_key"
FAYASMS_SENDER_ID = "YourBusinessName"

currency_symbol = "\u20B5"


def log_text(text):
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Open the file in append mode (creates the file if it doesn't exist)
    with open("log.txt", "a") as file:
        # Write the timestamp followed by the input text
        file.write(f"[{timestamp}] {text}\n")

class PaymentHistoryWindow(QWidget):
    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sales/Payment Records - {}".format(database))
        self.data= database
        self.main_window = parent
        #self.main_window.setWindowTitle("Payment History")
        layout = QVBoxLayout()

        # Filter Section
        filter_layout = QHBoxLayout()
        self.customer_filter = QComboBox()
        self.product_filter = QLineEdit()
        self.product_filter.setPlaceholderText("Search by Product")

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))  

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())  
        
        if self.main_window.user_manager.logged_in_role == 'Administrator':
            self.reverse_payment_button = QPushButton("Reverse Payment")
            self.reverse_payment_button.clicked.connect(self.reverse_payment) 
        self.print_receipt = QPushButton("Reprint Receipt")
        self.print_receipt.clicked.connect(self.print_sales_receipt)

        self.load_customers()
        self.customer_filter.currentIndexChanged.connect(self.load_payment_history)
        self.product_filter.textChanged.connect(self.load_payment_history)
        self.start_date.dateChanged.connect(self.load_payment_history)
        self.end_date.dateChanged.connect(self.load_payment_history)

        filter_layout.addWidget(QLabel("Customer:"))
        filter_layout.addWidget(self.customer_filter)
        filter_layout.addWidget(QLabel("Product:"))
        filter_layout.addWidget(self.product_filter)
        filter_layout.addWidget(QLabel("Start Date:"))
        filter_layout.addWidget(self.start_date)
        filter_layout.addWidget(QLabel("End Date:"))
        filter_layout.addWidget(self.end_date)
        
        self.main_row_selected = -1;

        # Payment Table
        self.payment_table = QTableWidget()
        self.payment_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.payment_table.setColumnCount(9)
        self.payment_table.setHorizontalHeaderLabels(["Tansaction ID","Customer", "Product", f"Amount Paid {currency_symbol}  ", "Mode", "Cheque No.", "Bank", "Date","Payment Date"])
        self.payment_table.setColumnHidden(7,True) # Hide date column, this will be used to query the table to apply unique changes. Display rather the date set by user in the data entry
        # Enable sorting
        self.payment_table.setSortingEnabled(True)

        # Summary Section
        self.summary_label = QLabel(f"Total Paid: {currency_symbol}  0 | Total Outstanding: {currency_symbol}  0 |Total Sales Value: {currency_symbol}  0")
        
        # Export Buttons
        self.export_csv_button = QPushButton("Resend Queued SMS")
        self.export_pdf_button = QPushButton("Export PDF")
        #self.export_csv_button.clicked.connect(lambda: self.export_payments_csv("None"))
        self.export_csv_button.clicked.connect(lambda: self.send_queued_sms(relog=False))
        self.export_pdf_button.clicked.connect(self.export_payments_pdf)
         
        
        export_layout = QHBoxLayout()
        export_layout.addWidget(self.export_csv_button)
        export_layout.addWidget(self.export_pdf_button) 
        export_layout.addWidget(self.print_receipt)
        
        if self.main_window.user_manager.logged_in_role == 'Administrator':
            self.edit_payment_button = QPushButton("Edit Payment")
            self.edit_payment_button.clicked.connect(self.enable_payment_editing) 
            self.lock_payment_button = QPushButton("Lock in Edited")
            self.lock_payment_button.setEnabled(False)  # Initially disabled
            self.lock_payment_button.clicked.connect(self.lock_in_edited_payment) 
            export_layout.addWidget(self.reverse_payment_button)
            export_layout.addWidget(self.edit_payment_button)
            export_layout.addWidget(self.lock_payment_button)

        layout.addLayout(filter_layout)
        layout.addWidget(self.payment_table)
        layout.addWidget(self.summary_label)
        layout.addLayout(export_layout)
        self.setLayout(layout)

        self.load_payment_history()

    def load_customers(self):
        """Load customer names into the dropdown."""
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT customer_name FROM payments ORDER BY customer_name")
        customers = cursor.fetchall()
        self.customer_filter.clear()
        self.customer_filter.addItem("All Customers")
        for customer in customers:
            self.customer_filter.addItem(customer[0])
        conn.close()

    def format_products_and_quantities(self, products, quantities):
        product_list = products.split(", ")
        quantity_list = quantities.split(", ")
        formatted_text = "\n".join(f"{p.ljust(20)} - {q.rjust(3)}" for p, q in zip(product_list, quantity_list))
        return formatted_text

    def load_payment_history(self):
        """Load payments based on filters and update summary statistics."""
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        customer = self.customer_filter.currentText()
        product = self.product_filter.text().strip()
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        query = """SELECT transaction_id, customer_name, item_name, amount_paid, payment_mode, cheque_number, cheque_bank, entry_date_and_time, transaction_date 
                   FROM payments WHERE DATE(entry_date_and_time) BETWEEN ? AND ?"""
        params = [start_date, end_date]

        if customer and customer != "All Customers":
            query += " AND customer_name = ?"
            params.append(customer)
        if product:
            query += " AND item_name LIKE ?"
            params.append(f"%{product}%")

        query += " ORDER BY entry_date_and_time DESC"
        cursor.execute(query, params)
        records = cursor.fetchall()
        
        #fetch quantities 

        monospaced_font = QFont("Courier New", 10)  # Use a monospaced font consolas
        self.payment_table.setRowCount(len(records))
        self.payment_table.setWordWrap(True)  # Enable word wrap
        total_paid = 0
        for row, record in enumerate(records):
            for col, data in enumerate(record):
                if col == 2:  # Index 4 corresponds to 'product_name'
                    #product_names = data.split(", ") 
                    #fetch quantities
                    cursor.execute(""" SELECT quantity FROM customers WHERE transaction_id = ? """, (records[row][0],))
                    qty = cursor.fetchall()
                    #print(qty, qty[0])
                    combined_text = self.format_products_and_quantities(data, qty[0][0])
                    #combined_text = "\n".join(product_names)

                    cell_value = QTableWidgetItem(combined_text)
                    cell_value.setFont(monospaced_font)  # Set monospaced font
                    cell_value.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                    
                    # Allow cell to expand vertically
                    self.payment_table.setItem(row, col, cell_value)
                else:                    
                    if col == 3 : data = float(f'{data:.2f}')
                    self.payment_table.setItem(row, col, QTableWidgetItem(str(data)))
            total_paid += float(record[3])

        # Get outstanding debt
        cursor.execute("SELECT SUM(remaining_debt) FROM customers")
        result = cursor.fetchone()
        total_outstanding = result[0] if result and result[0] else 0

        # Update Summary
        self.summary_label.setText(f"<b> <font color='blue' size =3> Total Paid: {currency_symbol} {total_paid:.2f} </font> | <font color='red' size =3 >Total Outstanding: {currency_symbol} {total_outstanding:.2f} </font>  | <font size=3 color='green' >Total Sales Value: {currency_symbol} {total_outstanding+total_paid:.2f}</font></b>")
        # Resize row heights to fit contents
        self.payment_table.resizeRowsToContents()
        conn.close()
        
    
    def reverse_payment(self):
        """ Reverse a selected payment and restore previous state. """
        selected_row = self.payment_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a payment to reverse.")
            return

        trans_id = self.payment_table.item(selected_row, 0).text()  # Get transaction ID and payment date
        tran_time = self.payment_table.item(selected_row, 7).text()  # Get transaction ID and payment date
        customer = self.payment_table.item(selected_row, 1).text()  # Get customer name
        amount_paid = float(self.payment_table.item(selected_row, 3).text())  # Get paid amount 

        # Admin Authentication
        password, ok = QInputDialog.getText(self, "Admin Authentication", "Enter Your Password:", QLineEdit.Password)
        auth = self.main_window.user_manager.validate_user(self.main_window.user_manager.logged_in_user, password)
        if not ok or not auth:
            QMessageBox.warning(self, "Access Denied", "Invalid admin password.")
            return

        # Confirmation Dialog
        confirm = QMessageBox.question(self, "Confirm Reversal",
                                    f"Are you sure you want to reverse payment for Transaction {trans_id}?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return

        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        
                
        # Restore previous debt`
        cursor.execute("UPDATE customers SET remaining_debt = remaining_debt + ?, total_paid = total_paid - ? WHERE transaction_id = ?",
                    (amount_paid, amount_paid, trans_id))

        #log reversals in red color in either a new table/window or same database
        # Remove the payment record
        cursor.execute("DELETE FROM payments WHERE transaction_id = ? AND entry_date_and_time = ?", (trans_id,tran_time))
        log = f"{self.main_window .user_manager.logged_in_user} deleted payment with transaction id: {trans_id} and value {amount_paid}."
        log_text(log)
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Pa`yment reversed successfully.")
        self.load_payment_history()  # Refresh table
        return
    
    def calculate_remaining_debt_as_at(self, trans_id, date):
        """
        Returns sum of amount_paid for a transaction ID
        with payment dates strictly before the specified date
        """
        total = 0.0
        conn = None
        
        try:
            conn = sqlite3.connect(self.data)
            cursor = conn.cursor()
            
            # Parameterized query with explicit date comparison
            cursor.execute("""
                SELECT COALESCE(SUM(amount_paid), 0) 
                FROM payments 
                WHERE transaction_id = ?
                AND entry_date_and_time < ?
            """, (trans_id, date))
            
            total = cursor.fetchone()[0]
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0.0
        finally:
            if conn:
                conn.close()
        
        return float(total)
        
    
    def generate_payment_receipt(self):
        """Generate a detailed payment receipt from the payments database."""
      
        selected_row = self.payment_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a payment to reprint receipt.")
            return

        trans_id = self.payment_table.item(selected_row, 0).text()  # Get transaction ID and payment date
        tran_time = self.payment_table.item(selected_row, 7).text()  # Get transaction ID and payment date
        customer = self.payment_table.item(selected_row, 1).text()  # Get customer name 
        items = self.payment_table.item(selected_row, 2).text()  # Get items
        paid = self.payment_table.item(selected_row, 3).text()  # Get transaction amt
        #sour = self.payment_table.item(selected_row, 8).text()  # Get payment source
        payment_mode  = self.payment_table.item(selected_row, 4).text()  # Get customer name
        cheque_bank =  self.payment_table.item(selected_row, 6).text()
        
        
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()

        # Fetch payment details from database
        cursor.execute("""
            SELECT    entry_date_and_time, user_logged
            FROM payments WHERE entry_date_and_time = ?
        """, (tran_time,))
        payment_data = cursor.fetchone()
        conn.close()

        if not payment_data:
            return "*** PAYMENT RECEIPT ***\nTransaction not found."

        # Unpack data from database
        source = payment_data[0]
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT    unit_price, quantity, bulk_discount,  total_owed, remaining_debt
            FROM customers WHERE transaction_id = ?
        """, (trans_id,))
        quans = cursor.fetchone()
        conn.close()
        unit_price, quantity, bulk_discounted_price,total_owed, remaining_debt = quans
        # {self.main_window.company_name}
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
        Date: {tran_time}
        Customer: {customer}
        
        Items Purchased:
        -----------------------------------
        """

        items = items.split(", ")
        unit_price = list(map(float, unit_price.split(", ")))
        quantity = list(map(int, quantity.split(", ")))
        bulk_discounted_price = list(map(float, bulk_discounted_price.split(", "))) 
        
        # Handle multiple items
        for i in range(len(items)):
            original_price = unit_price[i]
            discounted_price = bulk_discounted_price[i] if bulk_discounted_price[i] > 0 else original_price 

            receipt_text += f"              {items[i]} - {quantity[i]} units\n" if i != 0 else f"{items[i]} - {quantity[i]} units\n"
            receipt_text += f"        Unit Price: {currency_symbol}  {original_price:.2f}\n"
            
            if bulk_discounted_price[i] > 0:
                receipt_text += f"        Bulk Discounted Price: {currency_symbol}  {discounted_price:.2f}\n"
             

            receipt_text += "        -----------------------------------\n"
            
        prev_debt = self.calculate_remaining_debt_as_at(trans_id, tran_time)
        remaining_debt = float(total_owed) - prev_debt - float(paid)
        
        prev_owe = ''
        if prev_debt > 0:
            prev_owe = f"\n        Previous Payment: {currency_symbol}  {prev_debt}"
        receipt_text += f"""
        Total Cost: {currency_symbol}  {total_owed}{prev_owe}
        Amount Paid: {currency_symbol}  {paid}
        Remaining Debt: {currency_symbol}  {remaining_debt}
        Payment Mode: {payment_mode}
        """ 
        if payment_mode == "Cheque":
            receipt_text += f"Cheque Bank: {cheque_bank}\n"

        receipt_text += " -----------------------------------\n"
        receipt_text += f"        Served by: {payment_data[1]}\n"
        receipt_text += "        Thank you for your business!\n"

        return receipt_text

     
    def enable_payment_editing(self):
        """Enable editing for selected payment row."""
        selected_row = self.payment_table.currentRow()
        self.main_row_selected = selected_row
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a payment to edit.")
            return

        #get the time of the transaction to use it as a key to query payments table so that even if user edits transaction time, query will be successful
        self.query_time = self.payment_table.item(selected_row, 7).text()
        # Admin Authentication
        password, ok = QInputDialog.getText(self, "Admin Authentication", "Enter Your Password:", QLineEdit.Password)
        auth = self.main_window.user_manager.validate_user(self.main_window.user_manager.logged_in_user, password)
        if not ok or not auth:
            QMessageBox.warning(self, "Access Denied", "Invalid admin password.")
            return
        
        # Enable editing in the entire table (needed for changes to take effect)
        self.payment_table.setEditTriggers(QTableWidget.AllEditTriggers)

        # Allow editing for amount_paid, payment_mode, cheque_number, cheque_bank, cheque_clearance_date
        editable_columns = [3, 4, 5, 6, 7]  # Corresponding column indexes

        for col in editable_columns:
            item = self.payment_table.item(selected_row, col)
            if not item:
                item = QTableWidgetItem("")
                self.payment_table.setItem(selected_row, col, item)

            item.setFlags(item.flags() | Qt.ItemIsEditable)  # Enable editing

        # Enable "Lock in Edited" button
        self.lock_payment_button.setEnabled(True)

        QMessageBox.information(self, "Edit Mode Activated", "You can now edit the selected payment details.")
   

    def lock_in_edited_payment(self):
        """Save edited payment details and update customer records."""
        selected_row = self.payment_table.currentRow()
        if selected_row == -1 :
            QMessageBox.warning(self, "Error", "No payment selected.")
            return
        if selected_row != self.main_row_selected:
            selected_row = self.main_row_selected
            QMessageBox.warning(self, "Error", "Changes will be applied only to the row you selected initially")

        trans_id = self.payment_table.item(selected_row, 0).text()  # Transaction ID
        payment_mode = self.payment_table.item(selected_row, 4).text()  # Updated payment mode
        cheque_number = self.payment_table.item(selected_row, 5).text()
        cheque_bank = self.payment_table.item(selected_row, 6).text()
        trans_time = self.query_time #self.payment_table.item(selected_row, 7).text() 
        try:            
            amount_paid = abs(float(self.payment_table.item(selected_row, 3).text()))  # Updated amount 
        except ValueError as e:
            QMessageBox.warning(self, "Error", "Enter numeric value into amount paid!")            
            self.payment_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.lock_payment_button.setEnabled(False) 
            return 
        
        #print("amount is ", amount_paid)

        # Admin Authentication
        password, ok = QInputDialog.getText(self, "Admin Authentication", "Enter Your Password:", QLineEdit.Password)
        auth = self.main_window.user_manager.validate_user(self.main_window.user_manager.logged_in_user, password)
        if not ok or not auth:
            QMessageBox.warning(self, "Access Denied", "Invalid admin password.")
            return

        # Confirm Changes
        confirm = QMessageBox.question(self, "Confirm Edit",
                                    f"Apply these changes to Transaction {trans_id}?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return

        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()

        # Fetch previous payment amount
        cursor.execute("SELECT amount_paid FROM payments WHERE entry_date_and_time = ?", (trans_time,))
        previous_payment = cursor.fetchone()
        if not previous_payment:
            QMessageBox.warning(self, "Error", "Payment record not found.")
            conn.close()
            # Disable editing again
            self.payment_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.lock_payment_button.setEnabled(False)
            QMessageBox.information(self, "Success", "Payment details updated successfully.")
            self.load_payment_history()  # Refresh table
            return

        previous_amount = previous_payment[0]
        amount_difference = amount_paid - previous_amount  # New amount - old amount

        # Update payments table
        cursor.execute("""
            UPDATE payments SET amount_paid=?, payment_mode=?, cheque_number=?, cheque_bank=?
            WHERE entry_date_and_time=?
        """, (amount_paid, payment_mode, cheque_number, cheque_bank,  trans_time))

        # Update customers table (total_paid & remaining_debt must reflect change)
        cursor.execute("""
            UPDATE customers SET total_paid = total_paid + ?, remaining_debt = remaining_debt - ?
            WHERE transaction_id=?
        """, (amount_difference, amount_difference, trans_id))

        conn.commit()
        conn.close()
        log = f"{self.main_window .user_manager.logged_in_user} edited payment with transaction id: {trans_id}. New amount:   {amount_paid}"
        log_text(log)
 
        # Disable editing again
        self.payment_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.lock_payment_button.setEnabled(False) 
        QMessageBox.information(self, "Success", "Payment details updated successfully.")
        self.load_payment_history()  # Refresh table



    def export_payments_csv(self, ff="None", show_success = True):
        """Export payment records to CSV."""
    
        if ff == "None":
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)", options=QFileDialog.Options())
        else:
            file_path = os.getcwd()+'\\'+ff +".csv"
        if file_path:
            data = []
            for row in range(self.payment_table.rowCount()):
                row_data = [self.payment_table.item(row, col).text() if self.payment_table.item(row, col) else "" for col in range(self.payment_table.columnCount())]
                data.append(row_data)

            headers = self.get_table_headers(self.payment_table)
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)

            if(show_success): QMessageBox.information(self, "Success", "Export completed successfully!")
    
    def get_table_headers(self, table_widget):
        """Retrieve the column headers of the given QTableWidget."""
        headers = []
        for col in range(table_widget.columnCount()):
            headers.append(table_widget.horizontalHeaderItem(col).text())
        return headers        


    def export_payments_pdf(self):
        """Export payment records to a PDF file."""
        #first convert to csv, then convert from csv to pdf using reportlab module        
        self.export_payments_csv("temp",False)
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PDF Files (*.pdf)", options=QFileDialog.Options())
        if file_path:         
            csv_to_pdf("temp.csv", file_path)
            os.remove('temp.csv')
            

    def show_print_dialog(self):
        """ Show receipt print dialog before closing the sales window """
        reply = QMessageBox.question(self, "Print Receipt", "Do you want to print the receipt now?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            self.print_sales_receipt()

        self.accept()  # Now close the window after print confirmation
  
    

    def print_sales_receipt(self):
        """ Print the sales receipt or save as PDF if no printer is available """
        receipt_text = self.generate_payment_receipt()
        if not receipt_text: return 
        printer = QPrinter(QPrinter.HighResolution)
        
        log = f"{self.main_window.user_manager.logged_in_user} reprinting receipt"
        log_text(log)
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
    
    
    def send_sms_notification(self, contact, message, log=True):        
        sent = self.faya_sms(contact, message)
        if not sent and log:
            self.queue_sms(contact, message) 
    
    def queue_sms(self, recipient, message):
        self.create_sms_table()
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sms_queue (recipient, message) VALUES (?, ?)", (recipient, message))
        conn.commit()
        conn.close()
        
    def send_queued_sms(self,relog=False):
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, recipient, message FROM sms_queue WHERE status = 'pending'")
            queued_sms = cursor.fetchall()

            for sms_id, recipient, message in queued_sms:
                if self.send_sms_notification(recipient, message,log=False):  # If SMS is sent successfully
                    cursor.execute("DELETE FROM sms_queue WHERE id = ?", (sms_id,))  # Remove from queue
                    QMessageBox.information(self, "Succes", "SMS sent successfully to {}.".format(recipient))
                else:                
                    QMessageBox.warning(self,"SMS sending failed", f"Sending SMS to {recipient} failed")
            conn.commit()
        except:
            QMessageBox.warning(self,"No SMS Queue", "No record of SMS found")
        finally:
            conn.close()