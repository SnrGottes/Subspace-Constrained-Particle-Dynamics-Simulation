from PyQt6.QtWidgets import (QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QWidget)
from src.config_loader import ConfigLoader
from src.gui.widgets.base_components import DataSpinBox, BaseButton

gui_settings = ConfigLoader.get_gui_settings()

class InspectorPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(gui_settings['panels']['side_width'])