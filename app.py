# gui.py
import sys
import glob
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from worker import Worker

class GroupImgGUI(QWidget):
    def __init__(self, parent=None):
        super(GroupImgGUI, self).__init__(parent)
        self.dir = None
        self.eps = 0.5
        self.min_samples = 5
        self.affinity = 'euclidean'
        self.linkage = 'ward'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AI-Grouping-GUI")
        self.setGeometry(100, 100, 400, 400) 

        layout = QVBoxLayout()

        self.select_folder_btn = QPushButton("Select Folder")
        self.select_folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.select_folder_btn)

        self.settings_groupbox = QGroupBox("Settings")
        settings_layout = QFormLayout()
        
        self.kmeans_spinbox = QSpinBox()
        self.kmeans_spinbox.setRange(3, 15)
        self.kmeans_spinbox.setValue(3)

        kmeans_info_button = QToolButton()
        kmeans_info_button.setIcon(QIcon.fromTheme("help-about"))
        kmeans_info_button.setToolTip("Number of clusters to form as well as the number of centroids to generate.")

        self.resample_spinbox = QSpinBox()
        self.resample_spinbox.setRange(32, 256)
        self.resample_spinbox.setValue(128)
        self.resample_spinbox.setSingleStep(2)

        resample_info_button = QToolButton()
        resample_info_button.setIcon(QIcon.fromTheme("help-about"))
        resample_info_button.setToolTip("The size to which each image will be resized before feature extraction.")

        self.algorithm_combobox = QComboBox()
        self.algorithm_combobox.addItems(["KMeans", "DBSCAN", "Agglomerative"])
        self.algorithm_combobox.currentTextChanged.connect(self.show_algorithm_parameters)

        algorithm_info_button = QToolButton()
        algorithm_info_button.setIcon(QIcon.fromTheme("help-about"))
        algorithm_info_button.setToolTip("Choose between KMeans, DBSCAN, and Agglomerative clustering algorithms.")

        self.move_checkbox = QCheckBox()
        self.size_checkbox = QCheckBox()

        settings_layout.addRow(QLabel("Number of Groups (KMeans):"), self.create_parameter_widget(self.kmeans_spinbox, kmeans_info_button))
        settings_layout.addRow(QLabel("Resample Size:"), self.create_parameter_widget(self.resample_spinbox, resample_info_button))
        settings_layout.addRow(QLabel("Algorithm:"), self.create_parameter_widget(self.algorithm_combobox, algorithm_info_button))
        settings_layout.addRow(QLabel("Move Files:"), self.move_checkbox)
        settings_layout.addRow(QLabel("Include Size in Features:"), self.size_checkbox)

        self.settings_groupbox.setLayout(settings_layout)
        layout.addWidget(self.settings_groupbox)

        self.dbscan_settings_groupbox = QGroupBox("DBSCAN Settings")
        dbscan_settings_layout = QFormLayout()

        self.eps_spinbox = QDoubleSpinBox()
        self.eps_spinbox.setRange(0.1, 10.0)
        self.eps_spinbox.setValue(0.5)
        self.eps_spinbox.setSingleStep(0.1)
        eps_info_button = QToolButton()
        eps_info_button.setIcon(QIcon.fromTheme("help-about"))
        eps_info_button.setToolTip("The maximum distance between two samples for one to be considered as in the neighborhood of the other.")

        self.min_samples_spinbox = QSpinBox()
        self.min_samples_spinbox.setRange(1, 100)
        self.min_samples_spinbox.setValue(5)
        min_samples_info_button = QToolButton()
        min_samples_info_button.setIcon(QIcon.fromTheme("help-about"))
        min_samples_info_button.setToolTip("The number of samples (or total weight) in a neighborhood for a point to be considered as a core point.")

        dbscan_settings_layout.addRow(QLabel("eps:"), self.create_parameter_widget(self.eps_spinbox, eps_info_button))
        dbscan_settings_layout.addRow(QLabel("min_samples:"), self.create_parameter_widget(self.min_samples_spinbox, min_samples_info_button))

        self.dbscan_settings_groupbox.setLayout(dbscan_settings_layout)
        self.dbscan_settings_groupbox.setVisible(False)
        layout.addWidget(self.dbscan_settings_groupbox)
        
        self.agglomerative_settings_groupbox = QGroupBox("Agglomerative Settings")
        agglomerative_settings_layout = QFormLayout()

        self.affinity_combobox = QComboBox()
        self.affinity_combobox.addItems(["euclidean", "l1", "l2", "manhattan", "cosine"])
        self.affinity_combobox.setCurrentText("euclidean")
        self.affinity_combobox.setToolTip("Affinity measures the distance between clusters in different ways.")
        
        affinity_info_button = QToolButton()
        affinity_info_button.setIcon(QIcon.fromTheme("help-about"))
        affinity_info_button.setToolTip(
            "Affinity measures the distance between clusters in different ways:\n"
            "- euclidean: Straight-line distance.\n"
            "- l1: Sum of absolute differences (Manhattan distance).\n"
            "- l2: Sum of squared differences (Euclidean distance).\n"
            "- manhattan: Distance along axes at right angles.\n"
            "- cosine: Cosine of the angle between vectors."
        )

        self.linkage_combobox = QComboBox()
        self.linkage_combobox.addItems(["ward", "complete", "average", "single"])
        self.linkage_combobox.setCurrentText("ward")
        self.linkage_combobox.setToolTip("Linkage determines the criterion for merging clusters.")
        
        linkage_info_button = QToolButton()
        linkage_info_button.setIcon(QIcon.fromTheme("help-about"))
        linkage_info_button.setToolTip(
            "Linkage determines the criterion for merging clusters:\n"
            "- ward: Minimizes the variance within clusters.\n"
            "- complete: Maximizes the distance between clusters.\n"
            "- average: Uses the average distance between clusters.\n"
            "- single: Minimizes the distance between clusters."
        )

        agglomerative_settings_layout.addRow(QLabel("Affinity:"), self.create_parameter_widget(self.affinity_combobox, affinity_info_button))
        agglomerative_settings_layout.addRow(QLabel("Linkage:"), self.create_parameter_widget(self.linkage_combobox, linkage_info_button))

        self.agglomerative_settings_groupbox.setLayout(agglomerative_settings_layout)
        self.agglomerative_settings_groupbox.setVisible(False)
        layout.addWidget(self.agglomerative_settings_groupbox)

        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.run)
        layout.addWidget(self.run_btn)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        self.progress_bar.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 20px;
            }
            """
        )
        layout.addWidget(self.progress_bar)

        self.status_bar = QStatusBar()
        layout.addWidget(self.status_bar)

        self.setLayout(layout)

    def create_parameter_widget(self, widget, info_button=None):
        layout = QHBoxLayout()
        layout.addWidget(widget)
        if info_button:
            layout.addWidget(info_button)
        container = QWidget()
        container.setLayout(layout)
        return container

    def show_algorithm_parameters(self):
        self.agglomerative_settings_groupbox.setVisible(False)
        self.dbscan_settings_groupbox.setVisible(False)
        if self.algorithm_combobox.currentText() == "DBSCAN":
            self.dbscan_settings_groupbox.setVisible(True)
        elif self.algorithm_combobox.currentText() == "Agglomerative":
            self.agglomerative_settings_groupbox.setVisible(True)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.dir = folder
            self.select_folder_btn.setText(self.dir)

    def run(self):
        if not self.dir:
            QMessageBox.warning(self, "Error", "No folder selected!")
            return

        self.status_bar.showMessage("Processing...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        types = ('*.jpg', '*.JPG', '*.png', '*.jpeg')
        image_paths = []
        folder = self.dir
        if not folder.endswith("/"):
            folder += "/"
        for files in types:
            image_paths.extend(sorted(glob.glob(folder + files)))
        nimages = len(image_paths)
        if nimages <= 0:
            QMessageBox.warning(self, "Error", 'No images found!')
            self.progress_bar.setVisible(False)
            return

        self.worker = Worker(
            image_paths=image_paths,
            folder=folder,
            kmeans_value=self.kmeans_spinbox.value(),
            resample_value=self.resample_spinbox.value(),
            algorithm=self.algorithm_combobox.currentText().lower(),
            move_files=self.move_checkbox.isChecked(),
            eps=self.eps_spinbox.value(),
            min_samples=self.min_samples_spinbox.value(),
            affinity=self.affinity_combobox.currentText(),
            linkage=self.linkage_combobox.currentText()
        )

        self.worker.signals.progress.connect(self.update_progress)
        self.worker.signals.finished.connect(self.work_finished)
        self.worker.signals.message.connect(self.show_message)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        QCoreApplication.processEvents()  # Ensure the GUI updates

    def work_finished(self, success):
        if success:
            QMessageBox.information(self, "Done", 'Processing complete!')
        else:
            QMessageBox.warning(self, "Error", 'Processing failed!')
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Done!", 5000)

    def show_message(self, level, message):
        if level == "info":
            QMessageBox.information(self, "Info", message)
        elif level == "warning":
            QMessageBox.warning(self, "Warning", message)
        elif level == "error":
            QMessageBox.critical(self, "Error", message)

def main():
    app = QApplication(sys.argv)
    window = GroupImgGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
