import sys
import sqlite3, os, subprocess  
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, QTextEdit, QDialog, QSpinBox, QDateEdit, QDialogButtonBox, QCheckBox, QMenuBar, QMenu, QFileDialog)

from PyQt5.QtCore import Qt, QTimer, QDate, QStringListModel
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QTextEdit, QGroupBox, QAction, QSizePolicy, QCompleter,QDoubleSpinBox
from PyQt5.QtGui import QPalette, QIntValidator, QDoubleValidator
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from datetime import datetime
import requests 
from edit_inventory import TransactionIDGenerator
#from sale_receipt_pdf import SalesReceiptPDF       

FAYASMS_API_KEY = "your_fayasms_api_key"
FAYASMS_SENDER_ID = "YourBusinessName"


class SalesWindow(QDialog):
    def __init__(self, database, parent):
        super().__init__(parent)
        self.setWindowTitle("Record Sale")
        self.setGeometry(200, 200, 500, 400)
        self.data = database
        self.current_transaction_id = ""
        self.receipt_data = []
        self.parent_window = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Customer Name")
        self.customer_location = QLineEdit()
        self.customer_location.setPlaceholderText("Customer Location")
        self.customer_contact = QLineEdit()
        self.customer_contact.setPlaceholderText("Customer Contact")
        contact_validator = QRegExpValidator(QRegExp(r"^\d{10}$"), self.customer_contact)
        self.customer_contact.setValidator(contact_validator)
        
        # Load auto-complete suggestions from the database
        self.load_customer_suggestions()

        self.product_table = QTableWidget()
        self.product_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.product_table.setColumnCount(3)  # Added two more columns
        self.product_table.setHorizontalHeaderLabels(["Product", "Quantity", "Discounted Price"])
        self.load_inventory_items()
        
        date_layout = QHBoxLayout()
        self.tran_date = QDateEdit()
        self.tran_date.setCalendarPopup(True)
        self.tran_date.setDate(QDate.currentDate())  
        date_layout.addWidget(QLabel("Transaction Date"))
        date_layout.addWidget(self.tran_date)

        self.amount_paid = QLineEdit()
        self.amount_paid.setPlaceholderText("Amount Paid")
        validator = QDoubleValidator(0.0, 999999.99, 2)  # Min 0.0, Max 999999.99, 2 decimal places
        validator.setNotation(QDoubleValidator.StandardNotation)  # Standard notation
        self.amount_paid.setValidator(validator)
        self.payment_mode = QComboBox()
        self.payment_mode.addItems(["Cash", "Cheque", "Credit"])
        self.payment_mode.currentIndexChanged.connect(self.toggle_cheque_details)
        #self.product_table.cellChanged.connect(self.calculate_total_due)  # Detect cell changes
        date_layout.addWidget(QLabel("Amount Paid: "))
        date_layout.addWidget(self.amount_paid)

        pay_layout = QHBoxLayout()
        pay_layout.addWidget(QLabel("Mode of Payment:"))
        pay_layout.addWidget(self.payment_mode)
        pay_layout.addStretch()
        self.cheque_details = QWidget()
        cheque_layout = QVBoxLayout()
        self.cheque_number = QLineEdit()
        self.cheque_number.setPlaceholderText("Cheque Number")
        self.cheque_bank = QLineEdit()
        self.cheque_bank.setPlaceholderText("Bank")
        self.cheque_clearance_date = QDateEdit()
        self.cheque_clearance_date.setDate(QDate.currentDate())
        self.cheque_clearance_date.setCalendarPopup(True)
        cheque_Hor = QHBoxLayout()
        cheque_Hor.addWidget(self.cheque_number)
        cheque_Hor.addWidget(self.cheque_bank)
        cheque_layout.addLayout(cheque_Hor)
        #cheque_layout.addWidget(self.cheque_number)
        #cheque_layout.addWidget(self.cheque_bank)
        cheq_clear = QHBoxLayout()
        cheq_clear.addWidget(QLabel("Cheque Clearance Date: "))
        cheq_clear.addWidget(self.cheque_clearance_date)
        cheque_layout.addLayout(cheq_clear)
        #cheque_layout.addWidget(self.cheque_clearance_date)
        self.cheque_details.setLayout(cheque_layout)
        self.cheque_details.setVisible(False)         
        
        misc_layout = QHBoxLayout() 
        self.print_receipt = QCheckBox("Print Receipt")
        self.send_sms = QCheckBox("Send SMS Alert")
        misc_layout.addWidget(self.print_receipt)
        misc_layout.addWidget(self.send_sms)
        #self.print_receipt.stateChanged.connect(self.show_print_dialog)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.record_sale)
        self.button_box.rejected.connect(self.reject)        
        
        #customer_layout = QGridLayout()
        blayout = QVBoxLayout()
        customer_labels = QGroupBox("Customer Details")
        customer_layout = QHBoxLayout() #QHBoxLayout() 
        customer_layout.addWidget(QLabel("Customer Name:"))
        customer_layout.addWidget(QLabel("Customer Location:"))
        customer_layout.addWidget(QLabel("Customer Contact:"))
        
        customer_edit = QHBoxLayout()
        customer_editss = QGroupBox("Customer Details")
        customer_edit.addWidget(self.customer_name)
        customer_edit.addWidget(self.customer_location)
        customer_edit.addWidget(self.customer_contact) 
        
        customer_labels.setLayout(customer_layout)
        customer_editss.setLayout(customer_edit) 
        blayout.addWidget(customer_editss )

        layout.addLayout(blayout)            
        layout.addWidget(QLabel("Select Products:"))
        layout.addWidget(self.product_table) 
        layout.addLayout(date_layout) 
        layout.addLayout(pay_layout)
        layout.addWidget(self.cheque_details)
        layout.addLayout(misc_layout) 
        
        layout.addWidget(self.button_box)   
        self.setLayout(layout)    
        
    def load_customer_suggestions(self):
        """ Load customer data for auto-completion and set up bi-directional auto-fill """
        conn = sqlite3.connect(self.data)
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
                           
            
    def generate_transaction_id(self):
        obj = TransactionIDGenerator(self.data)
        return obj.generate_id()    

    def load_inventory_items(self):
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        cursor.execute("SELECT item_name FROM inventory")
        items = cursor.fetchall()
        conn.close()

        self.product_table.setRowCount(len(items))
        for row, item in enumerate(items):
            item_name = QTableWidgetItem(item[0])
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            self.product_table.setItem(row, 0, item_name)
            quantity_input = QSpinBox()
            quantity_input.setMaximum(9999)
            quantity_input.setMinimum(0)
            quantity_input.valueChanged.connect(self.calculate_total_due)  # Connect value change
            self.product_table.setCellWidget(row, 1, quantity_input)
            bulk_discount = QDoubleSpinBox() 
            bulk_discount.setMaximum(9999) 
            bulk_discount.setMinimum(0)
            bulk_discount.valueChanged.connect(self.calculate_total_due)  # Connect
            self.product_table.setCellWidget(row, 2, bulk_discount) 


    def calculate_total_due(self):
        """ Calculate total due when quantity or discounted price changes """
        total_due = 0.0
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        cursor.execute("SELECT unit_price FROM inventory")
        uprice = cursor.fetchall()
        conn.close()
        #print("called")
        for row in range(self.product_table.rowCount()):
            quantity_item = self.product_table.cellWidget(row, 1)
            disc_price_item = self.product_table.cellWidget(row, 2)
            u_price = uprice[row]
            #print(u_price)
            price_item = u_price[0] if float(disc_price_item.value()) == 0 else min(float(disc_price_item.value()), u_price[0])

            if quantity_item and price_item:
                try:
                    quantity = int(quantity_item.value()) 
                    total_due += quantity * price_item
                except ValueError:
                    continue  # Skip rows with invalid data
        
        self.amount_paid.setPlaceholderText(f"{total_due:.2f}")


    def toggle_cheque_details(self):
        self.cheque_details.setVisible(self.payment_mode.currentText() == "Cheque")

    def get_selected_products(self):
        selected_products = []
        for row in range(self.product_table.rowCount()):
            item = self.product_table.item(row, 0).text()
            quantity = self.product_table.cellWidget(row, 1).value()
            bulk_discount = self.product_table.cellWidget(row, 2).value() 

            if quantity > 0:
                selected_products.append((item, quantity, bulk_discount))
        return selected_products

    def contact_validation(self, contact):
        if len(contact) != 10:
            return False
        if not contact.isdigit():
            return False
        if not contact.startswith("0"):
            return False

    def record_sale(self):
        customer = self.customer_name.text().strip()
        location = self.customer_location.text().strip()
        contact = self.customer_contact.text().strip() 
        tran_date = self.tran_date.date().toString("ddd, dd MMM yyyy")
        selected_products = self.get_selected_products()
        payment_mode = self.payment_mode.currentText()
        paid = float(self.amount_paid.text()) if self.amount_paid.text() else 0.0
        cheque_number = self.cheque_number.text() if payment_mode == "Cheque" else None
        cheque_bank = self.cheque_bank.text() if payment_mode == "Cheque" else None
        cheque_clearance_date = self.cheque_clearance_date.date().toString("yyyy-MM-dd") if payment_mode == "Cheque" else None
        cost_of_sales_per_product = []

        if not customer or not contact or not selected_products:
            QMessageBox.warning(self, "Error", "Please fill all required fields and select products.")
            return
        
        if self.contact_validation(contact) == False:
            QMessageBox.warning(self, "Error", "Invalid Contact Number")
            return        

        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()

        total_owed = 0
        insufficient_stock_items = []
        items = ""
        qty = ""
        b_disc = ""  
        u_price = ""
        trans_id = self.generate_transaction_id()
        #items = []
        products_number = len(selected_products)
        counter = 0
        
        for item, quantity, bulk_discount in selected_products:
            counter += 1
            cursor.execute("SELECT unit_price, quantity_remaining FROM inventory WHERE item_name = ?", (item,))
            result = cursor.fetchone()
            unit_price, stock_remaining = result
            
            if quantity > stock_remaining:
                insufficient_stock_items.append(item)
                continue  # Skip this item            
            
            if quantity <= stock_remaining:            
                adder = ", " if counter < products_number else ""
                #items.append(item) # json.dumps(items)
                items += item + adder if len(selected_products) > 1 else item
                qty += str(quantity) + adder if len(selected_products) > 1 else str(quantity)
                b_disc += str(bulk_discount) + adder if len(selected_products) > 1 else str(bulk_discount) 
                u_price += str(result[0]) + adder if len(selected_products) > 1 else str(result[0])          
                
                if not result:
                    QMessageBox.warning(self, "Error", f"Item '{item}' not found in inventory.")
                    continue            
                applied_price = unit_price
                if bulk_discount > 0:
                    applied_price = bulk_discount  
                item_total = quantity * applied_price
                total_owed += item_total  # Accumulate total owed
                cost_of_sales_per_product.append((item, bulk_discount))

                cursor.execute("""
                    INSERT INTO sales (customer_name, location, contact, item_name, quantity, total_owed, amount_paid, remaining_debt, payment_mode, sale_date, user_logged)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'), ?)
                """, (customer, location, contact, item, quantity, item_total, 0, item_total, payment_mode, self.parent_window.user_manager.logged_in_user))
                
                cursor.execute("""
                    UPDATE inventory 
                    SET quantity_issued = quantity_issued + ?, quantity_remaining = quantity_remaining - ? 
                    WHERE item_name = ?
                """, (quantity, quantity, item))


        if insufficient_stock_items:
            QMessageBox.warning(self, "Stock Warning", f"Not enough stock for: {', '.join(insufficient_stock_items)}. These items were not added.")
 
        remaining_debt = total_owed - paid

        if total_owed > 0:
            cursor.execute("""
                UPDATE sales SET amount_paid = ?, remaining_debt = ? 
                WHERE customer_name = ? AND remaining_debt = total_owed
            """, (paid, remaining_debt, customer))

        if items:
            cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            cursor.execute("""
                INSERT INTO customers (transaction_id,name, location, contact, product_name,unit_price, quantity, bulk_discount, total_owed, total_paid, remaining_debt, entry_date_and_time,transaction_date, user_logged) 
                VALUES (?,?, ?,?,?,?,?, ?, ?,?, ?, ?,?,?) 
                ON CONFLICT(transaction_id) DO NOTHING
            """, (trans_id, customer, location, contact, items,u_price,qty,b_disc, total_owed, paid, remaining_debt, cur_time, tran_date, self.parent_window.user_manager.logged_in_user))
            
            
            cursor.execute("""
                INSERT INTO customers_data (name, location, contact) 
                VALUES (?,?,?) 
                ON CONFLICT(contact) DO NOTHING
            """, (customer, location, contact))
            
            
            log = f"{self.parent_window.user_manager.logged_in_user} sold {items} to {customer} for an amount of {total_owed}. Transaction id is: {trans_id}"
            self.log_text(log)
        
            # Log the payment in the payments table, including product details
         # Log the payment in the payments table, including product details
        
        if paid > 0 and items: 
            try:            
                cursor.execute("""
                        INSERT INTO payments (transaction_id,customer_name, item_name, amount_paid, payment_mode, cheque_number, cheque_bank, cheque_clearance_date,entry_date_and_time,transaction_date, user_logged)
                        VALUES (?,?, ?, ?, ?, ?, ?,?, ?,?,?)
                    """, (trans_id,customer, items, paid, payment_mode, cheque_number, cheque_bank, cheque_clearance_date, str(cur_time), tran_date, self.parent_window.user_manager.logged_in_user))
                conn.commit()
                #print("Logging about to begin!")
                log = f"{self.parent_window.user_manager.logged_in_user} received GHS {paid} in respect of {items} purchased."
                self.log_text(log)
                if cursor.rowcount > 0: 
                    QMessageBox.information(self, "Success", "Sale recorded successfully.")
                else:
                    QMessageBox.warning(self, "Error", "Insert Failed.")
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Error", f"Error: {e}")        
        
        if items:
            self.receipt_data = [trans_id, customer, location, contact, items,u_price,qty,b_disc, total_owed, paid, remaining_debt,payment_mode,cheque_bank,]
        conn.commit()
        conn.close() 
        
        if self.send_sms.isChecked() and items:         
            sms_message = f"GHS {paid} paid to {self.parent_window.company_name} in respect of {items} purchased."
            if remaining_debt > 0:
                sms_message += f'\nRemaining debt is GHS {remaining_debt}'
                
            self.send_sms_notification(contact,  sms_message)
            #QMessageBox.information(self, "Success", "Sale recorded successfully.")
        
        #show print dialog before closing the sales window
        if self.print_receipt.isChecked() and items: 
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
       
    def toggle_cheque_details(self):
        self.cheque_details.setVisible(self.payment_mode.currentText() == "Cheque")  

    def show_print_dialog(self):
        self.print_sales_receipt()
        self.accept()
        """ #Show receipt print dialog before closing the sales window 
        reply = QMessageBox.question(self, "Print Receipt", "Do you want to print the receipt now?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            self.print_sales_receipt()

        self.accept()  # Now close the window after print confirmation"""
    
    '''
    def generate_sales_receipt_pdf(self):
        receipt_pdf = SalesReceiptPDF
        a = receipt_pdf.generate_sales_receipt(self.receipt_data,self.parent_window.user_manager.logged_in_user)
    '''
        
    def generate_sales_receipt(self):
        """Generate a detailed sales receipt with bulk discounts """
        # Unpack receipt data
        trans_id, customer, location, contact, items, unit_price, quantity, bulk_discounted_price,  total_owed, paid, remaining_debt, payment_mode, cheque_bank = self.receipt_data

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
        Date: {sale_date}
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

            receipt_text += f"        {items[i]} - {quantity[i]} units\n" if i != 0 else f"{items[i]} - {quantity[i]} units\n"
            receipt_text += f"        Unit Price: GHS {original_price:.2f}\n"
            
            if bulk_discounted_price[i] > 0:
                receipt_text += f"        Bulk Discounted Price: GHS {discounted_price:.2f}\n"
            

            receipt_text += "        -----------------------------------\n"

        receipt_text += f"""
        Total Cost: GHS {total_owed:.2f}
        Amount Paid: GHS {paid:.2f}
        Remaining Debt: GHS {remaining_debt:.2f}
        Payment Mode: {payment_mode}
        """

        if payment_mode == "Cheque":
            receipt_text += f"Cheque Bank: {cheque_bank}\n"

        receipt_text += " -----------------------------------\n"
        receipt_text += f"        Served by: {self.parent_window.user_manager.logged_in_user}\n"
        receipt_text += "        Thank you for your business!\n"

        return receipt_text

        
    

    def print_sales_receipt(self):
        """ Print the sales receipt or save as PDF if no printer is available """
        receipt_text = self.generate_sales_receipt()

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
        
    def log_text(self, text):
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Open the file in append mode (creates the file if it doesn't exist)
        with open("log.txt", "a") as file:
            # Write the timestamp followed by the input text
            file.write(f"[{timestamp}] {text}\n")