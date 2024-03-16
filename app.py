import sys

from PyQt6.QtCore import QTimer

from cmo import System
import theory_calc
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QSpinBox, QFormLayout, \
    QSpacerItem, QSizePolicy, QPushButton, QTextEdit, QHBoxLayout, QGraphicsColorizeEffect, QTableWidget, \
    QTableWidgetItem, QHeaderView, QMessageBox
from PyQt6.QtGui import QFont, QIcon, QColor

params = {'lumb': 3, 'nu': 2, 'N': 10, 'max_time': 100}
timestep = 0.01

spinbox_style = f"""
                    QSpinBox {{
                        border: 2px solid #FFC9DD;
                        border-radius: 4px;
                        background-color: white;
                        font-family: 'Inter';
                        font-size: 12px;
                    }}
                    QSpinBox::up-button {{
                        background-color: #FFC9DD;
                        image: url(icons/chevron-up.svg);
                        border: none;
                    }}
                    QSpinBox::up-button:pressed {{
                        background-color: #FF589D;
                    }}
                    QSpinBox::down-button {{
                        background-color: #FFC9DD;
                        image: url(icons/chevron-down.svg);
                        border: none;
                    }}
                    QSpinBox::down-button:pressed {{
                        background-color: #FF589D;
                    }}
                """
button_style = """
                    QPushButton {
                        background-color: #F72585;
                        border-radius: 4px;
                        color: white;
                        font-family: 'Inter';
                        font-size: 16px;
                        font-weight: Bold;
                        padding: 8px 16px;
                    }
                    QPushButton:hover {
                        background-color: #FF7EB2;
                    }
                    QPushButton:pressed {
                        background-color: #C40060;
                    }
                """

secondary_button_style = """
                    QPushButton {
                        background-color: None;
                        border: 1px solid #F72585;
                        border-radius: 4px;
                        color: #F72585;
                        font-family: 'Inter';
                        font-size: 16px;
                        font-weight: Bold;
                        padding: 8px 16px;
                    }
                    QPushButton:hover {
                        background-color: #FF7EB2;
                    }
                    QPushButton:pressed {
                        background-color: #C40060;
                    }
                """

message_style_widget = """
                    QTextEdit {
                        background-color: #F6FCFF;
                        border: 1px solid #FFC9DD;
                        border-radius: 6px;
                        font-family: Inter;
                        font-weight: Light;
                        font-size: 10px;
                    }
                    QScrollBar:vertical {
                        background: #FFC9DD;
                        width: 10px;
                        margin: 0px 0px 0px 0px;
                        border: 1px solid #FFC9DD;
                    }
                    """
table_style = """
QTableWidget {
    background-color: white;
    border: 1px solid #FFC9DD;
    border-radius: 6px;
    font-family: Inter;
    font-weight: 500; /* Regular is not a valid value for font-weight, use 400 for Regular */
    font-size: 12px;
    gridline-color: #FFC9DD;
}

QTableWidget::item {
    padding: 5px;
}

QHeaderView::section {
    background-color: #FFEDF4;
    font-weight: Medium;
    border: none;
}

QScrollBar:vertical {
    background: #FFC9DD;
    width: 10px;
    margin: 0px 0px 0px 0px;
    border: 1px solid #FFC9DD;
}
"""

