import torch
import numpy as np

def recommend_top_k_movies(user_id, model, nMovies, k):
    """
    Recommend top-k movies for a given user based on the model's predictions.
    
    ARGS:
        - user_id: The ID of the user for whom we want to generate recommendations.
        - model: The trained recommendation model.
        - nMovies: Total number of movies in the dataset.
        - k: Number of top recommendations to return.

    RETURNS:
        - A list of movie IDs representing the top-k recommended movies for the user.
    """
    # Generate all movie IDs (0 to nMovies-1)
    movie_ids = torch.arange(nMovies).long()
    
    # Create a tensor for the user ID, repeated for each movie
    user_ids = torch.full((nMovies,), user_id, dtype=torch.long)

    # Get predictions for all movies for the given user
    with torch.no_grad():  # No need to track gradients during inference
        predictions = model(user_ids, movie_ids).squeeze()  # Get model predictions for all movies
    
    # Apply the threshold to filter out low-rated movies
    mask = predictions > 3  # Boolean mask for movies above the threshold
    filtered_movie_ids = movie_ids[mask]  # Filtered movie IDs
    filtered_predictions = predictions[mask]  # Filtered predictions

    # If fewer than k movies meet the threshold, adjust k
    k = min(k, len(filtered_predictions))
    
    # Get the indices of the top-k predicted ratings (highest scores) from the filtered list
    _, top_k_indices = torch.topk(filtered_predictions, k, largest=True, sorted=True)
    
    # Convert indices to movie IDs
    top_k_movie_ids = filtered_movie_ids[top_k_indices].numpy()
    
    return top_k_movie_ids