from PyQt5.QtWidgets import QMessageBox, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from user_mgt import UserManager
import datetime, os
from themes import *

def log_text(text):
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Open the file in append mode (creates the file if it doesn't exist)
    with open("log.txt", "a") as file:
        # Write the timestamp followed by the input text
        file.write(f"[{timestamp}] {text}\n")


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(300, 200, 200, 200)
        self.user_manager = UserManager(self, None)  # No main window yet

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.central_widget.setLayout(layout)
        self.load_theme()

    def login(self):
        """Authenticate user and open MainWindow."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if self.user_manager.authenticate_user(username, password):
            self.open_main_window()
            log = f"{username} Logged in."
            log_text(log)
            #QMessageBox.information(self, "Success", f"Welcome {username}!")
        else:      
            log = f"{username} attempted to log in but failed"
            log_text(log)
            QMessageBox.warning(self, "Login Failed", "Invalid credentials!")      
            
    def showEvent(self, event):
        """Clear login input fields whenever the window is shown."""
        self.username_input.clear()
        self.password_input.clear()
        super().showEvent(event)
    
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


    def open_main_window(self):
        """Open the main application window after successful login."""
        from main_window import MainWindow  # Import only when needed to prevent circular import

        self.main_window = MainWindow(self.user_manager)  # Pass user manager to main window
        self.user_manager.main_window = self.main_window  # Update reference
        self.main_window.show()
        self.close()
