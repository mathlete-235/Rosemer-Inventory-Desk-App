import sqlite3, os, csv, shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, QTextEdit, QDialog, QSpinBox, QDateEdit, QDialogButtonBox, QCheckBox, QMenuBar, QMenu, QFileDialog)

from PyQt5.QtCore import Qt, QTimer, QDate, QStringListModel, QEvent
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QTextEdit, QGroupBox, QAction, QSizePolicy, QCompleter
from PyQt5.QtGui import QPalette, QDoubleValidator, QIntValidator
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QSize
  
 
from customers import CustomersWindow
from payment_history import PaymentHistoryWindow
from payment import PaymentWindow
from edit_inventory import EditInventoryDialog
from sales import SalesWindow
from csv_to_pdf import csv_to_pdf
from user_mgt import UserManagementDialog
from home_view import HomeView
import datetime
from import_tables import ImportTableDialog
#from manage_customer import ManageCustomersWindow
from customer_manage import ManageCustomersWindow
from themes import *

currency_symbol = "\u20B5"


#add this method to handle dynamic tabel contect changes
class AutoResizeTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.horizontalHeader().sectionResized.connect(self.trigger_resize)
        self.verticalHeader().sectionResized.connect(self.trigger_resize)
    
    def trigger_resize(self):
        if self.isVisible():
            self.window().adjust_window_size()

