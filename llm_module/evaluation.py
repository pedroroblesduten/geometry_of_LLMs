from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
from typing import Dict, Any
import numpy as np
import matplotlib.pyplot as plt

def compute_geometric_metrics(embeddings: np.ndarray) -> Dict[str, Any]:
    centroid = np.mean(embeddings, axis=0)
    distances = cdist(embeddings, [centroid], 'euclidean')
    
    hull = ConvexHull(embeddings)

    return {
        "mean_distance": np.mean(distances), 
        "volume": hull.volume, 
        "area": hull.area
    }



def get_convex_hull_comparison_plot(embeddings1, embeddings2) -> plt.Figure:
    hull1 = ConvexHull(embeddings1)
    hull2 = ConvexHull(embeddings2)

    fig, ax = plt.subplots()

    ax.scatter(
        embeddings1[:, 0], 
        embeddings2[:, 1], 
        alpha=0.7, color='blue', 
        label='Text 1: Original')
    
    ax.scatter(
        embeddings1[:, 0], 
        embeddings2[:, 1], 
        alpha=0.7, 
        color='green', 
        label='Text 2: Generated')

    for simplex in hull1.simplices:
        ax.plot(embeddings1[simplex, 0], embeddings1[simplex, 1], 'k-')
    
    for simplex in hull2.simplices:
        ax.plot(embeddings2[simplex, 0], embeddings2[simplex, 1], 'k-')

    ax.title('Convex Hull Comparison')
    ax.xlabel('Dimension 1')
    ax.ylabel('Dimension 2')

    return fig
    


