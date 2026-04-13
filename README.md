# 🎵 Music Recommender Simulation

## Project Summary

This project builds a **content-based music recommender** that suggests songs from a 20-track catalog based on a user's stated taste preferences. Rather than watching what other listeners play (collaborative filtering), it reads each song's audio attributes directly—genre, mood, energy, acousticness—and scores how well they match the user's profile. The simulation is intentionally small and transparent so every recommendation can be traced back to a clear mathematical reason.

---

## How The System Works

### Real-World Recommenders

Streaming platforms like Spotify and YouTube combine two main strategies:

- **Collaborative filtering** groups users by shared listening behavior. If you and many others both loved Artist A and then discovered Artist B, the system infers that someone new to Artist A should also hear Artist B—even if the two songs sound completely different.
- **Content-based filtering** looks at the song itself: tempo, energy, danceability, mood. It matches those attributes to a user's stated or inferred preferences without needing data from other users.

Real systems blend both: collaborative filtering provides serendipity and social signal, while content-based filtering handles cold-start situations (new users or new songs with no listening history yet). Key data types involved include explicit signals (likes, skips, playlist adds, replays) and implicit signals (completion rate, time of day, shuffle vs. repeat).

### This Simulation

This simulation uses **content-based filtering only**, scoring every song in the catalog against a hand-crafted user profile.

**Data flow:**

```text
Input (User Preferences)
        ↓
   load_songs()  ←  data/songs.csv
        ↓
  score_song()   ← runs for EVERY song in the catalog
        ↓
recommend_songs() → sorts all scores, returns top-k
        ↓
Output (Ranked list with explanations)
```

### Algorithm Recipe (Scoring Rule)

For each song, `score_song()` adds up:

| Signal | Points | Why |
| --- | --- | --- |
| Genre matches user's favorite | +2.0 | Genre is the strongest structural filter |
| Mood matches user's target mood | +1.0 | Mood captures emotional intent |
| Energy similarity | up to +1.0 | `1.0 - abs(song_energy - user_energy)` rewards closeness, not just high/low |
| Acoustic bonus | +0.5 | Only fires when `likes_acoustic=True` AND `acousticness > 0.7` |

**Ranking Rule:** Once every song has a score, `sorted(..., reverse=True)` produces the final ranking. The top-k results are returned with both a numeric score and a plain-English explanation string.

### Song and UserProfile Features

Each **Song** stores: `id`, `title`, `artist`, `genre`, `mood`, `energy` (0–1), `tempo_bpm`, `valence` (0–1), `danceability` (0–1), `acousticness` (0–1).

Each **UserProfile** stores: `favorite_genre`, `favorite_mood`, `target_energy` (0–1), `likes_acoustic` (bool).

---

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Mac or Linux
.venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### Run the Recommender

```bash
python -m src.main
```

### Running Tests

```bash
pytest
```

---

## Experiments You Tried

### Three User Profiles

| Profile | genre | mood | energy |
| --- | --- | --- | --- |
| High-Energy Pop | pop | happy | 0.85 |
| Chill Lofi | lofi | chill | 0.38 |
| Deep Intense Rock | rock | intense | 0.92 |

**High-Energy Pop** — "Sunrise City" scored highest (3.97) because it matched genre + mood + energy. "Gym Hero" came second despite being `mood: intense` because it still matched genre and energy closely.

**Chill Lofi** — "Library Rain" and "Midnight Coding" both scored ~4.47 because they hit every signal including the acoustic bonus. "Focus Flow" came third: it missed the mood match (focused ≠ chill) but still scored genre + energy + acoustic.

**Deep Intense Rock** — "Storm Runner" won decisively (3.99) with a full genre + mood + energy hit. The remaining slots went to high-energy songs from other genres (pop, metal, EDM) purely on energy proximity — revealing that when genre diversity is limited in the catalog, energy becomes the tiebreaker.

### Weight Shift Experiment

Doubling energy weight to 2.0 and halving genre to 1.0 caused "Gym Hero" to overtake "Sunrise City" for the pop profile because Gym Hero's energy (0.93) is closer to the user's target (0.85) than Sunrise City's (0.82). This revealed that the default genre-heavy weighting is intentional: it keeps recommendations thematically coherent.

### Feature Removal Experiment

Commenting out the mood check eliminated the gap between "Sunrise City" and "Gym Hero" for the pop profile—they both matched on genre and energy. This shows that mood is the key differentiator between an "upbeat pop banger" and a "workout pop anthem."

---

## Limitations and Risks

- Works on a 20-song catalog only—real systems need millions of tracks to escape obvious filter bubbles.
- Does not read lyrics, language, or cultural context.
- Genre labels are rigid: "rock" and "metal" are unrelated strings even though they share sonic characteristics.
- Energy similarity alone can surface acoustically distant songs if genre/mood don't match; a jazz song at energy 0.38 will rank alongside a lofi song just because the numbers match.
- No listening history means the system cannot adapt to a user's changing taste over time.

---

## Reflection

See [model_card.md](model_card.md) for the full model card and personal reflection.

Building this project made it clear how much work a simple string comparison (genre matching) actually does. Two songs can have identical energy and mood values but feel completely different because they belong to different genres—and yet without that genre label, the algorithm would never know. Real-world systems solve this by learning dense embeddings from audio waveforms, so "rock" and "metal" end up geometrically close in a vector space even if the labels differ. The most surprising moment was discovering that the "Chill Lofi" profile produced the most decisive recommendations: because multiple songs hit the same high ceiling of genre + mood + acoustic match, the energy similarity score became a fine-grained tiebreaker—exactly the kind of nuance a real recommender needs.
