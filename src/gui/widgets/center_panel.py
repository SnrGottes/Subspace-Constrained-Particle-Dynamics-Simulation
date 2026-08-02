from PyQt6.QtWidgets import (QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QWidget)
from src.config_loader import ConfigLoader
from src.gui.widgets.base_components import GraphWidget, AxisSelectionWidget

gui_settings = ConfigLoader.get_gui_settings()

class CenterPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(gui_settings['panels']['center_width'])

        center_widget = QWidget()
        layout = QVBoxLayout(center_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        graph_layout = QHBoxLayout()
        axis_layout = QHBoxLayout()
        color_display_layout = QHBoxLayout()
        button_layout = QGridLayout()

        axis_layout.setContentsMargins(0, 0, 0, 0)

        axis_displayed, self.graph_widgets, self.axis_selection_widgets = 1, [], []
        for i in range(gui_settings['graph']['quantity_graph_widgets']):
            graph_size = gui_settings['panels']['center_width'] / gui_settings['graph']['quantity_graph_widgets']

            graph_widget = GraphWidget(
                graph_size, axis_displayed, axis_displayed+1
            )

            axis_selection_widget_1 = AxisSelectionWidget(axis_displayed, graph_size)
            axis_selection_widget_2 = AxisSelectionWidget(axis_displayed+1, graph_size)

            axis_selection_widget_1.edit_axis_signal.connect(graph_widget.edit_bottom_axis)
            axis_selection_widget_2.edit_axis_signal.connect(graph_widget.edit_left_axis)

            axis_displayed += 2

            self.graph_widgets.append(graph_widget)
            graph_layout.addWidget(graph_widget)

            self.axis_selection_widgets.append([
                axis_selection_widget_1,
                axis_selection_widget_2
            ])
            axis_layout.addWidget(axis_selection_widget_1)
            axis_layout.addWidget(axis_selection_widget_2)

        layout.addLayout(graph_layout)
        layout.addLayout(axis_layout)
        layout.addStretch()
        layout.addLayout(color_display_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)