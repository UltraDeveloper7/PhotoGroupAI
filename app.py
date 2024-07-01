import sys
import glob
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from worker import Worker
from dbscan_parameters_dialog import DBSCANParametersDialog

class GroupImgGUI(QWidget):
    def __init__(self, parent=None):
        super(GroupImgGUI, self).__init__(parent)
        self.dir = None
        self.eps = 0.5
        self.min_samples = 5
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AI-Grouping-GUI")
        self.setGeometry(100, 100, 400, 300)

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
        self.algorithm_combobox.addItems(["KMeans", "DBSCAN"])
        self.algorithm_combobox.currentTextChanged.connect(self.show_dbscan_parameters)

        algorithm_info_button = QToolButton()
        algorithm_info_button.setIcon(QIcon.fromTheme("help-about"))
        algorithm_info_button.setToolTip("Choose between KMeans and DBSCAN clustering algorithms.")

        self.move_checkbox = QCheckBox()
        self.size_checkbox = QCheckBox()

        settings_layout.addRow(QLabel("Number of Groups (KMeans):"), self.create_parameter_widget(self.kmeans_spinbox, kmeans_info_button))
        settings_layout.addRow(QLabel("Resample Size:"), self.create_parameter_widget(self.resample_spinbox, resample_info_button))
        settings_layout.addRow(QLabel("Algorithm:"), self.create_parameter_widget(self.algorithm_combobox, algorithm_info_button))
        settings_layout.addRow(QLabel("Move Files:"), self.move_checkbox)
        settings_layout.addRow(QLabel("Include Size in Features:"), self.size_checkbox)

        self.settings_groupbox.setLayout(settings_layout)
        layout.addWidget(self.settings_groupbox)

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

    def create_parameter_widget(self, widget, info_button):
        layout = QHBoxLayout()
        layout.addWidget(widget)
        layout.addWidget(info_button)
        container = QWidget()
        container.setLayout(layout)
        return container

    def show_dbscan_parameters(self):
        if self.algorithm_combobox.currentText() == "DBSCAN":
            dialog = DBSCANParametersDialog(self)
            if dialog.exec() == QDialog.Accepted:
                self.eps, self.min_samples = dialog.get_parameters()

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
            eps=self.eps,
            min_samples=self.min_samples
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
