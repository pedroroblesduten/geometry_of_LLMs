import numpy as np
from scipy.spatial.distance import cdist
from model_llm import ModelLLM
from scipy.spatial import ConvexHull
from sklearn.decomposition import FastICA
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

class LLMGeometricMetrics:
    def __init__(self, model_name):
        self.model_llm = ModelLLM(model_name, '/results')

    def get_mean_distance_from_centroid(self, text):
        # Generate embeddings using ModelLLM
        embeddings = self.model_llm.generate_embeddings(text)

        # Reshape embeddings to 2D (if needed)
        if embeddings.ndim > 2:
            embeddings = embeddings.reshape(-1, embeddings.shape[-1])

        # Calculate centroid of the embeddings (along the second axis)
        centroid = np.mean(embeddings, axis=0)

        # Calculate distances from each embedding to the centroid
        distances = cdist(embeddings, [centroid], 'euclidean')

        # Compute mean distance
        mean_distance = np.mean(distances)
        return mean_distance

    def get_convex_hull_metrics(self, text):
        # Generate embeddings using ModelLLM
        embeddings = self.model_llm.generate_embeddings(text)

        # Reshape embeddings to 2D (if needed)
        if embeddings.ndim > 2:
            embeddings = embeddings.reshape(-1, embeddings.shape[-1])

        # Determine the number of PCA components based on the number of samples
        n_components = min(embeddings.shape[0], 9)

        # Dimensionality reduction using PCA
        pca = PCA(n_components=n_components, random_state=0)
        reduced_embeddings = pca.fit_transform(embeddings)

        # Compute the convex hull
        hull = ConvexHull(reduced_embeddings)

        # Calculate volume and area of the convex hull
        volume = hull.volume
        area = hull.area

        return volume, area

    def plot_convex_hull(self, text):
        # Generate embeddings using ModelLLM
        embeddings = self.model_llm.generate_embeddings(text)

        # Reshape embeddings to 2D (if needed)
        if embeddings.ndim > 2:
            embeddings = embeddings.reshape(-1, embeddings.shape[-1])

        # Determine a suitable perplexity value (less than the number of samples)
        perplexity = min(30, len(embeddings) - 1)

        # Apply t-SNE for dimensionality reduction to 2D
        tsne = TSNE(n_components=2, random_state=0, perplexity=perplexity)
        reduced_embeddings = tsne.fit_transform(embeddings)

        # Compute the convex hull
        hull = ConvexHull(reduced_embeddings)

        # Plot the embeddings
        plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], alpha=0.7)

        # Plot the convex hull
        for simplex in hull.simplices:
            plt.plot(reduced_embeddings[simplex, 0], reduced_embeddings[simplex, 1], 'k-')

        # Additional plot settings
        plt.title('Convex Hull of t-SNE Reduced Embeddings')
        plt.xlabel('t-SNE Dimension 1')
        plt.ylabel('t-SNE Dimension 2')
        plt.savefig('./results/tsne_plot.png')

# Example usage
geometric_metrics = LLMGeometricMetrics('meta-llama/Llama-2-7b-chat-hf')
text = "Complete o texto a seguir: tenho por dom a paixao, nas queimadas de tronco seco"
geometric_metrics.plot_convex_hull(text)
