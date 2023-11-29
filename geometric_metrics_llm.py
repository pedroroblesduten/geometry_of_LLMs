import numpy as np
from scipy.spatial.distance import cdist
from model_llm import ModelLLM

class LLMGeometricMetrics:
    def __init__(self, model_name):
        self.model_llm = ModelLLM(model_name, './results')

    def get_mean_distance_from_centroid(self, text):
        # Generate embeddings using ModelLLM
        embeddings = self.model_llm.generate_embeddings(text)

        print(embeddings.shape)

        # Calculate centroid of the embeddings
        centroid = np.mean(embeddings, axis=1)
        print(centroid)

        # Calculate distances from each embedding to the centroid
        distances = cdist(embeddings, centroid[0], 'euclidean')

        # Compute mean distance
        mean_distance = np.mean(distances)
        return mean_distance

# Example usage
geometric_metrics = LLMGeometricMetrics('meta-llama/Llama-2-7b-chat-hf')
text = "Your sample text here"
mean_distance = geometric_metrics.get_mean_distance_from_centroid(text)
print("Mean Distance from Centroid:", mean_distance)

