
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QHBoxLayout,
                             QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox, QTextEdit, QDialog, QSpinBox, QDateEdit, QDialogButtonBox, QCheckBox, QMenuBar, QMenu, QFileDialog)
#from PyQt5.QtCore import *
import sqlite3
import os
import csv

class ImportTableDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Import Table into Database")
        self.setGeometry(100, 100, 400, 200)
        self.parent_window = parent
        
        layout = QVBoxLayout()
        
        # Source Database or CSV File
        self.source_db = QLineEdit()
        self.source_db.setPlaceholderText("Select Source Database or CSV File")
        self.source_btn = QPushButton("Browse")
        self.source_btn.clicked.connect(self.select_source_file)
        
        source_layout = QHBoxLayout()
        source_layout.addWidget(self.source_db)
        source_layout.addWidget(self.source_btn)
        
        # Table Selection Combo Box
        self.table_combo = QComboBox()
        self.table_combo.setEnabled(False)
        
        # Target Database
        self.target_db = QLineEdit()
        self.target_db.setPlaceholderText("Select Target Database")
        self.target_btn = QPushButton("Browse")
        self.target_btn.clicked.connect(self.select_target_db)
        
        target_layout = QHBoxLayout()
        target_layout.addWidget(self.target_db)
        target_layout.addWidget(self.target_btn)
        
        # Overwrite or Update
        self.overwrite_radio = QRadioButton("Overwrite Table")
        self.update_radio = QRadioButton("Update Table")
        self.overwrite_radio.setChecked(True)
        
        # Import Button
        self.import_btn = QPushButton("Import Table")
        self.import_btn.setEnabled(False)
        self.import_btn.clicked.connect(self.import_table)
        
        layout.addLayout(source_layout)
        layout.addWidget(self.table_combo)
        layout.addLayout(target_layout)
        layout.addWidget(self.overwrite_radio)
        layout.addWidget(self.update_radio)
        layout.addWidget(self.import_btn)
        
        self.setLayout(layout)
    
    def select_source_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Source Database or CSV", "", "Database Files (*.db);;CSV Files (*.csv)")
        if file:
            self.source_db.setText(file)
            if file.endswith('.csv'):
                self.table_combo.clear()
                self.table_combo.addItem(os.path.basename(file).replace('.csv', ''))
                self.table_combo.setEnabled(True)
                self.import_btn.setEnabled(True)
            else:
                self.load_tables()
    
    def load_tables(self):
        """ Loads tables from the source database into the combo box """
        conn = sqlite3.connect(self.source_db.text())
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            self.table_combo.clear()
            self.table_combo.addItems(tables)
            self.table_combo.setEnabled(True)
            self.import_btn.setEnabled(True)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error loading tables: {e}")
        finally:
            conn.close()
    
    def select_target_db(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Target Database", "", "Database Files (*.db)")
        if file:
            self.target_db.setText(file)
    
    def import_table(self):
        """ Imports the selected table from source database or CSV into target database """
        source_file = self.source_db.text()
        target_db = self.target_db.text()
        table_name = self.table_combo.currentText()
        overwrite = self.overwrite_radio.isChecked()
        
        if not source_file or not target_db or not table_name:
            QMessageBox.warning(self, "Error", "Please select source, target, and table!")
            return
        
        if source_file.endswith('.csv'):
            self.import_from_csv(source_file, target_db, table_name, overwrite)
        else:
            self.import_from_database(source_file, target_db, table_name, overwrite)
    
    def import_from_database(self, source_db, target_db, table_name, overwrite):
        """ Imports a table from one database to another """
        source_conn = sqlite3.connect(source_db)
        source_cursor = source_conn.cursor()
        target_conn = sqlite3.connect(target_db)
        target_cursor = target_conn.cursor()
        
        try:
            # Get column names from source table
            source_cursor.execute(f"PRAGMA table_info({table_name})")
            source_columns = [row[1] for row in source_cursor.fetchall()]
            
            # Check if table exists in target
            target_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            existing_table = target_cursor.fetchone()
            
            if existing_table:
                if overwrite:
                    target_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                else:
                    # Get existing target columns
                    target_cursor.execute(f"PRAGMA table_info({table_name})")
                    target_columns = [row[1] for row in target_cursor.fetchall()]
                    
                    # Add missing columns to target table
                    for col in source_columns:
                        if col not in target_columns:
                            target_cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {col}")
            
            # Copy Data
            source_cursor.execute(f"SELECT * FROM {table_name}")
            rows = source_cursor.fetchall()
            placeholders = ', '.join(['?' for _ in source_columns])
            columns = ', '.join(source_columns)
            
            target_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
            target_cursor.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", rows)
            
            target_conn.commit()
            QMessageBox.information(self, "Success", "Table imported successfully!")
        
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error importing table: {e}")
        
        finally:
            source_conn.close()
            target_conn.close()
    
    def import_from_csv(self, csv_file, target_db, table_name, overwrite):
        """ Imports data from a CSV file into an SQLite table """
        target_conn = sqlite3.connect(target_db)
        target_cursor = target_conn.cursor()
        
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                columns = next(reader)  # First row as column names
                
                if overwrite:
                    target_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                
                column_def = ', '.join([f'"{col}" TEXT' for col in columns])
                target_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_def})")
                
                placeholders = ', '.join(['?' for _ in columns])
                target_cursor.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", reader)
                
                target_conn.commit()
                QMessageBox.information(self, "Success", "CSV file imported successfully!")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error importing CSV: {e}")
        
        finally:
            target_conn.close()
