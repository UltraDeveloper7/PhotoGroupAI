import os
import shutil
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from image_clusterer import ImageClusterer  

class WorkerSignals(QObject):
    progress = Signal(int)
    finished = Signal(bool)
    message = Signal(str, str)  # Signal type and message

class Worker(QThread):
    def __init__(self, image_paths, folder, kmeans_value, resample_value, algorithm, move_files, eps, min_samples, affinity, linkage):
        super().__init__()
        self.signals = WorkerSignals()
        self.image_paths = image_paths
        self.folder = folder
        self.kmeans_value = kmeans_value
        self.resample_value = resample_value
        self.algorithm = algorithm
        self.move_files = move_files
        self.eps = eps
        self.min_samples = min_samples
        self.affinity = affinity
        self.linkage = linkage

    def run(self):
        try:
            nimages = len(self.image_paths)
            clusterer = ImageClusterer(
                n_clusters=self.kmeans_value,
                resample_size=self.resample_value,
                algorithm=self.algorithm,
                signals=self.signals,
                eps=self.eps,
                min_samples=self.min_samples,
                affinity=self.affinity,
                linkage=self.linkage
            )
            clusters = clusterer.cluster_images(self.image_paths)
            valid_clusters = set(clusters) - {-1}  # Exclude noise points

            for i in range(len(valid_clusters)):
                try:
                    os.makedirs(self.folder + str(i + 1).zfill(len(str(len(valid_clusters)))))
                except Exception as e:
                    self.signals.message.emit("warning", f"Folder already exists: {e}")

            action = shutil.copy
            if self.move_files:
                action = shutil.move

            for i, cluster in enumerate(clusters):
                if cluster != -1:  # Skip noise points in DBSCAN
                    action(self.image_paths[i], self.folder + "/" + str(cluster + 1).zfill(len(str(len(valid_clusters)))) + "/")
                progress_value = int((i + 1) * 100 / nimages)
                self.signals.progress.emit(progress_value)
                QThread.msleep(10)  # Small delay to ensure the GUI can update
            
            self.signals.finished.emit(True)
        except Exception as e:
            self.signals.message.emit("error", f"Error during processing: {e}")
            self.signals.finished.emit(False)