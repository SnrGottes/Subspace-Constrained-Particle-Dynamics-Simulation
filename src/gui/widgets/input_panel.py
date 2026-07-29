from PyQt6.QtWidgets import (QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QWidget)
from src.config_loader import ConfigLoader
from src.gui.widgets.base_components import DataSpinBox, BaseButton

gui_settings = ConfigLoader.get_gui_settings()
sim_settings = ConfigLoader.get_sim_settings()

class InputPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(gui_settings['panels']['side_width'])

        layout = QVBoxLayout()
        parm_layout = QGridLayout()
        button_layout = QHBoxLayout()

        title_label = QLabel('Enter data settings for simulation')
        title_label.setObjectName('title')

        self.input_double_rows, self.input_single_rows, row = {}, {}, 0

        for value_name in sim_settings['settings_list']['range_parameters']:
            neu_row = self.create_double_input_row(
                value_name=value_name, 
                value_data=sim_settings['range_parameters'][value_name]
            )
            self.input_double_rows.update({value_name: neu_row})

            parm_layout.addWidget(neu_row[0], row, 0)
            parm_layout.addWidget(neu_row[1], row, 1)
            parm_layout.addWidget(neu_row[2], row, 2)

            row += 1

        for value_name in sim_settings['settings_list']['parameters']:
            neu_row = self.create_single_input_row(
                value_name=value_name, 
                value_data=sim_settings['parameters'][value_name]
            )
            self.input_single_rows.update({value_name: neu_row})
        
            parm_layout.addWidget(neu_row[0], row, 0)
            parm_layout.addWidget(neu_row[1], row, gui_settings['panels']['parm_layout_column']-1, 1, 2)
        
            row += 1

        reset_button = BaseButton('reset settings')
        reset_button.clicked.connect(self.reset_clicked)
        button_layout.addWidget(reset_button)

        save_button = BaseButton('save settings')
        save_button.clicked.connect(self.save_clicked)
        button_layout.addWidget(save_button)

        layout.addWidget(title_label)
        layout.addLayout(parm_layout)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def create_double_input_row(self, value_name: str, value_data: dict):
        label = QLabel(f'Enter {value_name} value: ')

        min_spin_box = DataSpinBox(
            value_data['min_value'], value_data['max_value'],
            value_data['min_range'], value_data['step'])
        
        max_spin_box = DataSpinBox(
            value_data['min_value'], value_data['max_value'],
            value_data['max_range'], value_data['step'])

        return [label, min_spin_box, max_spin_box]

    def create_single_input_row(self, value_name: str, value_data: dict):
            label = QLabel(f'Enter {value_name} value: ')
    
            spin_box = DataSpinBox(
                value_data['min_value'], value_data['max_value'],
                value_data['value'], value_data['step'])
    
            return [label, spin_box]

    def get_settings(self):
        data = sim_settings
        for value_name in sim_settings['settings_list']['range_parameters']:
            min = self.input_double_rows[value_name][1]
            max = self.input_double_rows[value_name][2]

            data['range_parameters'][value_name]['min_range'] = self.input_double_rows[value_name][1].value()
            data['range_parameters'][value_name]['max_range'] = self.input_double_rows[value_name][2].value()

        for value_name in sim_settings['settings_list']['parameters']:
            value = self.input_single_rows[value_name][1]
            data['parameters'][value_name]['value'] = value.value()

        return data
    
    def reset_clicked(self):
        pass

    def save_clicked(self):
        data = self.get_settings()
        ConfigLoader.update_sim_settings(data)