import pyqtgraph as pg
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QWidget, QPushButton, QDoubleSpinBox
)
from src.config_loader import ConfigLoader

settings = ConfigLoader.get_gui_settings()

class DataSpinBox(QDoubleSpinBox):
    def __init__(self, min_v: float, max_v: float, default: float, step: float,  parent=None):
        super().__init__(parent)

        self.setRange(min_v, max_v)
        self.setValue(default)
        self.setSingleStep(step)
        self.setDecimals(settings['spin']['decimals'])

class BaseButton(QPushButton):
    def __init__(self, text: str,  parent=None):
        super().__init__(parent)

        self.setText(text)
        self.setObjectName('standart_button')

class ColorDisplay(QWidget):
    def __init__(self, color: str, axis_number: int, parent=None):
        super().__init__(parent)

        self.setStyleSheet(f'background-color: {color}')

        layout = QHBoxLayout(self)
        label = QLabel(f'X<sub>{axis_number}</sub>')
        layout.addWidget(label)

class GraphWidget(pg.PlotWidget):
    def __init__(self, widget_size: int, x_axis_idx: int, y_axis_idx: int, parent=None):
        super().__init__(parent)
        self.x_idx = x_axis_idx
        self.y_idx = y_axis_idx

        self._configure_plot(int(widget_size))

        self.scatter = pg.ScatterPlotItem(pxMode=True, hoverable=True)
        self.addItem(self.scatter)

        self.scatter.sigClicked.connect(self._on_points_clicked)

    def _configure_plot(self, widget_size):
        self.showGrid(x=True, y=True)
        self.setTitle('')
        self.setFixedSize(widget_size, widget_size)
        self.setLabel('left', f'Axis {self.y_idx}')
        self.setLabel('bottom', f'Axis {self.x_idx}')

    def _on_points_clicked(self):
        pass