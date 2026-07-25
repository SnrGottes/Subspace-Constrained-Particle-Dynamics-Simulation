from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QWidget, QPushButton, QDoubleSpinBox)

# enter size settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700
SIDE_PANEL_WIDTH = 420
CORE_PANEL_WIDTH = 560

STYLESHEET = '''
    QWidget#sub_container {
        border: 2px solid #b0b0b0;
    }
    QLabel#title {
        font-size:20px;
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

    # creates and configures a simple data entry field for two parameters
    def create_data_range_spin_box(self, min_v: float, max_v: float, default_min: float, default_max: float, step: float):
        spin_min, spin_max = QDoubleSpinBox(), QDoubleSpinBox()

        spin_min.setRange(min_v, max_v)
        spin_min.setValue(default_min)
        spin_min.setSingleStep(step)
        spin_min.setDecimals(4)

        spin_max.setRange(min_v, max_v)
        spin_max.setValue(default_max)
        spin_max.setSingleStep(step)
        spin_max.setDecimals(4)

        return spin_min, spin_max

    # creates and configures the program's default button 
    def create_btn(self, text: str, connect_func):
        btn = QPushButton(text)
        btn.clicked.connect(connect_func)
        btn.setMinimumSize(135, 50)
        return btn

    # adds fields for data entry in layout
    def add_row_get_data_range(self, layout, text: str, min, max, row: int):
        layout.addWidget(QLabel(text), row=row, column=0)
        layout.addWidget(min, row, 2)
        layout.addWidget(max, row, 3)

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

        # creates layouts for "left_layout"
        data_layout = QGridLayout()
        button_layout = QGridLayout()

        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

        # creates and configures title label for "left_layout" 
        title_label = QLabel('Enter data settings for simulation')
        title_label.setObjectName('title')
        left_layout.addWidget(title_label)

        # creates fields for data entry 
        self.mass_min, self.mass_max = self.create_data_range_spin_box(
            min_v=0.1, max_v=5.0, default_min=0.5, default_max=1, step=0.1)
        
        self.start_velocity_min, self.start_velocity_max = self.create_data_range_spin_box(
            min_v=0.0, max_v=50.0, default_min=1.0, default_max=30, step=0.1)

        # adds fields for data entry in "data_layout"
        self.add_row_get_data_range(layout=data_layout, text='Enter mass range: ',
                                     min=self.mass_min, max=self.mass_max, row=2)
        self.add_row_get_data_range(layout=data_layout, text='Enter start velocity range: ',
                                     min=self.start_velocity_min, max=self.start_velocity_max, row=3)

        # creates buttons to control the simulation
        save_btn = self.create_btn(text='save', connect_func=self.clicked_save)
        pause_btn = self.create_btn(text='pause', connect_func=self.clicked_pause)
        start_btn = self.create_btn(text='start', connect_func=self.clicked_start)

        for btn in [[save_btn, 0], [pause_btn, 1], [start_btn, 2]]:
            button_layout.addWidget(btn[0], 0, btn[1])

        # adds to "left_layout"
        left_layout.addLayout(data_layout)
        left_layout.addStretch()
        left_layout.addLayout(button_layout)

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