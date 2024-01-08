from scipy.spatial import ConvexHull
from typing import *
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

def get_geometric_metrics(embeddings):
    print("Getting Metrics:")
    print("\t Centroid", end="...")
    centroid = np.mean(embeddings, axis=0)
    print("OK")
    
    print("\t Centroid", end="...")
    distances = cdist(embeddings, [centroid], 'euclidean')
    print("OK")

    print("\t ConvexHull", end="...")
    hull = ConvexHull(embeddings)
    print("OK")

    return {
        "mean_distance": np.mean(distances), 
        "volume": hull.volume, 
        "area": hull.area
    }



def plot_convex_hull(embeddings, ax=None, savefig=True, path="./resultados"):
    
    if not ax:
        fig, ax0 = plt.subplots()
    else:
        ax0 = ax
    
    print("Creating Convex Hull", end="...")
    hull = ConvexHull(embeddings)
    print("")

    ax0.scatter(embeddings[:, 0], embeddings[:, 1], alpha=0.7)
    for simplex in hull.simplices:
        ax0.plot(embeddings[simplex, 0], embeddings[simplex, 1], 'k-')

    if savefig == True and fig:
        fig.savefig(path )

    if not ax:
        return fig, ax0
    else:
        return ax
    

def plot_convex_hull_comparison(self, file_path1, file_path2):
    text1 = self.read_text(file_path1)
    embeddings1 = self.model_llm.get_embeddings_from_input(text1)[0]

    text2 = self.read_text(file_path2)
    embeddings2 = self.model_llm.get_embeddings_from_input(text2)[0]

    # Combine embeddings for t-SNE
    combined_embeddings = np.vstack((embeddings1, embeddings2))

    # Apply t-SNE to the combined embeddings
    tsne = TSNE(n_components=2, random_state=0)
    reduced_embeddings_combined = tsne.fit_transform(combined_embeddings)

    # Split the embeddings back into their respective sets
    reduced_embeddings1 = reduced_embeddings_combined[:len(embeddings1)]
    reduced_embeddings2 = reduced_embeddings_combined[len(embeddings1):]
    # Compute the convex hulls and plot as before
    hull1 = ConvexHull(reduced_embeddings1)
    hull2 = ConvexHull(reduced_embeddings2)

    plt.scatter(reduced_embeddings1[:, 0], reduced_embeddings1[:, 1], alpha=0.7, color='blue', label='Text 1: Original')
    plt.scatter(reduced_embeddings2[:, 0], reduced_embeddings2[:, 1], alpha=0.7, color='green', label='Text 2: Generated')

    for simplex in hull1.simplices:
        plt.plot(reduced_embeddings1[simplex, 0], reduced_embeddings1[simplex, 1], 'k-')
    for simplex in hull2.simplices:
        plt.plot(reduced_embeddings2[simplex, 0], reduced_embeddings2[simplex, 1], 'k-')

    plt.title('t-SNE Convex Hull Comparison')
    plt.xlabel('t-SNE Dimension 1')
    plt.ylabel('t-SNE Dimension 2')
    plt.legend()
    plt.savefig('./results/tsne_compare.png')
    print('plot saved')