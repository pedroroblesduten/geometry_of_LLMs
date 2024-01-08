from umap import UMAP
from scipy.spatial import ConvexHull
from typing import *
import numpy as np

def compute_geometric_metrics(
    self, 
    embeddings, 
    dimensionality_reduction_model=UMAP(n_components=9)
    ) -> Dict[str, Any]:

    if embeddings.ndim > 2:
        embeddings = embeddings.reshape(-1, embeddings.shape[-1]) 

    centroid = np.mean(embeddings, axis=0)
    distances = cdist(embeddings, [centroid], 'euclidean')

    reduced_embeddings = dimensionality_reduction_model.fit_transform(embeddings)
    
    # Compute the convex hull
    hull = ConvexHull(reduced_embeddings)

    volume = hull.volume
    area = hull.area

    return {"mean_distance": np.mean(distances), "volume": hull.volume, "area": hull.area}