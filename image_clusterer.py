import os
import warnings
import numpy as np
from PIL import Image
from keras.applications.vgg16 import VGG16, preprocess_input  # type: ignore
from keras.preprocessing import image  # type: ignore
from keras.models import Model  # type: ignore
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count

Image.MAX_IMAGE_PIXELS = None
warnings.simplefilter('ignore')

class ImageClusterer:
    def __init__(self, n_clusters=3, resample_size=128, algorithm='kmeans', signals=None, eps=0.5, min_samples=5, affinity='euclidean', linkage='ward'):
        self.n_clusters = n_clusters
        self.resample_size = resample_size
        self.algorithm = algorithm
        self.model = VGG16(weights='imagenet', include_top=False)
        self.model = Model(inputs=self.model.inputs, outputs=self.model.layers[-1].output)
        self.signals = signals
        self.eps = eps
        self.min_samples = min_samples
        self.affinity = affinity
        self.linkage = linkage

    def extract_features(self, img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        features = self.model.predict(img_data)
        return features.flatten()

    def read_image(self, im):
        try:
            features = self.extract_features(im)
            return features
        except Exception as e:
            if self.signals:
                self.signals.message.emit("error", f"Error reading image '{os.path.basename(im)}': {e}")
            return None

    def cluster_images(self, image_paths):
        pool = ThreadPool(cpu_count())
        features = pool.map(self.read_image, image_paths)
        pool.close()
        pool.join()
        features = [f for f in features if f is not None]

        if len(features) == 0:
            raise ValueError("No valid features extracted from images.")

        pca = PCA(n_components=50)
        pca_features = pca.fit_transform(features)

        tsne = TSNE(n_components=2)
        tsne_features = tsne.fit_transform(pca_features)

        if self.algorithm == 'kmeans':
            clusterer = KMeans(n_clusters=self.n_clusters)
        elif self.algorithm == 'dbscan':
            clusterer = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        elif self.algorithm == 'agglomerative':
            clusterer = AgglomerativeClustering(n_clusters=self.n_clusters, metric=self.affinity, linkage=self.linkage)
        else:
            raise ValueError("Unsupported clustering algorithm")

        clusters = clusterer.fit_predict(tsne_features)
        return clusters