class SimulationScreen(QMainWindow):
    def __init__(self, input_screen):
        super().__init__()

        self.cmo = System(params)

        self.input_screen = input_screen

        self.setWindowTitle("Simulation")
        self.setGeometry(50,50,800,600)
        self.setStyleSheet("background-color: #EAF5FA; padding: 6px;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # кнопки сверху

        buttons_layout = QHBoxLayout()
        buttons_layout. setSpacing(20)

        back_button = QPushButton("Назад")
        back_button.setStyleSheet(secondary_button_style)
        back_button.clicked.connect(self.go_back)
        buttons_layout.addWidget(back_button)

        change_speed_button = QPushButton("Ускорить x10")
        change_speed_button.setStyleSheet(button_style)
        change_speed_button.pressed.connect(self.change_interval)
        change_speed_button.released.connect(self.reset_interval)
        buttons_layout.addWidget(change_speed_button)

        layout.addLayout(buttons_layout)

        # ОЧЕРЕДЬ

        self.squares = [QWidget() for _ in range(params['N'])]
        self.circle = QWidget()
        for square in self.squares:
            square.setFixedSize(20, 20)
            square.setStyleSheet("background-color: white; border: 1px solid #F72585;")
        self.circle.setFixedSize(20, 20)
        self.circle.setStyleSheet("background-color: white; border: 1px solid #F72585; border-radius: 10px;")

        # стрелочки
        arrow = QIcon("icons/arrow-right-thin.svg")
        self.arrow_in_label = QLabel()
        self.arrow_in_label.setPixmap(arrow.pixmap(20, 20))

        self.arrow_out_label = QLabel()
        self.arrow_out_label.setPixmap(arrow.pixmap(20, 20))

        self.arrow_in_label.setStyleSheet("background-color: #EAF5FA; border: 1px solid #F72585;")
        self.arrow_out_label.setStyleSheet("background-color: #EAF5FA; border: 1px solid #F72585;")

        arrow_color = QGraphicsColorizeEffect()
        arrow_color.setColor(QColor(255, 164, 199))

        self.arrow_in_label.setGraphicsEffect(arrow_color)
        self.arrow_out_label.setGraphicsEffect(arrow_color)

        # очередь
        queue_layout = QHBoxLayout()
        queue_layout.setSpacing(4)
        for square in self.squares:
            queue_layout.addWidget(square)
        queue_layout.addWidget(self.arrow_in_label)
        queue_layout.addWidget(self.circle)
        queue_layout.addWidget(self.arrow_out_label)
        layout.addLayout(queue_layout)

        # сообщения
        self.message_widget = QTextEdit()
        self.message_widget.setReadOnly(True)
        self.message_widget.setStyleSheet(message_style_widget)
        self.message_widget.setMaximumHeight(160)
        layout.addWidget(self.message_widget)

        # таблицы
        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(8)

        # ТЕОРЕТИЧЕСКАЯ ТАБЛИЦА
        theory_layout = QVBoxLayout()

        theory_table_label = QLabel("Теоретические значения")
        theory_table_font = QFont("Inter", 12, QFont.Weight.Bold)
        theory_table_label.setFont(theory_table_font)
        theory_table_label.setStyleSheet("QLabel { color : #F72585; }")

        theory_layout.addWidget(theory_table_label)
        theory_layout.setSpacing(4)

        self.theory_values = theory_calc.calculate_theoretic_values(params['lumb'], params['nu'], params['N'])

        self.other_values = {
            'P_rej': self.theory_values.P_rej,
            'P_queue': self.theory_values.P_queue,
            'Q': self.theory_values.Q,
            'A': self.theory_values.A,
            'L_hand': self.theory_values.L_hand,
            'L_queue': self.theory_values.L_queue,
            'L_system': self.theory_values.L_system,
            'T_queue': self.theory_values.T_queue,
            'T_hand': self.theory_values.T_hand,
            'T_system': self.theory_values.T_system
        }

        self.theory_table = QTableWidget()
        self.theory_table.setRowCount(len(self.theory_values.lim_distribution) + 10)
        self.theory_table.setColumnCount(2)
        self.theory_table.setHorizontalHeaderLabels(['Parameter', 'Value'])

        header = self.theory_table.horizontalHeader()
        header.setFont(QFont("Inter", 10))

        self.theory_table.setColumnWidth(0, 80)
        self.theory_table.setColumnWidth(1, 80)

        self.theory_table.horizontalHeader().setFixedHeight(40)
        self.theory_table.verticalHeader().setVisible(False)

        for i, value in enumerate(self.theory_values.lim_distribution):
            self.theory_table.setItem(i, 0, QTableWidgetItem(f'Distribution {i}'))
            formatted_value = "{:.6f}".format(value)
            self.theory_table.setItem(i, 1, QTableWidgetItem(formatted_value))

        for i, (key, value) in enumerate(self.other_values.items(), start=len(self.theory_values.lim_distribution)):
            self.theory_table.setItem(i, 0, QTableWidgetItem(key))
            formatted_value = "{:.6f}".format(value)
            self.theory_table.setItem(i, 1, QTableWidgetItem(formatted_value))

        theory_layout.addWidget(self.theory_table)
        theory_layout.setStretchFactor(self.theory_table, 1)

        self.theory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.theory_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.theory_table.setStyleSheet(table_style)

        tables_layout.addLayout(theory_layout)

        # ЭКСПЕРИМЕНТАЛЬНАЯ ТАБЛИЦА

        experiment_layout = QVBoxLayout()
        experiment_layout.setSpacing(4)

        experiment_table_label = QLabel("Текущие экспериментальные значения")
        experiment_table_font = QFont("Inter", 12, QFont.Weight.Bold)
        experiment_table_label.setFont(experiment_table_font)
        experiment_table_label.setStyleSheet("QLabel { color : #F72585; }")

        experiment_layout.addWidget(experiment_table_label)

        self.experiment_values = self.cmo.values

        self.experiment_other_values = {
            'P_rej': self.experiment_values.P_rej,
            'P_queue': self.experiment_values.P_queue,
            'Q': self.experiment_values.Q,
            'A': self.experiment_values.A,
            'L_hand': self.experiment_values.L_hand,
            'L_queue': self.experiment_values.L_queue,
            'L_system': self.experiment_values.L_system,
            'T_queue': self.experiment_values.T_queue,
            'T_hand': self.experiment_values.T_hand,
            'T_system': self.experiment_values.T_system
        }

        self.experiment_table = QTableWidget()
        self.experiment_table.setRowCount(len(self.theory_values.lim_distribution) + 10)
        self.experiment_table.setColumnCount(2)
        self.experiment_table.setHorizontalHeaderLabels(['Parameter', 'Value'])

        experiment_header = self.experiment_table.horizontalHeader()
        experiment_header.setFont(QFont("Inter", 10))

        self.experiment_table.setColumnWidth(0, 80)
        self.experiment_table.setColumnWidth(1, 80)

        self.experiment_table.horizontalHeader().setFixedHeight(40)
        self.experiment_table.verticalHeader().setVisible(False)

        for i, value in enumerate(self.experiment_values.lim_distribution):
            self.experiment_table.setItem(i, 0, QTableWidgetItem(f'Distribution {i}'))
            formatted_value = "{:.6f}".format(value)
            self.experiment_table.setItem(i, 1, QTableWidgetItem(formatted_value))

        for i, (key, value) in enumerate(self.experiment_other_values.items(), start=len(self.experiment_values.lim_distribution)):
            self.experiment_table.setItem(i, 0, QTableWidgetItem(key))
            formatted_value = "{:.6f}".format(value)
            self.experiment_table.setItem(i, 1, QTableWidgetItem(formatted_value))

        experiment_layout.addWidget(self.experiment_table)
        experiment_layout.setStretchFactor(self.experiment_table, 1)

        self.experiment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.experiment_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.experiment_table.setStyleSheet(table_style)

        tables_layout.addLayout(experiment_layout)

        layout.addLayout(tables_layout)

        central_widget.setLayout(layout)

        self.cmo.request_in_queue.connect(self.update_message_widget)
        self.cmo.request_in_queue.connect(self.update_squares_in)

        self.cmo.request_in_handler.connect(self.update_squares_out)
        self.cmo.request_in_handler.connect(self.update_circle_in)
        self.cmo.request_in_handler.connect(self.update_message_widget)
        self.cmo.request_in_handler.connect(lambda: self.update_arrow_in(self.arrow_in_label))

        self.cmo.request_has_proccesed.connect(self.update_message_widget)
        self.cmo.request_has_proccesed.connect(self.update_circle_out)
        self.cmo.request_has_proccesed.connect(lambda: self.update_arrow_in(self.arrow_out_label))
        self.cmo.request_has_proccesed.connect(self.update_experimental_table)

        self.cmo.request_cancelled.connect(self.update_message_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.handle_next_request)
        self.timer.start(100)

    def handle_next_request(self):
        try:
            next_request = next(self.cmo.__iter__())
        except StopIteration:
            # Все запросы обработаны
            self.timer.stop()
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("Информация")
            msgBox.setText("Все запросы обработаны!")
            msgBox.setStyleSheet("""
                        QMessageBox {
                            background-color: #C0E2F1;
                        }
                        QMessageBox QLabel {
                            font-family: Inter;
                            font-size: 16px;
                            color: #005572;
                        }
                    """)
            msgBox.exec()

    def update_squares_in(self):
        for square in reversed(self.squares):
            if square.styleSheet() == "background-color: white; border: 1px solid #F72585;":
                square.setStyleSheet("background-color: #FF7EB2; border: 1px solid #F72585;")
                break

    def update_squares_out(self):
        for square in self.squares:
            if square.styleSheet() != "background-color: white; border: 1px solid #F72585;":
                square.setStyleSheet("background-color: white; border: 1px solid #F72585;")
                break

    def update_circle_in(self):
        self.circle.setStyleSheet("background-color: #FF7EB2; border: 1px solid #F72585; border-radius: 10px;")

    def update_circle_out(self):
        self.circle.setStyleSheet("background-color: white; border: 1px solid #F72585; border-radius: 10px;")

    def update_arrow_in(self, label):
        color_on = QGraphicsColorizeEffect()
        color_on.setColor(QColor(196, 0, 96))

        arrow_color = QGraphicsColorizeEffect()
        arrow_color.setColor(QColor(255, 164, 199))

        label.setGraphicsEffect(color_on)
        QTimer.singleShot(100, lambda: label.setGraphicsEffect(arrow_color))

    def update_experimental_table(self):

        self.experiment_values = self.cmo.values

        self.experiment_other_values = {
            'P_rej': self.experiment_values.P_rej,
            'P_queue': self.experiment_values.P_queue,
            'Q': self.experiment_values.Q,
            'A': self.experiment_values.A,
            'L_hand': self.experiment_values.L_hand,
            'L_queue': self.experiment_values.L_queue,
            'L_system': self.experiment_values.L_system,
            'T_queue': self.experiment_values.T_queue,
            'T_hand': self.experiment_values.T_hand,
            'T_system': self.experiment_values.T_system
        }

        self.experiment_table.setRowCount(0)

        for i, value in enumerate(self.experiment_values.lim_distribution):
            self.experiment_table.insertRow(i)
            self.experiment_table.setItem(i, 0, QTableWidgetItem(f'Distribution {i}'))
            formatted_value = "{:.6f}".format(value)
            self.experiment_table.setItem(i, 1, QTableWidgetItem(formatted_value))

        for i, (key, value) in enumerate(self.experiment_other_values.items(),
                                         start=len(self.experiment_values.lim_distribution)):
            self.experiment_table.insertRow(i)
            self.experiment_table.setItem(i, 0, QTableWidgetItem(key))
            formatted_value = "{:.6f}".format(value)
            self.experiment_table.setItem(i, 1, QTableWidgetItem(formatted_value))

    def go_back(self):
        self.input_screen.show()
        self.hide()

    def update_message_widget(self, message):
        if message == "Запрос обработался":
            color = '#1B8900'
            font_weight = 'Regular'
        elif message == "Запрос отклонен":
            color = '#C40060'
            font_weight = 'Regular'
        else:
            color = '#393939'
            font_weight = 'Light'

        formatted_message = f'<span style="color:{color}; font-weight: {font_weight};">{message}</span>'
        self.message_widget.append(formatted_message)

    def change_interval(self):
        self.timer.setInterval(10)

    def reset_interval(self):
        self.timer.setInterval(100)

class InputScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("M/M/1/N Quering System")
        self.setGeometry(50,50,400,400)
        self.setStyleSheet("background-color: #EAF5FA; padding: 6px;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setSpacing(20)

        spacer = QSpacerItem(0, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        layout.addItem(spacer)

        # Название
        title_label = QLabel("M/M/1/N Quering System")
        title_font = QFont("Inter", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("QLabel { color : #F72585; }")
        layout.addWidget(title_label)

        # ИНПУТЫ
        input_layout = QFormLayout()
        input_layout.setSpacing(8)

        instructions_label = QLabel("Введите параметры")
        instructions_font = QFont("Inter", 14, QFont.Weight.DemiBold)
        instructions_label.setFont(instructions_font)
        instructions_label.setStyleSheet("QLabel { color : #0093B7; }")
        layout.addWidget(instructions_label)

        spacer = QSpacerItem(0, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        layout.addItem(spacer)

        # lumb
        intensity_label = QLabel("Интенсивность поступления")
        intensity_font = QFont("Inter", 12)
        intensity_label.setFont(intensity_font)
        self.intensity_spinbox = QSpinBox()
        self.intensity_spinbox.setRange(1, 50)
        self.intensity_spinbox.setStyleSheet(spinbox_style)
        input_layout.addRow(intensity_label, self.intensity_spinbox)

        spacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        input_layout.addItem(spacer)

        # nu
        service_label = QLabel("Интенсивность обслуживания")
        service_font = QFont("Inter", 12)
        service_label.setFont(service_font)
        self.service_spinbox = QSpinBox()
        self.service_spinbox.setRange(1, 50)
        self.service_spinbox.setStyleSheet(spinbox_style)
        input_layout.addRow(service_label, self.service_spinbox)

        spacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        input_layout.addItem(spacer)

        # N
        max_requests_label = QLabel("Максимальное количество запросов, которые могут находиться в системе одновременно")
        max_requests_font = QFont("Inter", 12)
        max_requests_label.setFont(max_requests_font)
        self.max_requests_spinbox = QSpinBox()
        self.max_requests_spinbox.setRange(1, 20)
        self.max_requests_spinbox.setStyleSheet(spinbox_style)
        input_layout.addRow(max_requests_label, self.max_requests_spinbox)

        spacer = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        input_layout.addItem(spacer)

        layout.addLayout(input_layout)

        spacer = QSpacerItem(0, 16, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        input_layout.addItem(spacer)

        start_simulation_button = QPushButton("Начать симуляцию")
        start_simulation_button.setStyleSheet(button_style)

        start_simulation_button.clicked.connect(self.start_simulation)
        layout.addWidget(start_simulation_button)

        spacer = QSpacerItem(0, 200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        layout.addItem(spacer)

        central_widget.setLayout(layout)

    def start_simulation(self):

        params['lumb'] = self.intensity_spinbox.value()
        params['nu'] = self.service_spinbox.value()
        params['N'] = self.max_requests_spinbox.value()

        self.second_screen = SimulationScreen(self)
        self.second_screen.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication([])
    window = InputScreen()
    window.show()
    sys.exit(app.exec())