class MainWindow(QMainWindow):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager # User system integrated
        self.create_database("_temp__.db")
        
        self.setGeometry(100, 100, 740, 450)
        self.database_name = self.get_last_opened_database()  # Load last used file or default 
        self.setWindowTitle("Home - {}".format(self.database_name))
        self.company_name = self.get_company_name()
        # Create a stacked widget to manage multiple views
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        
        self.setMinimumSize(400, 300)  # Set reasonable minimum dimensions        
        
        self.resize_animation = None  # Track active animation
        #self.menuBar().installEventFilter(self)  # Add event filter for menu bar
        
        #self.table = AutoResizeTable(self)
        

        # Create Main Inventory View
        self.inventory_view = QWidget()
        self.stacked_widget.addWidget(self.inventory_view)  # Index 0

        # Create Customer View
        self.customer_view = CustomersWindow(self.database_name, self)
        self.stacked_widget.addWidget(self.customer_view)  # Index 1
        
        self.window_titles = ("Inventory", "Sales Records", "Payment Records", 'Home', "Customer Records")
        # Create Payment View
        self.payment_history_view = PaymentHistoryWindow(self.database_name, self)
        self.stacked_widget.addWidget(self.payment_history_view)  # Index 2
        #Create Hove view
        
        self.home_view = HomeView(self, self.user_manager)
        self.stacked_widget.addWidget(self.home_view) #index 3
        self.stacked_widget.setCurrentIndex(3)
        # Show the main view initially                
        
        self.customer_base = ManageCustomersWindow(self.database_name, self)
        self.stacked_widget.addWidget(self.customer_base) #index 4

        self.stacked_widget.currentChanged.connect(self.adjust_window_size)
       
        
        # Load user-specific logout timer
        self.logout_timeout = self.get_user_logout_time() * 60 * 1000  # Convert minutes to milliseconds
        self.inactivity_timer = QTimer(self)
        self.inactivity_timer.timeout.connect(self.auto_logout)
        self.reset_inactivity_timer()

        # Track user activity
        self.installEventFilter(self)
        
        self.initUI() 
        self.load_theme()
        


        #self._current_tables[self.inventory_tabl] 
    
    def initUI(self):
        self.menubar = self.menuBar()     
        
        self.file_menu = self.menubar.addMenu("File")
        a = self.get_current_view()
        if a == 3: self.file_menu.menuAction().setVisible(False)        
        
        self.home_action = QAction("🏠 Home", self)
        self.home_action.triggered.connect(self.show_home)
        self.menubar.addAction(self.home_action)

        self.inventory_action = QAction("📦 Inventory", self)
        self.inventory_action.triggered.connect(self.show_main_view)
        self.menubar.addAction(self.inventory_action)

        self.payment_action = QAction("💰 Payment Records", self)
        self.payment_action.triggered.connect(self.open_payment_history)
        self.menubar.addAction(self.payment_action)

        self.customers_action = QAction("🛒 Sales", self)
        self.customers_action.triggered.connect(self.open_customers_window)
        self.menubar.addAction(self.customers_action)

        self.customers_database = QAction("👥 Customers", self)
        self.customers_database.triggered.connect(self.open_manage_customers)
        self.menubar.addAction(self.customers_database)
        
        self.user_menu = self.menubar.addMenu("User")
        self.settings_menu = self.menubar.addMenu("Options") 
        settings_action = self.settings_menu.addAction("Preferences") 
        
        settings_action.triggered.connect(self.open_settings_dialog)

        if self.user_manager.logged_in_role == 'Administrator':
            add_user_action = self.user_menu.addAction("Add User")
            add_user_action.triggered.connect(self.user_manager.open_add_user_dialog)
            delete_user_action = self.user_menu.addAction("Delete User")
            delete_user_action.triggered.connect(self.user_manager.open_delete_user_dialog)
        reset_password_action = self.user_menu.addAction("Reset Password")
        reset_password_action.triggered.connect(self.user_manager.open_reset_password_dialog) 
        
        new_action = self.file_menu.addAction("New File")
        open_action = self.file_menu.addAction("Open File")
        save_as_action = self.file_menu.addAction("Save as ...")
        export_action = self.file_menu.addAction("Export Table to CSV")
        export_pdf = self.file_menu.addAction("Export Table to PDF")
        import_action = self.file_menu.addAction("Import Tables")
        exit_action = self.file_menu.addAction("Exit")
        
        new_action.triggered.connect(self.new_file)
        open_action.triggered.connect(self.open_file)
        save_as_action.triggered.connect(self.save_database_as)
        export_action.triggered.connect(lambda: self.export_to_csv("None", True))
        export_pdf.triggered.connect(self.export_to_pdf)
        import_action.triggered.connect(self.import_file)
        exit_action.triggered.connect(self.closeEvent)                       
        
        self.inventory_table = QTableWidget()
        self.inventory_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.inventory_table.setColumnCount(7)
        self.inventory_table.setHorizontalHeaderLabels(["Item Name", "Date Received", f"Unit Price {currency_symbol}", "Quantity Received", "Quantity Issued", "Quantity Remaining", f"Total Cost {currency_symbol}"])
        
        # Enable sorting
        self.inventory_table.setSortingEnabled(True)
        self.load_inventory()   
        self.adjust_window_size()    
         
        layout = QVBoxLayout()
        layout.addWidget(self.inventory_table)
        
        # === Buttons Section (Grouped) ===
        button_layout = QGridLayout()
        # Group 1: Sales Actions
        sales_group = QGroupBox("Sales Actions")
        sales_layout = QHBoxLayout()
        self.btn_sales = QPushButton("New Sale")
        self.btn_sales.clicked.connect(lambda: self.open_sales_window(self))
        self.payment_button = QPushButton("Make Payment", self)
        self.payment_button.clicked.connect(self.open_payment_window)  
        sales_layout.addWidget(self.btn_sales)
        sales_layout.addWidget(self.payment_button)  
        sales_group.setLayout(sales_layout)
                
        # Group 2: Inventory Management
        inventory_group = QGroupBox("Inventory Management")
        inventory_layout = QHBoxLayout()
        
        if self.user_manager.logged_in_role == 'Administrator':
            self.add_inventory_button = QPushButton("Add Stock")
            self.add_inventory_button.clicked.connect(self.open_add_inventory_dialog)
            self.edit_inventory_button = QPushButton("Edit Stock Info")
            self.edit_inventory_button.clicked.connect(self.edit_inventory_item)  
            self.delete_inventory_button = QPushButton("Delete Stock")
            self.delete_inventory_button.clicked.connect(self.delete_inventory_item)
            inventory_layout.addWidget(self.add_inventory_button)
            inventory_layout.addWidget(self.edit_inventory_button)
            inventory_layout.addWidget(self.delete_inventory_button)
        inventory_group.setLayout(inventory_layout)
        
        # === Add Groups to Button Layout ===
        button_layout.addWidget(sales_group, 0, 1)
        button_layout.addWidget(inventory_group, 0, 0)
        #button_layout.addWidget(reports_group, 1, 0, 1, 2)  # Span two columns

        # Add Button Layout to Main Layout
        layout.addLayout(button_layout)          
        container = QWidget()
        container.setLayout(layout)
        self.inventory_view.setLayout(layout)
        #self.setCentralWidget(container)
        
    def get_company_name(self):        
        conn = sqlite3.connect(self.user_manager.database)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key='company_name'")
        result = cursor.fetchone()
        if result:
            return result[0]
        return "Enter Your Company name in Settings"

    def open_user_management(self):
        """Open the User Management Dialog."""
        user_mgmt_dialog = UserManagementDialog(self.user_manager, self)
        user_mgmt_dialog.exec_()
             
    
    def open_settings_dialog(self):
        """Open the Settings Dialog."""
        dialog = SettingsDialog(self.user_manager)
        dialog.exec_()
    
        
    def adjust_window_size(self, additional_table = None):                
        table = None
        table2 = None
        self.get_current_view() 
        if self.current_widget == 0 :
            table = self.inventory_table
        elif  self.current_widget == 1 : 
            table = self.customer_view.customer_table        
        elif self.current_widget == 4 :
            table = self.customer_base.customer_records_table
            table2 = self.customer_base.transaction_history_table
        else: table = self.payment_history_view.payment_table # PaymentHistoryWindow(self.database_name, self).payment_table 
        
        # Get current tab's table widget
        if self.isMaximized():  
            table.resizeColumnsToContents()
            table.resizeRowsToContents()
            if table2:
                table2.resizeColumnsToContents()
                table2.resizeRowsToContents()
            return  # Don't resize if the window is maximized        
               
            # Calculate required dimensions
        self.calculate_table_size(table)
        if table2 :
            if table2.isVisible():
                self.calculate_table_size(table2)
        
        # Get current screen geometry
        screen = QApplication.primaryScreen().availableGeometry()
        max_width = int(screen.width() * 0.9)
        max_height = int(screen.height() * 0.8)      
        
        
        # Add space for menubar and other UI elements
        menubar_height = self.menuBar().height()
        menubar_width = 0 #self.menuBar().width()
        statusbar_height = self.statusBar().height() if self.statusBar().isVisible() else 0
        padding = 100  # Additional space for buttons and margins
        
        # Calculate new window size
        new_width = min(table.total_width + 100+ menubar_width, max_width)
        new_height = min(table.total_height + menubar_height + statusbar_height + padding, max_height)
        if table2:
            if table2.isVisible():
                new_width = min(table.total_width + 100+ menubar_width+table2.total_width, max_width)
                new_height = min(table.total_height + menubar_height + statusbar_height + padding+table2.total_height, max_height)            
        
        
        # Ensure minimum size for menubar visibility
        min_height = menubar_height + 100  # At least 100px for content
        new_height = max(new_height, min_height)
        
        # Apply new size with smooth animation
        self.animate_resize(new_width, new_height)
        #self.resize_window_smoothly(new_width, new_height)

    def calculate_table_size(self, table):
        # Resize columns/rows to content
        
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        #'''
        # Calculate total table size
        width = 0
        for i in range(table.columnCount()):
            width += table.columnWidth(i)
        
        height = 0
        for i in range(table.rowCount()):
            height += table.rowHeight(i)
        
        # Add header dimensions
        if table.verticalHeader().isVisible():
            width += table.verticalHeader().width()
        if table.horizontalHeader().isVisible():
            height += table.horizontalHeader().height() 
            
        # Add header dimensions (modified to include menubar)
        header = table.horizontalHeader()
        if header.isVisible():
            height += header.height()
        
        # Store dimensions on table object
        table.total_width = width  + 20  # Add margin
        table.total_height = height  + 20
 
    

    def resize_window_smoothly(self, target_width, target_height):
        """Resize the main window smoothly without freezing the menu bar."""
        if self.isMaximized():
            return  # Do not resize if the window is maximized

        # Get current window size
        current_width, current_height = self.width(), self.height()

        # Calculate resize steps (adjust speed by changing the divisor)
        step_x = (target_width - current_width) // 10  # Divides into 10 smooth steps
        step_y = (target_height - current_height) // 10

        def step_resize():
            """Incrementally resize the window without freezing the UI."""
            nonlocal current_width, current_height

            if abs(current_width - target_width) <= abs(step_x) and abs(current_height - target_height) <= abs(step_y):
                self.resize(target_width, target_height)  # Final resize
                return  # Stop timer when target size is reached

            # Adjust width and height step by step
            current_width += step_x
            current_height += step_y
            self.resize(current_width, current_height)

            # Ensure menu bar remains active
            self.menuBar().setEnabled(True)

            # Schedule next step
            QTimer.singleShot(20, step_resize)  # Adjust timing for smoothness

        # Start the incremental resizing process
        step_resize()

    def animate_resize(self, target_width, target_height):
        # Smooth size transition
        current_width = self.width()
        current_height = self.height()
        
        self.animation = QPropertyAnimation(self, b"size")
        self.animation.setDuration(900)
        self.animation.setStartValue(QSize(current_width, current_height))
        self.animation.setEndValue(QSize(target_width, target_height))
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.start()


    '''
    def resizeEvent(self, event):
        """ Adjust window size dynamically when resized """
        super().resizeEvent(event)
        #self.adjust_window_size()  # Ensure it updates when needed
    '''
    
    def get_last_opened_database(self):
        """ Load the last opened database or fallback to _temp__.db """
        settings_file = "last_db.txt"
        if os.path.exists(settings_file):  # Check if settings file exists
            with open(settings_file, "r") as file:
                last_db = file.read().strip()
                if os.path.exists(last_db):  # Check if last DB exists
                    return last_db

        return "_temp__.db"  # Default database if last opened file is missing

    def save_last_opened_database(self):
        """ Save the current database file path before closing """
        with open("last_db.txt", "w") as file:
            file.write(self.database_name)
        
        
    def open_payment_window(self):
        payment_window = PaymentWindow(self.database_name,self)
        payment_window.exec_()
        self.load_inventory()
    
    
    # Define open_manage_customers function in CustomersWindow
    def open_manage_customers(self):
        self.setWindowTitle("Customer Records - {}".format(self.database_name))  
        self.customer_base.load_customers()         
        self.file_menu.menuAction().setVisible(True)
        self.user_menu.menuAction().setVisible(False)
        self.settings_menu.menuAction().setVisible(False)
        self.payment_action.setVisible(True)
        #self.customers_database.setVisible(False)
        self.home_action.setVisible(True)
        self.inventory_action.setVisible(True)
        self.customers_action.setVisible(True)
        self.stacked_widget.setCurrentIndex(4)  
        self.set_window_title()
        self.adjust_window_size()
    
        
    def open_payment_history(self):
        self.setWindowTitle("Sales/Payment Records - {}".format(self.database_name))
        self.payment_history_view.data = self.database_name
        #self.customer_view.load_customers()
        self.payment_history_view.load_customers()
        self.payment_history_view.load_payment_history()
        self.file_menu.menuAction().setVisible(True)
        self.user_menu.menuAction().setVisible(False)
        self.settings_menu.menuAction().setVisible(False)
        self.payment_action.setVisible(False)
        self.home_action.setVisible(True)
        self.inventory_action.setVisible(True)
        self.customers_action.setVisible(True)
        self.stacked_widget.setCurrentIndex(2)
        #history_window = PaymentHistoryWindow(self.database_name,self)
        #history_window.exec_()
        self.set_window_title()
        self.load_inventory()
        self.adjust_window_size()
    
    def open_customers_window(self):
        #self.customers_window = CustomersWindow(self.database_name)
        #self.customers_window.exec_() 
        self.setWindowTitle("Sales - {}".format(self.database_name))        
        self.customer_view.data = self.database_name
        self.customer_view.load_customers()
        self.stacked_widget.setCurrentIndex(1) 
        self.file_menu.menuAction().setVisible(True)
        self.user_menu.menuAction().setVisible(False)
        self.customers_action.setVisible(False)
        self.settings_menu.menuAction().setVisible(False)
        self.home_action.setVisible(True)
        self.payment_action.setVisible(True)
        self.inventory_action.setVisible(True)
        self.set_window_title()
        self.adjust_window_size()

    def show_main_view(self):
        """ Switch back to the main inventory view """
        self.load_inventory()
        self.setWindowTitle("Inventory - {}".format(self.database_name))
        self.stacked_widget.setCurrentIndex(0)
        self.file_menu.menuAction().setVisible(True)
        self.user_menu.menuAction().setVisible(False)
        self.inventory_action.setVisible(False)
        self.settings_menu.menuAction().setVisible(False)
        self.home_action.setVisible(True)
        self.payment_action.setVisible(True)
        self.customers_action.setVisible(True)
        self.set_window_title()
        self.adjust_window_size()
        
        
    def show_home(self):
        """Switch to Home View"""
        self.stacked_widget.setCurrentIndex(3)
        self.set_window_title()
        self.file_menu.menuAction().setVisible(False)
        self.user_menu.menuAction().setVisible(True)
        self.settings_menu.menuAction().setVisible(True)
        self.home_action.setVisible(False)
        self.payment_action.setVisible(True)
        self.inventory_action.setVisible(True)
        self.customers_action.setVisible(True)
        
    
    def edit_inventory_item(self):
        selected_row = self.inventory_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "No item selected.")
            return
        
        item_name = self.inventory_table.item(selected_row, 0).text()
        current_quantity = int(self.inventory_table.item(selected_row, 3).text())
        current_price = float(self.inventory_table.item(selected_row, 2).text())
        
        dialog = EditInventoryDialog(item_name, current_quantity, current_price, self)
        if dialog.exec_() == QDialog.Accepted:
            new_quantity, new_price = dialog.get_new_values()
            if int(new_quantity) <= 0 or float(new_price) <= 0:
                QMessageBox.warning(self, "Error", "Check the Quantity and or Unit Price for a positive input.")
                return 
                
            new_total_cost = new_quantity * new_price
            temp_issued = self.inventory_table.item(selected_row, 4).text()
            if temp_issued == "" or temp_issued == None or temp_issued == "None":
                qty_issued = 0
            else:
                qty_issued = int(self.inventory_table.item(selected_row, 4).text())
            qty_remaining = new_quantity - qty_issued
            
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE inventory 
                SET quantity_received = ?, unit_price = ?, total_cost = ?, quantity_remaining = ?, user_logged = ?
                WHERE item_name = ?
            """, (new_quantity, new_price, new_total_cost, qty_remaining, self.user_manager.logged_in_user, item_name))
            conn.commit()
            conn.close()
            log = f"{self.user_manager.logged_in_user} edit {item_name} in stock"
            log_text(log)
            self.load_inventory()
    
    def delete_inventory_item(self):
        selected_row = self.inventory_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "No item selected.")
            return
        confirm = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to delete this item?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            item_name = self.inventory_table.item(selected_row, 0).text()
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventory WHERE item_name = ?", (item_name,))
            conn.commit()
            conn.close()            
            log = f"{self.user_manager.logged_in_user} deleted {item_name} from stock"
            log_text(log)
            self.load_inventory()
    
    def new_file(self):
        self.current_db = "_temp__.db"
        conn = sqlite3.connect(self.current_db)
        cursor = conn.cursor()
        cursor.execute("VACUUM")  # Reset database
        conn.commit()
        conn.close()
        #QMessageBox.information(self, "New File", "A new inventory database has been created.")
        filepath, _ = QFileDialog.getSaveFileName(self, "Create New Database", "", "Database Files (*.db)")
        if filepath:
            try:
                if filepath == self.database_name:
                    os.remove(self.database_name)  
                self.database_name = filepath
                self.set_window_title()        
                self.create_database(self.database_name)
                self.customer_view.data = self.database_name
                self.payment_history_view.data = self.database_name
                self.customer_view.load_customers()
                self.payment_history_view.load_customers()
                self.payment_history_view.load_payment_history()
                self.load_inventory()
            except FileNotFoundError:   
                self.set_window_title()                     
                self.create_database(self.database_name)
                self.customer_view.data = self.database_name
                self.payment_history_view.data = self.database_name
                self.customer_view.load_customers()
                self.payment_history_view.load_customers()
                self.payment_history_view.load_payment_history()
                self.load_inventory()
                
        
    def open_sales_window(self, parent_window):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT item_name FROM inventory")
        items = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        self.sales_window = SalesWindow(self.database_name, parent_window)
        self.sales_window.exec_()
        #QMessageBox.information(self, "Info", "Sale recorded successfully!")
        self.load_inventory()
        
    
    def load_inventory(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT item_name, date_received, unit_price, quantity_received, quantity_issued, quantity_remaining, total_cost FROM inventory")
        rows = cursor.fetchall()
        conn.close()
        
        self.inventory_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, data in enumerate(row_data):
                self.inventory_table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
    
    def open_add_inventory_dialog(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Add Inventory Item")
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Product Name:"))
        self.item_name_input = QLineEdit()
        layout.addWidget(self.item_name_input)
        
        layout.addWidget(QLabel("Product Quantity:"))
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(1000000)
        #self.quantity_input.setValidator(QIntValidator(0, 99999999999))
        layout.addWidget(self.quantity_input)
        
        layout.addWidget(QLabel("Date Received:"))
        self.date_received_input = QDateEdit()
        self.date_received_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_received_input)
        
        layout.addWidget(QLabel("Unit Price:"))
        self.unit_price_input = QLineEdit()
        validator = QDoubleValidator(0.0, 999999.99, 2)  # Min 0.0, Max 999999.99, 2 decimal places
        validator.setNotation(QDoubleValidator.StandardNotation)  # Standard notation
        self.unit_price_input.setValidator(validator)
        layout.addWidget(self.unit_price_input)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.save_inventory(self.item_name_input.text(), self.date_received_input.date().toString("yyyy-MM-dd"), self.unit_price_input.text(), self.quantity_input.value()))
        button_box.rejected.connect(self.dialog.reject)
        layout.addWidget(button_box)
        
        self.dialog.setLayout(layout)
        self.dialog.exec_()
    
    def save_inventory(self, item_name, date_received, unit_price, quantity):
        if not item_name or not unit_price or not quantity or int(quantity) <= 0 or float(unit_price) <= 0:
            QMessageBox.warning(self, "Error", "Please fill all fields and check for accuracy")
            return
        
        total_cost = float(unit_price) * int(quantity)
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (item_name, date_received, unit_price, quantity_received, quantity_remaining, total_cost, user_logged) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (item_name, date_received, float(unit_price), int(quantity), int(quantity), total_cost, self.user_manager.logged_in_user))
        conn.commit()
        conn.close()
        self.item_name_input.clear()
        self.quantity_input.setValue(0)
        self.unit_price_input.clear()
        self.dialog.accept()
        self.load_inventory()
        log = f"{self.user_manager.logged_in_user} added {item_name} to stock"
        log_text(log)
        QMessageBox.information(self, "Success", "Item added successfully.") 
    
    def set_window_title(self):
        current_view = self.get_current_view()
        self.setWindowTitle(f"{self.window_titles[current_view]} - {self.database_name}")    
    
    def open_file(self):
        #options = QFileDialog.Options()
        #file_path, _ = QFileDialog.getOpenFileName(self, "Open Database", "", "Database Files (*.db);;All Files (*)", options=options)
        #if file_path:
        #    self.current_db = file_path
        #    QMessageBox.information(self, "File Opened", f"Database {file_path} opened successfully.")
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Database", "", "Database Files (*.db)")
        # print("file path is ", self.database_name)
        if  filepath:
            self.database_name = filepath
            self.set_window_title()
            self.customer_view.data = self.database_name
            self.payment_history_view.data = self.database_name
            self.customer_view.load_customers()
            self.payment_history_view.load_customers()
            self.payment_history_view.load_payment_history()
            self.customer_base.data = self.database_name
            self.customer_base.load_customers()
            self.load_inventory()
            self.customer_view.load_search()
            self.adjust_window_size()
            
            #QMessageBox.information(self, "Open File", f"Opened {self.database_name}")
            
    def get_current_view(self):
        self.current_widget = self.stacked_widget.currentIndex()
        #print(f"Current view: {self.current_widget}")
        return self.current_widget
    
    def set_theme(self, theme):
        """ Apply the selected theme """
        if theme == "light":
            self.setStyleSheet(LIGHT_THEME)
        if theme == "sunset_glo":
            self.setStyleSheet(SUNSET_GLOW)
        if theme == "neon_nit":
            self.setStyleSheet(NEON_NIGHTS)
        if theme == "galaxy":
            self.setStyleSheet(GALAXY_EXPLORER)
        elif theme == "dark":
            self.setStyleSheet(DARK_THEME)
        elif theme == "system":
            self.setStyleSheet("")  # Uses system default
        elif theme == "dark1":
            self.setStyleSheet(DARK_THEME_1)
        elif theme == "dark2":
            self.setStyleSheet(DARK_THEME_2)
        elif theme == "light1":
            self.setStyleSheet(LIGHT_THEME_1)
        elif theme == "light2":
            self.setStyleSheet(LIGHT_THEME_2)
        elif theme == "neon":
            self.setStyleSheet(NEON_CYBERPUNK)
        elif theme == "electric":
            self.setStyleSheet(ELECTRIC_FOREST)
        elif theme == "sunset":
            self.setStyleSheet(SUNSET_GRADIENT)
        elif theme == "ocean":
            self.setStyleSheet(OCEAN_DEPTHS)
        elif theme == "candy":
            self.setStyleSheet(CANDY_LAND)
        elif theme == "material":
            self.setStyleSheet(MATERIAL_DARK)
        elif theme == "fiber":
            self.setStyleSheet(FIBERS)
        elif theme == "combi":
            self.setStyleSheet(COMBINEAR)
        elif theme == "mac":
            self.setStyleSheet(MAC)

        # Save theme choice
        with open("theme_settings.txt", "w") as file:
            file.write(theme)

    def load_theme(self):
        """ Load the last used theme from settings """
        if os.path.exists("theme_settings.txt"):
            with open("theme_settings.txt", "r") as file:
                theme = file.read().strip()
                self.set_theme(theme)
        else:
            self.set_theme('fiber')
    
    def export_to_csv(self, ff="None", show_success = True):
        self.get_current_view()
        table = self.inventory_table if self.current_widget == 0 else self.payment_history_view.payment_table if self.current_widget == 2 else self.customer_base.customer_records_table if self.current_widget == 4 else self.customer_view.customer_table
        """Export payment records to CSV."""    
        if ff == "None":
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)", options=QFileDialog.Options())
        else:
            file_path = os.getcwd()+'\\'+ff +".csv"
        if file_path:
            data = []
            for row in range(table.rowCount()):
                row_data = [table.item(row, col).text() if table.item(row, col) else "" for col in range(table.columnCount())]
                data.append(row_data)

            headers = self.get_table_headers(table)
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


    def export_to_pdf(self):
        """Export payment records to a PDF file."""
        #first convert to csv, then convert from csv to pdf using reportlab module        
        self.export_to_csv("temp",False)
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PDF Files (*.pdf)", options=QFileDialog.Options())
        if file_path:         
            csv_to_pdf("temp.csv", file_path)
            os.remove('temp.csv')
    
    def save_database_as(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Database As", "", "Database Files (*.db);;All Files (*)", options=options
        )

        if file_path:
            try:
                shutil.copyfile(self.database_name, file_path)
                self.database_name = file_path
                self.customer_view.data = self.database_name
                self.payment_history_view.data = self.database_name
                self.customer_view.load_customers()
                self.payment_history_view.load_customers()
                self.payment_history_view.load_payment_history()
                self.load_inventory()
                self.set_window_title()
                QMessageBox.information(self, "Success", "Database saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save database: {str(e)}")
                
    
    def create_database(self, db_name):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
                
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                date_received TEXT,
                unit_price REAL,
                quantity_received INTEGER,
                quantity_issued INTEGER DEFAULT 0,
                quantity_remaining INTEGER,
                total_cost REAL,
                user_logged TEXT
            )
        """)        
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sms_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                location TEXT,
                contact TEXT,
                item_name TEXT,
                quantity INTEGER,
                unit_price REAL,
                total_owed REAL,
                amount_paid REAL DEFAULT 0,
                remaining_debt REAL,
                sale_date TEXT DEFAULT CURRENT_TIMESTAMP,
                payment_mode TEXT,
                cheque_number TEXT,
                cheque_bank TEXT,
                cheque_clearance_date TEXT,
                transaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
                user_logged TEXT                
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                location TEXT,
                contact TEXT UNIQUE       
            )
        """)

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY  AUTOINCREMENT,
                transaction_id TEXT,
                customer_name TEXT NOT NULL,
                item_name TEXT,
                amount_paid REAL NOT NULL,
                payment_mode TEXT NOT NULL,
                cheque_number TEXT,
                cheque_bank TEXT,
                cheque_clearance_date TEXT,
                entry_date_and_time TEXT, --  unique identifier used to query the table
                transaction_date TEXT, 
                user_logged TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT UNIQUE,
                name TEXT,
                location TEXT,
                contact TEXT,
                product_name TEXT,
                unit_price TEXT,
                quantity TEXT,
                bulk_discount TEXT DEFAULT NULL,
                prompt_payment_discount TEXT DEFAULT NULL,
                total_owed REAL DEFAULT 0,
                total_paid REAL DEFAULT 0,
                remaining_debt REAL DEFAULT 0,
                entry_date_and_time TEXT,
                transaction_date, TEXT,
                user_logged TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    

    def import_file(self):
        gs = ImportTableDialog(self)
        gs.exec_()
        self.load_inventory()
        self.customer_view.load_customers()
        self.customer_view.load_search
        self.payment_history_view.load_payment_history()
    
        
    def closeEvent(self, event):
        """ Prompt to save or delete '_temp__.db' before exiting """
        if self.database_name == "_temp__.db":
            reply = QMessageBox.question(self, "Exit", 
                                         "Do you want to save before exiting?", 
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if reply == QMessageBox.Yes:
                self.save_database_as()  # Save the database
                os.remove("_temp__.db")  # Delete the file
                self.save_last_opened_database()
                event.accept()  # Allow closing
            elif reply == QMessageBox.No:
                os.remove("_temp__.db")  # Delete the file
                event.accept()  # Allow closing
            else:
                event.ignore()  # Cancel exit
        else:
            try:
                os.remove("_temp__.db")  # Delete the file
                self.save_last_opened_database()
                #event.accept()  # Normal exit for other database
            except FileNotFoundError:                
                self.save_last_opened_database()
                event.accept()  # Normal exit for other database 
    
    def get_user_logout_time(self):
        """Retrieve the user's preferred logout timeout from the database."""
        conn = sqlite3.connect(self.user_manager.database)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM user_settings WHERE username=? AND key='logout_timer'", 
                       (self.user_manager.logged_in_user,))
        result = cursor.fetchone()
        conn.close()
        return int(result[0]) if result else 60  # Default to 60 minutes

    def reset_inactivity_timer(self):
        """Reset the inactivity timer when user is active."""
        self.inactivity_timer.start(self.logout_timeout)

    def auto_logout(self):
        """Log out the user after inactivity timeout."""
        QMessageBox.information(self, "Session Timeout", "You have been logged out due to inactivity.")
        self.user_manager.logout()

    def eventFilter(self, source, event):
        """Detect user activity and reset inactivity timer."""
        if event.type() in [QEvent.MouseMove, QEvent.KeyPress]:
            self.reset_inactivity_timer()
        return super().eventFilter(source, event)
           

