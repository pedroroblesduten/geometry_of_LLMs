import numpy as np
from scipy.spatial.distance import cdist
from scipy.spatial import ConvexHull
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from model_llm import ModelLLM

class LLMGeometricMetrics:
    def __init__(self, model_name):
        self.model_llm = ModelLLM(model_name, '/results')
        self.input_text = ""

    def read_text(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.input_text = file.read()
        except IOError:
            print(f"Error: File {file_path} not accessible or does not exist.")
            self.input_text = ""

    def get_mean_distance_from_centroid(self):
        embeddings = self.model_llm.generate_embeddings(self.input_text)

        if embeddings.ndim > 2:
            embeddings = embeddings.reshape(-1, embeddings.shape[-1])

        centroid = np.mean(embeddings, axis=0)
        distances = cdist(embeddings, [centroid], 'euclidean')
        mean_distance = np.mean(distances)
        return mean_distance

    def get_convex_hull_metrics(self):
        embeddings = self.model_llm.generate_embeddings(self.input_text)

        if embeddings.ndim > 2:
            embeddings = embeddings.reshape(-1, embeddings.shape[-1])

        n_components = min(embeddings.shape[0], 9)
        pca = PCA(n_components=n_components, random_state=0)
        reduced_embeddings = pca.fit_transform(embeddings)

        hull = ConvexHull(reduced_embeddings)
        volume = hull.volume
        area = hull.area

        return volume, area

    def plot_convex_hull(self):
        embeddings = self.model_llm.generate_embeddings(self.input_text)

        if embeddings.ndim > 2:
            embeddings = embeddings.reshape(-1, embeddings.shape[-1])

        perplexity = min(30, len(embeddings) - 1)
        tsne = TSNE(n_components=2, random_state=0, perplexity=perplexity)
        reduced_embeddings = tsne.fit_transform(embeddings)

        hull = ConvexHull(reduced_embeddings)

        plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], alpha=0.7)
        for simplex in hull.simplices:
            plt.plot(reduced_embeddings[simplex, 0], reduced_embeddings[simplex, 1], 'k-')

        plt.title('Convex Hull of t-SNE Reduced Embeddings')
        plt.xlabel('t-SNE Dimension 1')
        plt.ylabel('t-SNE Dimension 2')
        plt.savefig('./results/tsne_plot.png')

# Example usage
geometric_metrics = LLMGeometricMetrics('meta-llama/Llama-2-7b-chat-hf')
file_path = "example.txt"
geometric_metrics.read_text(file_path)
mean_distance = geometric_metrics.get_mean_distance_from_centroid()
print("Mean Distance from Centroid:", mean_distance)
volume, area = geometric_metrics.get_convex_hull_metrics()
print("Convex Hull Volume:", volume)
print("Convex Hull Area:", area)
geometric_metrics.plot_convex_hull()

