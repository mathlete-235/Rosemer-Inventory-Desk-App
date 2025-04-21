import sqlite3
import hashlib
from PyQt5.QtWidgets import QWidget, QStackedWidget, QComboBox, QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class UserManager:
    def __init__(self, login_window, main_window):
        self.login_window = login_window
        self.main_window = main_window
        self.database = "users.db"
        self.logged_in_user = None
        self.logged_in_role = None
        self.create_user_database()
        self.create_settings_database()


    def create_user_database(self):
        """Create the user database if it doesn't exist."""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT CHECK(role IN ('Administrator', 'Attendant')) NOT NULL
            )
        """)
        
        hashed_password = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)", ("admin", hashed_password, 'Administrator'))
        
        conn.commit()
        conn.close()

    def authenticate_user(self, username, password):
        """Check user credentials and return role if valid."""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            stored_hash, role = result
            if hashlib.sha256(password.encode()).hexdigest() == stored_hash:
                self.logged_in_user = username
                self.logged_in_role = role
                return True
        return False

    def validate_user(self, username, password):
        """Check user credentials and return role if valid."""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            stored_hash = result[0]
            if hashlib.sha256(password.encode()).hexdigest() == stored_hash: 
                return True
        return False

    def check_permissions(self, feature):
        """Check if the logged-in user has permission for an action."""
        admin_only_features = ["reverse_transaction", "edit_payment", "add_user", "edit_transaction"]
        if self.logged_in_role != "Administrator" and feature in admin_only_features:
            QMessageBox.warning(None, "Access Denied", "You don't have permission to perform this action!")
            return False
        return True

    def logout(self):
        """Logout the current user and open the login window again."""
        self.logged_in_user = None
        self.logged_in_role = None
        self.main_window.close()
        self.login_window.show()

    def open_add_user_dialog(self):
        """Open a dialog to add a new user (Admin Only)."""
        if self.logged_in_role != "Administrator":
            QMessageBox.warning(None, "Access Denied", "Only administrators can add new users!")
            return

        dialog = AddUserDialog(self)
        dialog.exec_()
                   
        
    def open_reset_password_dialog(self):
        """Open a dialog to reset a user's password."""
        dialog = ResetPasswordDialog(self)
        dialog.exec_()
    
    def open_delete_user_dialog(self):
        """Open a dialog to delete a user account (Admin Only)."""
        if self.logged_in_role != "Administrator":
            QMessageBox.warning(None, "Access Denied", "Only administrators can delete users!")
            return
    
        dialog = DeleteUserDialog(self)
        dialog.exec_()

        
        
    def create_settings_database(self):
        """Create tables for storing settings."""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        # Table for global settings (Company Name)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        # Table for user-specific settings (Logout Timer)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                username TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                PRIMARY KEY (username, key)
            )
        """)

        conn.commit()
        conn.close()
        
    def get_all_users(self):
        """Retrieve a list of all usernames except the default admin."""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username != 'admin'")
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return users

    def get_all_users_with_roles(self):
        """Retrieve all registered users along with their roles."""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT username, role FROM users ORDER BY username ASC")
        users = cursor.fetchall()
        conn.close()
        return users
    
    def user_exists(self, username):
        """Check if a user exists in the database."""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists

    def add_user(self, username, password, role):
        """Add user to the database."""
        if not username or not password or role not in ["Administrator", "Attendant"]: 
            return
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                           (username, password_hash, role))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
        
        
    def change_user_role(self, username, new_role):
        """Change the role of a user in the database."""
        if username == "admin":
            return False  # Prevent changing the default admin's role

        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, username))
        conn.commit()
        conn.close()
        return True

        


    def delete_user(self, username):
        """Delete the specified user from the database."""
        if username == "admin":            
            return False

        if username == self.logged_in_user: 
            return False

        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if not result: 
            conn.close()
            return

        # Delete user
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        return True
    

    def reset_password(self, username, new_password, confirm_password):
        """Reset password in the database."""
        if not username or not new_password or not confirm_password: 
            return 0

        if new_password != confirm_password: 
            return 0

        password_hash = hashlib.sha256(new_password.encode()).hexdigest()

        # Check if user exists
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if not result: 
            conn.close()
            return

        # Admin Check (Only Admins Can Reset Other Users' Passwords)
        if self.logged_in_role != "Administrator" and self.logged_in_user != username: 
            conn.close()
            return

        # Update Password
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (password_hash, username))
        conn.commit()
        conn.close()

       
        
        
            

class AddUserDialog(QDialog):
    """Dialog for adding new users."""
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        self.setWindowTitle("Add New User")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Enter Role (Administrator/Attendant)")

        self.add_button = QPushButton("Add User")
        self.add_button.clicked.connect(self.add_user)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Role:"))
        layout.addWidget(self.role_input)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_user(self):
        """Add user to the database."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_input.text().strip()

        if not username or not password or role not in ["Administrator", "Attendant"]:
            QMessageBox.warning(self, "Error", "Invalid input! Role must be 'Administrator' or 'Attendant'.")
            return

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(self.user_manager.database)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                           (username, password_hash, role))
            conn.commit()
            QMessageBox.information(self, "Success", "User added successfully!")
            self.accept()  # Close dialog
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists!")
        conn.close()

        
        
