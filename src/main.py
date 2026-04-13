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

    high_energy_pop = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
    }

    chill_lofi = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
    }

    deep_intense_rock = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.95,
    }

    conflicting_profile = {
        "genre": "ambient",
        "mood": "intense",
        "energy": 0.9,
    }

    print_recommendations("High-Energy Pop", high_energy_pop, songs)
    print_recommendations("Chill Lofi", chill_lofi, songs)
    print_recommendations("Deep Intense Rock", deep_intense_rock, songs)
    print_recommendations("Conflicting Profile", conflicting_profile, songs)


if __name__ == "__main__":
    main()