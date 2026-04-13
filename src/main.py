"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main
"""

import os
from src.recommender import load_songs, recommend_songs

# ---------------------------------------------------------------------------
# Three diverse user profiles for evaluation
# ---------------------------------------------------------------------------

PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "likes_acoustic": False,
    },
}


def print_recommendations(profile_name: str, recommendations: list) -> None:
    """Print a clean, labeled block of recommendations for one user profile."""
    print("=" * 60)
    print(f"  Profile: {profile_name}")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']} — {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Why   : {explanation}")
        print()


def main() -> None:
    # Resolve path relative to the project root, not the src/ folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "songs.csv")

    songs = load_songs(csv_path)
    print(f"Loaded songs: {len(songs)}\n")

    for profile_name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, recommendations)


if __name__ == "__main__":
    main()
