import pyqtgraph as pg
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QWidget, QPushButton, QDoubleSpinBox
)

# enter size settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 600
SIDE_PANEL_WIDTH = 350
CORE_PANEL_WIDTH = 700
AXIS_COLOR = ['#ff0000', '#ff00ff', '#00ff00', '#00ffff', '#0000ff', '#ffff00']
GRAPH_SIZE = 345
DECIMAL_PRECISION = 4
NUMBER_OF_AXES = 5

STYLESHEET = '''
    QWidget#sub_container {
        border: 2px solid #b0b0b0;
    }
    QLabel#title {
        font-size:23px;
    }
    QLabel#data_label {
        font-size: 10px;
    }
    QLabel#X_label {
        font-size: 20px;
    }
'''

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(STYLESHEET)
        self.setup_gui()

    # creates and configures the main layouts
    def create_main_layout(self, layout_type, width: int):
        container = QWidget()
        container.setObjectName('sub_container')
        container.setFixedWidth(width)

        inner_layout = layout_type()
        container.setLayout(inner_layout)
        return inner_layout, container

    # creates and configures a simple data entry field for a single parameter
    def create_data_spin_box(self, min_v: float, max_v: float, default: float, step: float):
            spin = QDoubleSpinBox()
    
            spin.setRange(min_v, max_v)
            spin.setValue(default)
            spin.setSingleStep(step)
            spin.setDecimals(DECIMAL_PRECISION)
    
            return spin

    # creates and configures a simple data entry field for two parameters
    def create_data_range_spin_box(self, min_v: float, max_v: float, default_min: float, default_max: float, step: float):
        spin_min, spin_max = QDoubleSpinBox(), QDoubleSpinBox()

        spin_min.setRange(min_v, max_v)
        spin_min.setValue(default_min)
        spin_min.setSingleStep(step)
        spin_min.setDecimals(DECIMAL_PRECISION)

        spin_max.setRange(min_v, max_v)
        spin_max.setValue(default_max)
        spin_max.setSingleStep(step)
        spin_max.setDecimals(DECIMAL_PRECISION)

        return spin_min, spin_max

    # creates and configures the program's default button 
    def create_btn(self, text: str, connect_func):
        btn = QPushButton(text)
        btn.clicked.connect(connect_func)
        return btn

    # сreates an object to display key graphical data from the simulation
    def create_graph_widget(self, graph_widget):
        graph_widget.setBackground('w')
        graph_widget.setTitle('')
        graph_widget.showGrid(x=True, y=True)
        graph_widget.setFixedSize(GRAPH_SIZE, GRAPH_SIZE)

        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        pen = pg.mkPen(color='r', width=3) 
        graph_widget.plot(x, y, pen=pen, name="Синусоида")

        return graph_widget

    # creates a simple widget for displaying a color associated with a specific coordinate axis
    def create_color_display(self, color: str):
        cd = QWidget()
        cd.setMinimumSize(30,30)
        cd.setStyleSheet(f'''
            background-color:{color};
            margins-radius: 5%;
            border: 2px solid #b0b0b0;
        ''')

        return cd

    # adds fields for data entry in layout
    def add_row_get_data(self, layout, text: str, spin, row: int):
        label = QLabel(text)
        label.setObjectName('data_label')
        layout.addWidget(label, row, 0)
        layout.addWidget(spin, row, 1)

    # adds fields for data entry in layout
    def add_row_get_data_range(self, layout, text: str, min, max, row: int):
        label = QLabel(text)
        label.setObjectName('data_label')
        layout.addWidget(label, row, 0)
        layout.addWidget(min, row, 1)
        layout.addWidget(max, row, 2)

    # Configures the main application interface
    def setup_gui(self):
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle('Subspace Constrained Particle Dynamics Simulation')

        # creates and configures central layout
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # creates main layouts
        left_layout, left_widget = self.create_main_layout(QVBoxLayout, SIDE_PANEL_WIDTH)
        core_layout, core_widget = self.create_main_layout(QVBoxLayout, CORE_PANEL_WIDTH)
        right_layout, right_widget = self.create_main_layout(QVBoxLayout, SIDE_PANEL_WIDTH)

        core_layout.setContentsMargins(5, 5, 5, 5)

        # "left_layout" setting
        # creates layouts for "left_layout"
        data_layout = QGridLayout()
        display_settings_layout = QHBoxLayout()

        # creates and configures title label for "left_layout" 
        title_label = QLabel('Enter data settings for simulation')
        title_label.setObjectName('title')
        left_layout.addWidget(title_label)

        # creates fields for data entry 
        self.mass_min, self.mass_max = self.create_data_range_spin_box(
            min_v=0.1, max_v=5.0, default_min=0.5, default_max=1, step=0.1)
        self.start_velocity_min, self.start_velocity_max = self.create_data_range_spin_box(
            min_v=0.0, max_v=50.0, default_min=1.0, default_max=30, step=0.1)
        self.dimensions = self.create_data_spin_box(min_v=3, max_v=8, default=6, step=1)

        # adds fields for data entry in "data_layout"
        self.add_row_get_data_range(layout=data_layout, text='Enter mass range: ',
                                    min=self.mass_min, max=self.mass_max, row=2)
        self.add_row_get_data_range(layout=data_layout, text='Enter start velocity range: ',
                                    min=self.start_velocity_min, max=self.start_velocity_max, row=3)
        self.add_row_get_data(layout=data_layout, text='Enter the simulation dimensions: ',
                                    spin=self.dimensions, row=4)

        # display the available coordinate axes, with colors representing them on the graph
        color_dialogs = []
        for i in range(0, NUMBER_OF_AXES):
            cd = self.create_color_display(color=AXIS_COLOR[i])
            cd_label = QLabel(f'X<sub>{i+1}</sub>')

            color_dialogs.append(cd)
            cd_label.setObjectName('X_label')

            display_settings_layout.addWidget(cd_label)
            display_settings_layout.addWidget(cd)

        # adds to "left_layout"
        left_layout.addLayout(data_layout)
        left_layout.addStretch()
        left_layout.addLayout(display_settings_layout)

        # "core_layout" setting
        # creates layouts for "core_layout" 
        graph_layout = QHBoxLayout()
        displayed_coordinates_layout = QHBoxLayout()
        button_layout = QGridLayout()

        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

        # creates chart widgets to visualize the simulation
        graph_widget_1 = self.create_graph_widget(pg.PlotWidget())
        graph_widget_2 = self.create_graph_widget(pg.PlotWidget())

        graph_layout.addWidget(graph_widget_1)
        graph_layout.addWidget(graph_widget_2)

        # creates buttons to control the simulation
        save_btn = self.create_btn(text='save', connect_func=self.clicked_save)
        pause_btn = self.create_btn(text='pause', connect_func=self.clicked_pause)
        start_btn = self.create_btn(text='start', connect_func=self.clicked_start)

        for btn in [[save_btn, 0], [pause_btn, 1], [start_btn, 2]]:
            button_layout.addWidget(btn[0], 0, btn[1])

        # adds to "core_layout"
        core_layout.addLayout(graph_layout)
        core_layout.addStretch()
        core_layout.addLayout(button_layout)

        # add main layouts in central layout 
        for widget in (left_widget, core_widget, right_widget):
            layout.addWidget(widget)

        self.setCentralWidget(central_widget)

    # functions for button responses 
    def clicked_save(self):
        pass
    
    def clicked_pause(self):
        pass
    
    def clicked_start(self):
        pass