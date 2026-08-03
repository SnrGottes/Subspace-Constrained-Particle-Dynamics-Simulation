import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QWidget, QPushButton, QDoubleSpinBox, QAbstractSpinBox
)
from src.config_loader import ConfigLoader

gui_settings = ConfigLoader.get_gui_settings()
sim_settings = ConfigLoader.get_sim_settings()

class DataSpinBox(QDoubleSpinBox):
    def __init__(self, min_v: float, max_v: float, default: float, step: float,  parent=None):
        super().__init__(parent)

        dec_str = str(step).split(".")
        count = len(dec_str) - 1

        self.setRange(min_v, max_v)
        self.setValue(default)
        self.setSingleStep(step)
        self.setDecimals(gui_settings['spin']['decimals'])
        self.setDecimals(count)
        self.setStyleSheet(self.styleSheet() + '''
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
            width: 8px;
            height: 10px;
            }
        ''')

class BaseButton(QPushButton):
    def __init__(self, text: str,  parent=None):
        super().__init__(parent)

        self.setText(text)
        self.setObjectName('base_button')

class AxisButton(QPushButton):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)

        self.setText(text)
        self.setObjectName('axis_button')

class ColorDisplayWidget(QWidget):
    def __init__(self, color: str, axis_number: int, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        label = QLabel(f'X<sub>{axis_number}</sub>:')
        widget = QWidget()

        layout.setContentsMargins(0,0,0,0)
        label.setObjectName('X_label')
        widget.setStyleSheet(f'background-color: {color}')

        layout.addWidget(label)
        layout.addWidget(widget)
        self.setLayout(layout)

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
        self.setLabel('left', f'Axis X<sub>{self.y_idx}</sub>')
        self.setLabel('bottom', f'Axis X<sub>{self.x_idx}</sub>')

    def _on_points_clicked(self):
        pass

    def edit_axis(self, changing_axis: str, axis: int):
        self.setLabel(changing_axis, f'Axis X<sub>{axis}</sub>')

    def edit_left_axis(self, axis: int):
        self.edit_axis('left', axis)

    def edit_bottom_axis(self, axis: int):
        self.edit_axis('bottom', axis)

class AxisSelectionWidget(QWidget):
    edit_axis_signal = pyqtSignal(int)

    def __init__(self, axis: int, widget_size: int, parent=None):
        super().__init__(parent)

        self.setFixedHeight(2)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.setFixedHeight(int(widget_size/2))

        self.axis = axis

        self.left_button = AxisButton('←')
        self.label = QLabel(f'X<sub>{self.axis}</sub')
        self.right_button = AxisButton('→')

        self.label.setObjectName('axis_label')

        self.left_button.clicked.connect(self.left_clicked)
        self.right_button.clicked.connect(self.right_clicked)

        for widget in [self.left_button, self.label, self.right_button]:
            self.layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(self.layout)

    def left_clicked(self):
        self.axis -= 1
        if self.axis <= 0:
            self.axis = sim_settings['constans']['axis_count']['value']

        self.button_clicked()

    def right_clicked(self):
        self.axis += 1
        if self.axis > sim_settings['constans']['axis_count']['value']:
            self.axis = 1

        self.button_clicked()

    def button_clicked(self):
        self.edit_axis_signal.emit(self.axis)
        self.label.setText(f"X<sub>{self.axis}</sub>")