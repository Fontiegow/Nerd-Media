import random

# Tiny sample dataset
games = [
    "The Witcher 3", "Elden Ring", "Hades", "Stardew Valley",
    "Minecraft", "Hollow Knight", "Disco Elysium", "Doom Eternal"
]

def recommend_games(user_input: str, n=3):
    """
    Simple placeholder recommender.
    Later you’ll plug in embeddings, similarity, ML, etc.
    """
    random.shuffle(games)
    return games[:n]
