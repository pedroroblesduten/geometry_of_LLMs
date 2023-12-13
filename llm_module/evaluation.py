import umap
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
from typing import Dict, Any
import numpy as np
import matplotlib.pyplot as plt

def compute_geometric_metrics(
        embeddings, dimensionality_reduction_model=umap.UMAP(n_components=9)) -> Dict[str, Any]:

    if embeddings.ndim > 2:
        embeddings = embeddings.reshape(-1, embeddings.shape[-1]) 

    centroid = np.mean(embeddings, axis=0)
    distances = cdist(embeddings, [centroid], 'euclidean')

    reduced_embeddings = dimensionality_reduction_model.fit_transform(embeddings)
    
    # Compute the convex hull
    hull = ConvexHull(reduced_embeddings)

    return {"mean_distance": np.mean(distances), "volume": hull.volume, "area": hull.area}



def get_convex_hull_comparison_plot(
        embeddings1, 
        embeddings2,  
        dimensionality_reduction_model=umap.UMAP(n_components=2)) -> plt.Figure:

    combined_embeddings = np.vstack((embeddings1, embeddings2))  
    reduced_embeddings_combined = dimensionality_reduction_model \
        .fit_transform(combined_embeddings)

    reduced_embeddings1 = reduced_embeddings_combined[:len(embeddings1)]
    reduced_embeddings2 = reduced_embeddings_combined[len(embeddings1):]

    hull1 = ConvexHull(reduced_embeddings1)
    hull2 = ConvexHull(reduced_embeddings2)

    fig, ax = plt.subplots()

    ax.scatter(
        reduced_embeddings1[:, 0], 
        reduced_embeddings1[:, 1], 
        alpha=0.7, color='blue', 
        label='Text 1: Original')
    
    ax.scatter(
        reduced_embeddings2[:, 0], 
        reduced_embeddings2[:, 1], 
        alpha=0.7, 
        color='green', 
        label='Text 2: Generated')

    for simplex in hull1.simplices:
        ax.plot(reduced_embeddings1[simplex, 0], reduced_embeddings1[simplex, 1], 'k-')
    
    for simplex in hull2.simplices:
        ax.plot(reduced_embeddings2[simplex, 0], reduced_embeddings2[simplex, 1], 'k-')

    ax.title('Convex Hull Comparison')
    ax.xlabel('Dimension 1')
    ax.ylabel('Dimension 2')

    return fig
    


