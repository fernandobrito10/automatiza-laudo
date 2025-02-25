from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton, QLabel, 
                           QLineEdit, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consulta de Atendimento")
        self.setFixedSize(800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Create top section with search
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create input section
        self.input_field = QLineEdit()
        self.input_field.setFixedHeight(40)
        self.input_field.setFont(QFont('Arial', 12))
        self.input_field.setPlaceholderText("Digite o número do atendimento")
        
        # Create button
        self.search_button = QPushButton("Buscar")
        self.search_button.setFixedSize(100, 40)
        self.search_button.setFont(QFont('Arial', 12))
        
        # Add widgets to top layout
        top_layout.addWidget(self.input_field)
        top_layout.addWidget(self.search_button)
        
        # Create result display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFont(QFont('Arial', 12))
        
        # Add all sections to main layout
        main_layout.addWidget(top_widget)
        main_layout.addWidget(self.result_display)
        
        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d3fdc;
            }
            QWidget {
                background-color: #0d3fdc;
            }
            QPushButton {
                background-color: white;
                color: #0d3fdc;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QLineEdit {
                padding: 5px 10px;
                border: 2px solid white;
                border-radius: 5px;
                color: #333;
                background-color: white;
            }
            QTextEdit {
                border: 2px solid white;
                border-radius: 5px;
                padding: 10px;
                color: white;
                background-color: rgba(255, 255, 255, 0.1);
            }
        """) 