from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMenu, QAction, QGridLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import datetime, os,sys



def log_text(text):
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Open the file in append mode (creates the file if it doesn't exist)
    with open("log.txt", "a") as file:
        # Write the timestamp followed by the input text
        file.write(f"[{timestamp}] {text}\n")

class HomeView(QWidget):
    def __init__(self, main_window, user_manager):
        super().__init__()
        self.main_window = main_window
        self.user_manager = user_manager
        self.initUI()

    def initUI(self):
        
        """
        # Set background image using QLabel
        image_path = os.path.join(os.path.dirname(__file__), "rosemer.jpg")
        #image_path = resource_path("rosemer.jpg")
        self.bg_label = QLabel(self)
        pixmap = QPixmap(image_path)  # Ensure the path is correct
        if pixmap.isNull():
            print("Error: Could not load image. Check the file path.")

        self.bg_label.setPixmap(pixmap)
        self.bg_label.setScaledContents(True)  # Scale the image to fit the window
        self.bg_label.setGeometry(0, 0, self.width(), self.height())  # Set to window size
        """
        main_layout = QVBoxLayout()


        # === Top Bar Layout ===
        top_layout = QHBoxLayout()
        # Welcome Message
        self.username_label = QLabel(f"Welcome, {self.user_manager.logged_in_user}")
        self.username_label.setFont(QFont("Arial", 14, QFont.Bold))
        top_layout.addWidget(self.username_label)
        # Spacer to push buttons to the right
        top_layout.addStretch()
        
        # === Logout Button ===
        self.logout_button = QPushButton("🚪 Logout")
        self.logout_button.setStyleSheet("background-color: #d32f2f; color: white; padding: 6px;")
        self.logout_button.clicked.connect(self.user_manager.logout)  # Example connection
        top_layout.addWidget(self.logout_button)

        # === User Management Button (Admins Only) ===
        if self.user_manager.logged_in_role == "Administrator":
            self.user_mgmt_button = QPushButton("👤 Manage Users")
            self.user_mgmt_button.setStyleSheet("background-color: #1976d2; color: white; padding: 6px;")
            self.user_mgmt_button.clicked.connect(self.main_window.open_user_management)  # Example connection
            top_layout.addWidget(self.user_mgmt_button)

        # === Theme Selection Button with Dropdown ===
        self.theme_button = QPushButton("🎨 Theme")
        self.theme_button.setStyleSheet("background-color: #388e3c; color: white; padding: 6px;")
        self.theme_menu = QMenu()
        
        light_action = QAction("Light Theme", self)
        dark_action = QAction("Dark Theme", self)
        system_action = QAction("System Theme", self)
        light_action_1 = QAction("Light Theme 1", self)
        dark_action_1 = QAction("Dark Theme 1", self)
        ocean_depth = QAction("Ocean Depths", self)
        light_action_2 = QAction("Light Theme 2", self)
        dark_action_2 = QAction("Dark Theme 2", self)
        neon_cyber = QAction("Neon CyberPunk", self)
        electric_for = QAction("Electric Forest", self)
        candy_lan = QAction("Candy Land", self)
        sunset_grad = QAction("Sunset Gradient", self)
        neon_nit = QAction("Neon Night", self)
        sunset_glo = QAction("Sunset Glow", self)
        mac = QAction("mac", self)
        combi = QAction("combi", self)
        fiber = QAction("fiber", self)
        material = QAction("material", self)
        galaxy = QAction("galaxy", self)

        light_action.triggered.connect(lambda: self.main_window.set_theme("light"))
        dark_action.triggered.connect(lambda: self.main_window.set_theme("dark"))
        system_action.triggered.connect(lambda: self.main_window.set_theme("system"))
        dark_action_1.triggered.connect(lambda: self.main_window.set_theme("dark1"))
        light_action_1.triggered.connect(lambda: self.main_window.set_theme("light1"))
        dark_action_2.triggered.connect(lambda: self.main_window.set_theme("dark2"))
        light_action_2.triggered.connect(lambda: self.main_window.set_theme("light2"))
        neon_cyber.triggered.connect(lambda: self.main_window.set_theme("neon"))
        electric_for.triggered.connect(lambda: self.main_window.set_theme("electric")) 
        sunset_grad.triggered.connect(lambda: self.main_window.set_theme("sunset"))
        candy_lan.triggered.connect(lambda: self.main_window.set_theme("candy"))
        ocean_depth.triggered.connect(lambda: self.main_window.set_theme("ocean"))  
        sunset_glo.triggered.connect(lambda: self.main_window.set_theme("sunset_glo"))
        neon_nit.triggered.connect(lambda: self.main_window.set_theme("neon_nit"))
        galaxy.triggered.connect(lambda: self.main_window.set_theme("galaxy"))   
        mac.triggered.connect(lambda: self.main_window.set_theme("mac"))      
        combi.triggered.connect(lambda: self.main_window.set_theme("combi"))      
        material.triggered.connect(lambda: self.main_window.set_theme("material"))      
        fiber.triggered.connect(lambda: self.main_window.set_theme("fiber"))         

        self.theme_menu.addAction(light_action)
        self.theme_menu.addAction(dark_action)
        self.theme_menu.addAction(system_action)
        self.theme_menu.addAction(light_action_1)
        self.theme_menu.addAction(dark_action_1)
        self.theme_menu.addAction(electric_for)
        self.theme_menu.addAction(light_action_2)
        self.theme_menu.addAction(dark_action_2)
        self.theme_menu.addAction(candy_lan)
        self.theme_menu.addAction(sunset_grad)
        self.theme_menu.addAction(ocean_depth)
        self.theme_menu.addAction(neon_cyber)
        self.theme_menu.addAction(sunset_glo)
        self.theme_menu.addAction(neon_nit)
        self.theme_menu.addAction(galaxy)
        self.theme_menu.addAction(mac)
        self.theme_menu.addAction(combi)
        self.theme_menu.addAction(material)
        self.theme_menu.addAction(fiber)        
        

        self.theme_button.setMenu(self.theme_menu)
        top_layout.addWidget(self.theme_button)

        main_layout.addLayout(top_layout)
        

        # Title Label
        title_label = QLabel("Welcome to Inventory Management")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #005f73; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Buttons with Icons
        self.inventory_button = QPushButton("📦 Go to Inventory")
        self.inventory_button.setFont(QFont("Arial", 12))
        self.inventory_button.setStyleSheet("background-color: #009688; color: white; padding: 10px;")
        self.inventory_button.clicked.connect(self.main_window.show_main_view)

        self.payment_button = QPushButton("💰 View Payment Records")
        self.payment_button.setFont(QFont("Arial", 12))
        self.payment_button.setStyleSheet("background-color: #ff9800; color: white; padding: 10px;")
        self.payment_button.clicked.connect(self.main_window.open_payment_history)

        self.customers_button = QPushButton("🛒  View Sales Records")
        self.customers_button.setFont(QFont("Arial", 12))
        self.customers_button.setStyleSheet("background-color: #3f51b5; color: white; padding: 10px;")
        self.customers_button.clicked.connect(self.main_window.open_customers_window)

        self.customers_database_button = QPushButton("👥 Go to Customers Records")
        self.customers_database_button.setFont(QFont("Arial", 12))
        self.customers_database_button.setStyleSheet("background-color: #00BFFF; color: white; padding: 10px;")
        self.customers_database_button.clicked.connect(self.main_window.open_manage_customers)
        
        
        # Create a grid layout for 2x2 button arrangement
        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignCenter)  # Align grid to the center
        grid_layout.setSpacing(20)  # Add spacing between buttons
        
        grid_layout.addWidget(self.inventory_button, 0, 0)
        grid_layout.addWidget(self.payment_button, 0, 1)
        grid_layout.addWidget(self.customers_button,1,0)
        grid_layout.addWidget(self.customers_database_button,1,1)

        # Add buttons to main_layout
        #main_layout.addWidget(self.inventory_button)
        #main_layout.addWidget(self.payment_button)
        #main_layout.addWidget(self.customers_button)
        #main_layout.addWidget(self.customers_database_button)
        main_layout.addLayout(grid_layout)

        self.setLayout(main_layout)

    def resizeEvent(self, event):
        """ Resize the background image when the window is resized """
        #self.bg_label.setGeometry(0, 0, self.width(), self.height())



def resource_path(relative_path):
    """ Get the absolute path to a resource, works for PyInstaller """
    if getattr(sys, 'frozen', False):  # If the app is run as a bundled executable
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

