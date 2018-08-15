from aqt.qt import *


class InputDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.input_values = None
        self._init_ui()

    def _init_ui(self):
        self.setGeometry(20, 20, 480, 360)
        self.layout = QVBoxLayout()

        self._init_input()
        self._init_spinbox()
        self._init_buttons()

        self.setLayout(self.layout)

    def _init_input(self):
        self.input_label = QLabel("Insert in each line a word:")
        self.input_box = QPlainTextEdit(self)

        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_box)

    def _init_spinbox(self):
        self.amount_label = QLabel("Definitions: ")
        self.amount_spinbox = QSpinBox()
        self.amount_spinbox.setMinimum(1)
        self.amount_spinbox.setMaximum(50)
        self.amount_spinbox.setValue(10)

        self.amount_layout = QHBoxLayout()
        self.amount_layout.addWidget(self.amount_label)
        self.amount_layout.addWidget(self.amount_spinbox)
        self.layout.addLayout(self.amount_layout)

    def _init_buttons(self):
        self.import_button = QPushButton("Import")
        self.import_button.clicked.connect(self.on_import_click)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.import_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_layout)

    def on_import_click(self):
        text = self.input_box.toPlainText()
        if len(text) > 0:
            definition_amount = self.amount_spinbox.value()
            self.input_values = [text, definition_amount]
            self.close()

    def run(self):
        self.exec_()
        return self.input_values
