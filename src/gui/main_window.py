import pyqtgraph as pg
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QWidget, QPushButton, QDoubleSpinBox
)
from src.config_loader import ConfigLoader
from src.gui.widgets.input_panel import InputPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_configuration()
        self.layout_configuration()

    def window_configuration(self):
        window_settings = ConfigLoader.get_gui_settings()['main_window']
        self.setMinimumSize(
            window_settings['width'],
            window_settings['height']
        )
        self.setWindowTitle(window_settings['title'])

    def layout_configuration(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        input_panel = InputPanel()
        layout.addWidget(input_panel)

        self.setCentralWidget(widget)