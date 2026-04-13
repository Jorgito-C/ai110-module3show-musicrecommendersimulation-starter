import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV and cast numeric fields for scoring."""
    songs: List[Dict] = []

    with open(csv_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "popularity": float(row["popularity"]),
                "release_decade": int(row["release_decade"]),
                "mood_tag": row["mood_tag"],
                "vocal_intensity": float(row["vocal_intensity"]),
                "lyrical_density": float(row["lyrical_density"]),
                "live_energy": float(row["live_energy"]),
            }
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return reasons."""
    score = 0.0
    reasons: List[str] = []

    # Genre match (experiment: reduce genre influence)
    if song["genre"] == user_prefs["genre"]:
        score += 1.0
        reasons.append("genre match (+1.0)")

    # Mood match
    if song["mood"] == user_prefs["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity (experiment: increase energy influence)
    energy_similarity = max(0.0, 1 - abs(song["energy"] - user_prefs["energy"]))
    energy_points = energy_similarity * 6.0
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    # Optional tempo preference
    if "tempo" in user_prefs:
        tempo_similarity = 1 - min(abs(song["tempo_bpm"] - user_prefs["tempo"]) / 100, 1)
        tempo_points = tempo_similarity * 1.5
        score += tempo_points
        reasons.append(f"tempo similarity (+{tempo_points:.2f})")

    # Optional valence preference
    if "valence" in user_prefs:
        valence_similarity = max(0.0, 1 - abs(song["valence"] - user_prefs["valence"]))
        valence_points = valence_similarity * 1.0
        score += valence_points
        reasons.append(f"valence similarity (+{valence_points:.2f})")

    # Advanced optional preference: popularity target (0-100)
    if "popularity_target" in user_prefs:
        popularity_similarity = max(
            0.0, 1 - abs(song["popularity"] - user_prefs["popularity_target"]) / 100
        )
        popularity_points = popularity_similarity * 1.2
        score += popularity_points
        reasons.append(f"popularity similarity (+{popularity_points:.2f})")

    # Advanced optional preference: target release decade
    if "release_decade" in user_prefs:
        decade_gap = abs(song["release_decade"] - user_prefs["release_decade"]) // 10
        decade_similarity = max(0.0, 1 - (decade_gap / 4))
        decade_points = decade_similarity * 1.0
        score += decade_points
        reasons.append(f"release decade similarity (+{decade_points:.2f})")

    # Advanced optional preference: detailed mood tags
    if "preferred_mood_tags" in user_prefs:
        preferred_tags = user_prefs["preferred_mood_tags"]
        if song["mood_tag"] in preferred_tags:
            score += 1.5
            reasons.append("detailed mood tag match (+1.50)")

    # Advanced optional preference: vocal intensity
    if "vocal_intensity" in user_prefs:
        vocal_similarity = max(0.0, 1 - abs(song["vocal_intensity"] - user_prefs["vocal_intensity"]))
        vocal_points = vocal_similarity * 0.8
        score += vocal_points
        reasons.append(f"vocal intensity similarity (+{vocal_points:.2f})")

    # Advanced optional preference: lyrical density
    if "lyrical_density" in user_prefs:
        lyrical_similarity = max(0.0, 1 - abs(song["lyrical_density"] - user_prefs["lyrical_density"]))
        lyrical_points = lyrical_similarity * 0.7
        score += lyrical_points
        reasons.append(f"lyrical density similarity (+{lyrical_points:.2f})")

    # Advanced optional preference: live performance energy
    if "live_energy" in user_prefs:
        live_similarity = max(0.0, 1 - abs(song["live_energy"] - user_prefs["live_energy"]))
        live_points = live_similarity * 0.8
        score += live_points
        reasons.append(f"live energy similarity (+{live_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score, then apply diversity penalties in top-k selection."""
    scored_songs: List[Tuple[Dict, float, List[str]]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))

    selected: List[Tuple[Dict, float, str]] = []
    artist_counts: Dict[str, int] = {}
    genre_counts: Dict[str, int] = {}
    remaining = scored_songs.copy()

    while remaining and len(selected) < k:
        best_idx = 0
        best_adjusted_score = float("-inf")

        for idx, (song, base_score, _) in enumerate(remaining):
            artist_penalty = artist_counts.get(song["artist"], 0) * 1.0
            genre_penalty = genre_counts.get(song["genre"], 0) * 0.6
            adjusted_score = base_score - artist_penalty - genre_penalty
            if adjusted_score > best_adjusted_score:
                best_adjusted_score = adjusted_score
                best_idx = idx

        song, base_score, reasons = remaining.pop(best_idx)
        artist_repeat_count = artist_counts.get(song["artist"], 0)
        genre_repeat_count = genre_counts.get(song["genre"], 0)

        diversity_notes: List[str] = []
        if artist_repeat_count > 0:
            diversity_notes.append(f"diversity penalty artist (-{artist_repeat_count * 1.0:.2f})")
        if genre_repeat_count > 0:
            diversity_notes.append(f"diversity penalty genre (-{genre_repeat_count * 0.6:.2f})")

        final_reasons = reasons + diversity_notes
        selected.append((song, best_adjusted_score, ", ".join(final_reasons)))

        artist_counts[song["artist"]] = artist_repeat_count + 1
        genre_counts[song["genre"]] = genre_repeat_count + 1

    return selected