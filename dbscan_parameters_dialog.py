from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class DBSCANParametersDialog(QDialog):
    def __init__(self, parent=None):
        super(DBSCANParametersDialog, self).__init__(parent)
        self.setWindowTitle("DBSCAN Parameters")
        self.setGeometry(100, 100, 300, 200)
        
        layout = QFormLayout()
        
        self.eps_spinbox = QDoubleSpinBox()
        self.eps_spinbox.setRange(0.1, 10.0)
        self.eps_spinbox.setValue(0.5)
        self.eps_spinbox.setSingleStep(0.1)
        
        self.min_samples_spinbox = QSpinBox()
        self.min_samples_spinbox.setRange(1, 100)
        self.min_samples_spinbox.setValue(5)
        
        eps_info_button = QToolButton()
        eps_info_button.setIcon(QIcon.fromTheme("help-about"))
        eps_info_button.setToolTip("The maximum distance between two samples for one to be considered as in the neighborhood of the other.")
        
        min_samples_info_button = QToolButton()
        min_samples_info_button.setIcon(QIcon.fromTheme("help-about"))
        min_samples_info_button.setToolTip("The number of samples (or total weight) in a neighborhood for a point to be considered as a core point.")
        
        eps_layout = QHBoxLayout()
        eps_layout.addWidget(self.eps_spinbox)
        eps_layout.addWidget(eps_info_button)
        
        min_samples_layout = QHBoxLayout()
        min_samples_layout.addWidget(self.min_samples_spinbox)
        min_samples_layout.addWidget(min_samples_info_button)
        
        layout.addRow(QLabel("eps:"), eps_layout)
        layout.addRow(QLabel("min_samples:"), min_samples_layout)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        
        layout.addWidget(self.ok_button)
        self.setLayout(layout)
        
    def get_parameters(self):
        return self.eps_spinbox.value(), self.min_samples_spinbox.value()