class SettingsDialog(QDialog):
    """Settings window for company name and logout timer."""
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        self.setWindowTitle("Settings")
        self.setGeometry(400, 200, 350, 250)

        layout = QVBoxLayout()

        # Company Name (Admin Only)
        self.company_name_input = QLineEdit()
        self.company_name_input.setPlaceholderText("Enter Company Name")
        layout.addWidget(QLabel("Company Name (Admin Only):"))
        layout.addWidget(self.company_name_input)

        # Logout Timer (For All Users)
        self.logout_timer_input = QLineEdit()
        self.logout_timer_input.setPlaceholderText("Enter Logout Timer (minutes)")
        layout.addWidget(QLabel("Logout Timer (Any User):"))
        layout.addWidget(self.logout_timer_input)

        # Load existing settings
        self.load_settings()

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def load_settings(self):
        """Load saved settings from the database."""
        conn = sqlite3.connect(self.user_manager.database)
        cursor = conn.cursor()

        # Load company name (only for Admins)
        if self.user_manager.logged_in_role == "Administrator":
            cursor.execute("SELECT value FROM settings WHERE key='company_name'")
            result = cursor.fetchone()
            if result:
                self.company_name_input.setText(result[0])
        else:
            self.company_name_input.setDisabled(True)  # Disable for non-admin users

        # Load logout timer (for all users)
        cursor.execute("SELECT value FROM user_settings WHERE username=?", (self.user_manager.logged_in_user,))
        result = cursor.fetchone()
        self.logout_timer_input.setText(result[0] if result else "60")  # Default to 60 minutes

        conn.close()

    def save_settings(self):
        """Save the settings to the database."""
        conn = sqlite3.connect(self.user_manager.database)
        cursor = conn.cursor()

        # Save Company Name (Admins Only)
        if self.user_manager.logged_in_role == "Administrator":
            company_name = self.company_name_input.text().strip()
            if company_name:
                cursor.execute("INSERT INTO settings (key, value) VALUES ('company_name', ?) ON CONFLICT(key) DO UPDATE SET value=?",
                               (company_name, company_name))

        # Save Logout Timer (For All Users)
        logout_timer = self.logout_timer_input.text().strip()
        if logout_timer.isdigit():
            cursor.execute("INSERT INTO user_settings (username, key, value) VALUES (?, 'logout_timer', ?) ON CONFLICT(username, key) DO UPDATE SET value=?",
                           (self.user_manager.logged_in_user, logout_timer, logout_timer))
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for the logout timer.")
            return

        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Settings saved successfully!")
        self.accept()

def log_text(text):
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Open the file in append mode (creates the file if it doesn't exist)
    with open("log.txt", "a") as file:
        # Write the timestamp followed by the input text
        file.write(f"[{timestamp}] {text}\n")