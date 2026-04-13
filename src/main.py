from .recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n=== {profile_name} ===")
    print(f"User profile: {user_prefs}")
    print("=" * 72)

    for i, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = [reason.strip() for reason in explanation.split(",") if reason.strip()]
        print(f"{i:>2}. {song['title']} - {song['artist']}")
        print(f"    Final score : {score:.2f}")
        print(f"    Tags        : genre={song['genre']} | mood={song['mood']}")
        print("    Reasons     :")
        for reason in reasons:
            print(f"      - {reason}")
        print("-" * 72)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = [
        (
            "High-Energy but Sad Pop (conflicting)",
            {
                "genre": "pop",
                "mood": "sad",
                "energy": 0.9,
            },
        ),
        (
            "No-Match Genre/Mood, Energy-Dominant",
            {
                "genre": "opera",
                "mood": "furious",
                "energy": 0.78,
            },
        ),
        (
            "Out-of-Range High Energy",
            {
                "genre": "rock",
                "mood": "intense",
                "energy": 1.3,
            },
        ),
        (
            "Out-of-Range Low Energy",
            {
                "genre": "lofi",
                "mood": "chill",
                "energy": -0.2,
            },
        ),
        (
            "Tempo/Valence Exploit Candidate",
            {
                "genre": "ambient",
                "mood": "intense",
                "energy": 0.9,
                "tempo": 220,
                "valence": 0.05,
            },
        ),
        (
            "Modern Euphoric Pop (advanced features)",
            {
                "genre": "pop",
                "mood": "happy",
                "energy": 0.82,
                "popularity_target": 90,
                "release_decade": 2020,
                "preferred_mood_tags": ["euphoric", "sunny"],
                "vocal_intensity": 0.8,
                "lyrical_density": 0.55,
                "live_energy": 0.65,
            },
        ),
    ]

    for profile_name, user_prefs in profiles:
        print_recommendations(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()