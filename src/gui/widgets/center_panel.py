from PyQt6.QtWidgets import (QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QWidget)
from src.config_loader import ConfigLoader
from src.gui.widgets.base_components import GraphWidget

gui_settings = ConfigLoader.get_gui_settings()

class CenterPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(gui_settings['panels']['center_width'])

        center_widget = QWidget()
        layout = QVBoxLayout(center_widget)

        center_widget.setStyleSheet('border: 2px solid #b0b0b0;')

        graph_layout = QHBoxLayout()
        axis_layout = QHBoxLayout()
        color_display_layout = QVBoxLayout()
        button_layout = QGridLayout()

        axis_displayed, self.graph_widgets = 1, []
        for i in range(gui_settings['graph']['quantity_graph_widgets']):
            graph_widget = GraphWidget(
                gui_settings['panels']['center_width'] / gui_settings['graph']['quantity_graph_widgets'],
                axis_displayed, axis_displayed+1)
            axis_displayed += 2
            self.graph_widgets.append(graph_widget)
            graph_layout.addWidget(graph_widget)

        layout.addLayout(graph_layout)
        layout.addLayout(axis_layout)
        layout.addStretch()
        layout.addLayout(color_display_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)