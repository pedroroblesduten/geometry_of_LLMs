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



def plot_convex_hull(
        embeddings, 
        ax=None, 
        savefig=True, 
        path="./resultados", 
        color="blue"):
    
    if not ax:
        fig, ax0 = plt.subplots()
    else:
        ax0 = ax
    
    print("Creating Convex Hull", end="...")
    hull = ConvexHull(embeddings)
    print("")

    ax0.scatter(embeddings[:, 0], embeddings[:, 1], alpha=0.7, color=color)
    for simplex in hull.simplices:
        ax0.plot(embeddings[simplex, 0], embeddings[simplex, 1], 'k-')

    if savefig == True and fig:
        fig.savefig(path)

    if not ax:
        return fig, ax0
    else:
        return ax
