from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton, QLabel, 
                           QLineEdit, QVBoxLayout, QWidget, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consulta de Atendimento")
        self.setFixedSize(600, 400)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create input section
        input_label = QLabel("Número do Atendimento:")
        input_label.setFont(QFont('Arial', 10))
        self.input_field = QLineEdit()
        self.input_field.setFixedHeight(30)
        self.input_field.setFont(QFont('Arial', 10))
        
        # Create button
        self.search_button = QPushButton("Consultar")
        self.search_button.setFixedHeight(40)
        self.search_button.setFont(QFont('Arial', 10))
        
        # Create result display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFont(QFont('Arial', 10))
        
        # Add widgets to layout
        layout.addWidget(input_label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_display)
        
        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0053A6;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
            }
        """) 