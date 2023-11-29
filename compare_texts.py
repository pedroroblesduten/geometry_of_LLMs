import numpy as np
from scipy.spatial.distance import cdist
from scipy.spatial import ConvexHull
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from tabulate import tabulate
from model_llm import ModelLLM
from scipy.spatial import ConvexHull
from sklearn.decomposition import FastICA
from sklearn.decomposition import PCA

class CompareText:
    def __init__(self, model_llm):
        self.model_llm = model_llm

    def read_text(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except IOError:
            print(f"Error: File {file_path} not accessible or does not exist.")
            return ""

    def plot_convex_hull_comparison(self, file_path1, file_path2):
        text1 = self.read_text(file_path1)
        embeddings1 = self.model_llm.get_embeddings_from_input(text1)[0]

        text2 = self.read_text(file_path2)
        embeddings2 = self.model_llm.get_embeddings_from_input(text2)[0]

        # Determine suitable perplexity values
        perplexity1 = min(30, len(embeddings1) - 1)
        perplexity2 = min(30, len(embeddings2) - 1)

        tsne = TSNE(n_components=2, random_state=0)

        # Apply t-SNE with adjusted perplexity for each set of embeddings
        reduced_embeddings1 = tsne.set_params(perplexity=perplexity1).fit_transform(embeddings1)
        reduced_embeddings2 = tsne.set_params(perplexity=perplexity2).fit_transform(embeddings2)

        # Compute the convex hulls
        hull1 = ConvexHull(reduced_embeddings1)
        hull2 = ConvexHull(reduced_embeddings2)

        # Plot the embeddings and convex hulls
        plt.scatter(reduced_embeddings1[:, 0], reduced_embeddings1[:, 1], alpha=0.7, color='blue', label='Text 1: Original')
        plt.scatter(reduced_embeddings2[:, 0], reduced_embeddings2[:, 1], alpha=0.7, color='green', label='Text 2: Generated')

        for simplex in hull1.simplices:
            plt.plot(reduced_embeddings1[simplex, 0], reduced_embeddings1[simplex, 1], 'k-')

        for simplex in hull2.simplices:
            plt.plot(reduced_embeddings2[simplex, 0], reduced_embeddings2[simplex, 1], 'k-')

        # Additional plot settings
        plt.title('t-SNE Convex Hull Comparison')
        plt.xlabel('t-SNE Dimension 1')
        plt.ylabel('t-SNE Dimension 2')
        plt.legend()
        plt.savefig('./results/tsne_compare.png')
        print('plot salvo')

    def compare_geometric_metrics(self, file_path1, file_path2):
        text1 = self.read_text(file_path1)
        embeddings1 = self.model_llm.get_embeddings_from_input(text1)

        text2 = self.read_text(file_path2)
        embeddings2 = self.model_llm.get_embeddings_from_input(text2)

        metrics1 = self.compute_geometric_metrics(embeddings1)
        metrics2 = self.compute_geometric_metrics(embeddings2)

        headers = ["Metric", "Text 1", "Text 2"]
        table = [
            ["Mean Distance from Centroid", metrics1["mean_distance"], metrics2["mean_distance"]],
            ["Convex Hull Volume", metrics1["volume"], metrics2["volume"]],
            ["Convex Hull Area", metrics1["area"], metrics2["area"]]
        ]

        print(tabulate(table, headers, tablefmt="grid"))

    def compute_geometric_metrics(self, embeddings):
        if embeddings.ndim > 2:
            embeddings = embeddings.reshape(-1, embeddings.shape[-1])

        centroid = np.mean(embeddings, axis=0)
        distances = cdist(embeddings, [centroid], 'euclidean')
        mean_distance = np.mean(distances)

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

        return {"mean_distance": mean_distance, "volume": volume, "area": area}

# Example usage
model_llm = ModelLLM("meta-llama/Llama-2-7b-chat-hf", "./results/")
compare_text = CompareText(model_llm)
file_path1 = "example.txt"
file_path2 = "output.txt"

compare_text.compare_geometric_metrics(file_path1, file_path2)
compare_text.plot_convex_hull_comparison(file_path1, file_path2)

