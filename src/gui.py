from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QWidget, QPushButton)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.change_window_settings()

    def create_main_layout(self, layout_type, width=int):
        container = QWidget()
        container.setObjectName('sub_container')
        container.setFixedWidth(width)
        container.setStyleSheet('''
            QWidget#sub_container {
                background-color: #FFCCCC;
                border: 2px solid red;
                border-radius: 10%;
            }
        ''')

        inner_layout = layout_type()
        container.setLayout(inner_layout)

        inner_layout.setSpacing(0)
        
        return inner_layout, container

    def change_window_settings(self):
        self.setFixedSize(1400, 700)
        self.setWindowTitle('Subspace Constrained Particle Dynamics Simulation')

        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.setSpacing(10)

        left_layout, left_widget = self.create_main_layout(QVBoxLayout, 408)
        core_layout, core_widget = self.create_main_layout(QVBoxLayout, 544)
        right_layout, right_widget = self.create_main_layout(QVBoxLayout, 408)

        for widget in (left_widget, core_widget, right_widget):
            layout.addWidget(widget)

        self.setCentralWidget(central_widget)