class ResetPasswordDialog(QDialog):
    """Dialog to reset a user's password."""
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        self.setWindowTitle("Reset Password")
        self.setGeometry(400, 200, 300, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter New Password")
        self.new_password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm New Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.reset_button = QPushButton("Reset Password")
        self.reset_button.clicked.connect(self.reset_password)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("New Password:"))
        layout.addWidget(self.new_password_input)
        layout.addWidget(QLabel("Confirm Password:"))
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def reset_password(self):
        """Reset password in the database."""
        username = self.username_input.text().strip()
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not username or not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        password_hash = hashlib.sha256(new_password.encode()).hexdigest()

        # Check if user exists
        conn = sqlite3.connect(self.user_manager.database)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if not result:
            QMessageBox.warning(self, "Error", "User not found!")
            conn.close()
            return

        # Admin Check (Only Admins Can Reset Other Users' Passwords)
        if self.user_manager.logged_in_role != "Administrator" and self.user_manager.logged_in_user != username:
            QMessageBox.warning(self, "Access Denied", "Only administrators can reset other users' passwords.")
            conn.close()
            return

        # Update Password
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (password_hash, username))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Password reset successfully!")
        self.accept()

class DeleteUserDialog(QDialog):
    """Dialog for deleting user accounts."""
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        self.setWindowTitle("Delete User")
        self.setGeometry(400, 200, 200, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username to Delete")

        self.delete_button = QPushButton("Delete User")
        self.delete_button.clicked.connect(self.delete_user)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def delete_user(self):
        """Delete the specified user from the database."""
        username = self.username_input.text().strip()

        if username == "admin":
            QMessageBox.warning(self, "Error", "The default 'admin' account cannot be deleted!")
            return

        if username == self.user_manager.logged_in_user:
            QMessageBox.warning(self, "Error", "You cannot delete your own account while logged in!")
            return

        conn = sqlite3.connect(self.user_manager.database)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if not result:
            QMessageBox.warning(self, "Error", "User not found!")
            conn.close()
            return

        # Delete user
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", f"User '{username}' deleted successfully!")
        self.accept()


        
class AddUserForm(QWidget):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Attendant", "Administrator"])
        layout.addWidget(QLabel("Role:"))
        layout.addWidget(self.role_combo)

        add_user_button = QPushButton("Add User")
        add_user_button.clicked.connect(self.add_user)
        layout.addWidget(add_user_button)

        self.setLayout(layout)

    def add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password cannot be empty.")
            return

        if self.user_manager.add_user(username, password, role):
            QMessageBox.information(self, "Success", f"User '{username}' added successfully.")
        else:
            QMessageBox.warning(self, "Error", f"User '{username}' already exists.")

class DeleteUserForm(QWidget):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        layout = QVBoxLayout()

        self.user_combo = QComboBox()
        self.load_users()
        layout.addWidget(QLabel("Select User to Delete:"))
        layout.addWidget(self.user_combo)

        delete_user_button = QPushButton("Delete User")
        delete_user_button.clicked.connect(self.delete_user)
        layout.addWidget(delete_user_button)

        self.setLayout(layout)

    def load_users(self):
        users = self.user_manager.get_all_users()
        self.user_combo.clear()
        self.user_combo.addItems(users)

    def delete_user(self):
        username = self.user_combo.currentText()
        if username == "admin":
            QMessageBox.warning(self, "Error", "The default 'admin' account cannot be deleted.")
            return

        if self.user_manager.delete_user(username):
            QMessageBox.information(self, "Success", f"User '{username}' deleted successfully.")
            self.load_users()
        else:
            QMessageBox.warning(self, "Error", f"Failed to delete user '{username}'.")

class ResetPasswordForm(QWidget):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        layout = QVBoxLayout()

        self.user_combo = QComboBox()
        self.load_users()
        layout.addWidget(QLabel("Select User:"))
        layout.addWidget(self.user_combo)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter New Password")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("New Password:"))
        layout.addWidget(self.new_password_input)

        reset_password_button = QPushButton("Reset Password")
        reset_password_button.clicked.connect(self.reset_password)
        layout.addWidget(reset_password_button)

        self.setLayout(layout)

    def load_users(self):
        users = self.user_manager.get_all_users()
        self.user_combo.clear()
        self.user_combo.addItems(users)

    def reset_password(self):
        username = self.user_combo.currentText()
        new_password = self.new_password_input.text().strip()

        if not new_password:
            QMessageBox.warning(self, "Input Error", "New password cannot be empty.")
            return

        if self.user_manager.reset_password(username, new_password):
            QMessageBox.information(self, "Success", f"Password for '{username}' reset successfully.")
        else:
            QMessageBox.warning(self, "Error", f"Failed to reset password for '{username}'.")

class ViewUsersForm(QWidget):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        layout = QVBoxLayout()

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(2)
        self.user_table.setHorizontalHeaderLabels(["Username", "Role"])
        layout.addWidget(self.user_table)

        self.setLayout(layout)
        self.load_users()

    def load_users(self):
        users = self.user_manager.get_all_users_with_roles()
        self.user_table.setRowCount(len(users))
        for row, (username, role) in enumerate(users):
            self.user_table.setItem(row, 0, QTableWidgetItem(username))
            self.user_table.setItem(row, 1, QTableWidgetItem(role))


 
class ChangeUserGroupForm(QWidget):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        layout = QVBoxLayout()

        # User Selection ComboBox
        self.user_combo = QComboBox()
        self.load_users()
        layout.addWidget(QLabel("Select User:"))
        layout.addWidget(self.user_combo)

        # Role Selection ComboBox
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Attendant", "Administrator"])
        layout.addWidget(QLabel("Select New Role:"))
        layout.addWidget(self.role_combo)

        # Change Role Button
        change_role_button = QPushButton("Change Role")
        change_role_button.clicked.connect(self.change_user_role)
        layout.addWidget(change_role_button)

        self.setLayout(layout)

    def load_users(self):
        """Load users into the combo box, excluding the default 'admin'."""
        users = self.user_manager.get_all_users()
        self.user_combo.clear()
        for user in users:
            if user != "admin":  # Exclude the default 'admin' account
                self.user_combo.addItem(user)

    def change_user_role(self):
        """Change the role of the selected user."""
        username = self.user_combo.currentText()
        new_role = self.role_combo.currentText()

        if username == "admin":
            QMessageBox.warning(self, "Error", "The default 'admin' account's role cannot be changed.")
            return

        if self.user_manager.change_user_role(username, new_role):
            QMessageBox.information(self, "Success", f"User '{username}' role changed to '{new_role}'.")
        else:
            QMessageBox.warning(self, "Error", f"Failed to change role for user '{username}'.")


class UserManagementDialog(QDialog):
    def __init__(self, user_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Account Management")
        self.user_manager = user_manager

        layout = QVBoxLayout(self)

        # ComboBox for selecting the task
        self.task_combo = QComboBox()
        self.task_combo.addItems([
            "Add User",
            "Delete User",
            "Reset Password",
            "View Registered Users",
            "Change User Group"
        ])
        self.task_combo.currentIndexChanged.connect(self.display_selected_task)
        layout.addWidget(self.task_combo)

        # StackedWidget to hold different forms
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Initialize forms for each task
        self.init_add_user_form()
        self.init_delete_user_form()
        self.init_reset_password_form()
        self.init_view_users_form()
        self.init_change_user_group_form()

        # Display the first task by default
        self.display_selected_task(0)

    def init_add_user_form(self):
        """Initialize the form for adding a new user."""
        form = QWidget()
        form_layout = QVBoxLayout(form)

        self.add_username_input = QLineEdit()
        self.add_username_input.setPlaceholderText("Username")
        form_layout.addWidget(self.add_username_input)

        self.add_password_input = QLineEdit()
        self.add_password_input.setPlaceholderText("Password")
        self.add_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.add_password_input)

        self.add_role_combo = QComboBox()
        self.add_role_combo.addItems(["Attendant", "Administrator"])
        form_layout.addWidget(self.add_role_combo)

        add_user_button = QPushButton("Add User")
        add_user_button.clicked.connect(self.add_user)
        form_layout.addWidget(add_user_button)

        self.stacked_widget.addWidget(form)

    def init_delete_user_form(self):
        """Initialize the form for deleting a user."""
        form = QWidget()
        form_layout = QVBoxLayout(form)

        self.delete_user_combo = QComboBox()
        self.load_users(self.delete_user_combo)
        form_layout.addWidget(self.delete_user_combo)

        delete_user_button = QPushButton("Delete User")
        delete_user_button.clicked.connect(self.delete_user)
        form_layout.addWidget(delete_user_button)

        self.stacked_widget.addWidget(form)

    def init_reset_password_form(self):
        """Initialize the form for resetting a user's password."""
        form = QWidget()
        form_layout = QVBoxLayout(form)

        self.reset_user_combo = QComboBox()
        self.load_users(self.reset_user_combo)
        form_layout.addWidget(self.reset_user_combo)

        self.reset_password_input = QLineEdit()
        self.reset_password_input.setPlaceholderText("New Password")
        self.reset_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.reset_password_input)

        reset_password_button = QPushButton("Reset Password")
        reset_password_button.clicked.connect(self.reset_password)
        form_layout.addWidget(reset_password_button)

        self.stacked_widget.addWidget(form)

    def init_view_users_form(self):
        """Initialize the form for viewing registered users."""
        form = QWidget()
        form_layout = QVBoxLayout(form)

        self.users_table = QTableWidget()
        self.users_table.setColumnCount(2)
        self.users_table.setHorizontalHeaderLabels(["Username", "Role"])
        form_layout.addWidget(self.users_table)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.load_users_table)
        form_layout.addWidget(refresh_button)

        self.stacked_widget.addWidget(form)

    def init_change_user_group_form(self):
        """Initialize the form for changing a user's group."""
        form = QWidget()
        form_layout = QVBoxLayout(form)

        self.change_group_user_combo = QComboBox()
        self.load_users(self.change_group_user_combo)
        form_layout.addWidget(QLabel("Select User:"))
        form_layout.addWidget(self.change_group_user_combo)

        self.change_group_role_combo = QComboBox()
        self.change_group_role_combo.addItems(["Attendant", "Administrator"])
        form_layout.addWidget(QLabel("Select New Role:"))
        form_layout.addWidget(self.change_group_role_combo)

        change_group_button = QPushButton("Change Role")
        change_group_button.clicked.connect(self.change_user_group)  # ✅ Now properly connected
        form_layout.addWidget(change_group_button)

        self.stacked_widget.addWidget(form)

    def display_selected_task(self, index):
        """Display the form corresponding to the selected task."""
        self.stacked_widget.setCurrentIndex(index)
        if index == 3:  # View Registered Users
            self.load_users_table()

    def load_users(self, combo_box):
        """Load users into the given combo box, excluding the default 'admin'."""
        users = self.user_manager.get_all_users()
        combo_box.clear()
        for user in users:
            if user != "admin":  # Exclude the default 'admin' account
                combo_box.addItem(user)

    def load_users_table(self):
        """Load users into the table widget."""
        users = self.user_manager.get_all_users_with_roles()
        self.users_table.setRowCount(len(users))
        for row, (username, role) in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(username))
            self.users_table.setItem(row, 1, QTableWidgetItem(role))
            
    def change_user_role(self, username, new_role):
        """Change the role of a user in the database."""
        if username == "admin":
            return False  # Prevent changing the default admin's role

        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, username))
        conn.commit()
        conn.close()
        return True


    def add_user(self):
        """Add a new user."""
        username = self.add_username_input.text().strip()
        password = self.add_password_input.text().strip()
        role = self.add_role_combo.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password cannot be empty.")
            return

        if self.user_manager.user_exists(username):
            QMessageBox.warning(self, "Error", f"User '{username}' already exists.")
            return

        if self.user_manager.add_user(username, password, role):
            QMessageBox.information(self, "Success", f"User '{username}' added successfully.")
            self.add_username_input.clear()
            self.add_password_input.clear()
            self.load_users(self.delete_user_combo)
            self.load_users(self.reset_user_combo)
            self.load_users(self.change_group_user_combo)
        else:
            QMessageBox.warning(self, "Error", f"Failed to add user '{username}'.")
            
    def delete_user(self):
        """Delete the selected user after admin confirmation."""
        username = self.delete_user_combo.currentText()

        if not username:
            QMessageBox.warning(self, "Error", "No user selected.")
            return

        if username == "admin":
            QMessageBox.warning(self, "Error", "The default 'admin' account cannot be deleted.")
            return

        # Confirm deletion
        confirm = QMessageBox.question(self, "Confirm Deletion", 
                                    f"Are you sure you want to delete user '{username}'?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if confirm == QMessageBox.No:
            return  # User canceled deletion

        if self.user_manager.delete_user(username):
            QMessageBox.information(self, "Success", f"User '{username}' deleted successfully.")
            self.load_users(self.delete_user_combo)  # Refresh user list
            self.load_users(self.reset_user_combo)   # Refresh reset password list
            self.load_users(self.change_group_user_combo)  # Refresh change group list
        else:
            QMessageBox.warning(self, "Error", f"Failed to delete user '{username}'.")
            
 
    def reset_password(self):
        """Reset a user's password."""
        username = self.reset_user_combo.currentText()
        new_password = self.reset_password_input.text().strip()

        if not new_password:
            QMessageBox.warning(self, "Error", "New password cannot be empty.")
            return

        password_hash = hashlib.sha256(new_password.encode()).hexdigest()

        conn = sqlite3.connect(self.user_manager.database)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if not result:
            QMessageBox.warning(self, "Error", "User not found!")
            conn.close()
            return

        # Update Password
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (password_hash, username))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Password reset successfully!")
        self.reset_password_input.clear()
        
    def change_user_group(self):
        """Change the role of a user."""
        username = self.change_group_user_combo.currentText()
        new_role = self.change_group_role_combo.currentText()

        if username == "admin":
            QMessageBox.warning(self, "Error", "The default 'admin' account's role cannot be changed.")
            return

        if self.user_manager.change_user_role(username, new_role):
            QMessageBox.information(self, "Success", f"User '{username}' role changed to '{new_role}'.")
        else:
            QMessageBox.warning(self, "Error", "Failed to change user role.")

           