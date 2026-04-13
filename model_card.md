# Model Card: Music Recommender Simulation

## 1. Model Name

### VibeFinder 1.0

---

## 2. Intended Use

VibeFinder suggests up to 5 songs from a 20-track catalog based on a user's stated genre preference, target mood, energy level, and acoustic taste. It is designed for classroom exploration of content-based filtering concepts—not for production use or real users. It assumes the user can accurately describe their own taste in advance, which real listeners often cannot.

---

## 3. How the Model Works

When you run VibeFinder, you hand it a short description of what you are in the mood for: a favorite genre (like "pop"), a target mood (like "happy"), a desired energy level on a 0-to-1 scale, and whether you tend to like acoustic sounds.

The system then looks at every song in the catalog one at a time and gives it a score:

- If a song's genre matches yours, it gets 2 bonus points — the biggest reward, because genre is the clearest boundary between musical worlds.
- If the song's mood matches your target, it gets 1 bonus point.
- The system also calculates how close the song's energy level is to your target. A perfect match adds 1 full point; a song that is very far from your energy preference adds almost nothing.
- If you said you like acoustic music and the song has a high acousticness value, it earns an extra half point.

After every song has a score, they are sorted from highest to lowest and the top five are returned along with a plain-English explanation of why each one scored the way it did.

---

## 4. Data

The catalog contains 20 songs stored in `data/songs.csv`. Each song has 10 attributes: a numeric ID, title, artist name, genre label, mood label, energy (0–1), tempo in BPM, valence (0–1), danceability (0–1), and acousticness (0–1).

The original 10 starter songs skewed toward pop, lofi, and rock. Ten additional songs were added to broaden coverage: metal, country, EDM, R&B, folk, synthwave, gospel, hip-hop, classical, and ambient. Despite this expansion, pop-adjacent genres (pop, indie pop, synthwave) make up a disproportionate share of happy/energetic songs. Genres like classical and ambient have only one representative each, so users preferring those styles will see very thin genre-match results and rely heavily on energy and mood scores instead.

---

## 5. Strengths

- **Transparency:** Every recommendation comes with a written reason. Users can see exactly why a song was ranked where it was.
- **Lofi and chill profiles:** Because the catalog has several lofi songs with consistent mood/acoustic values, these profiles produce strong, clearly differentiated rankings.
- **Energy as a tiebreaker:** When multiple songs hit the same genre and mood ceiling, the continuous energy score provides a meaningful fine-grained tiebreaker rather than arbitrary ordering.
- **No cold-start problem:** Unlike collaborative systems, VibeFinder requires zero listening history. A brand-new user profile works just as well as an established one.

---

## 6. Limitations and Bias

**Genre string matching is brittle.** "Rock" and "metal" are treated as completely unrelated even though they share sonic characteristics. A user who likes rock will never see a metal song in their top results unless energy and mood align by coincidence.

**Pop over-representation in high-energy/happy slots.** About 30% of the catalog lands in pop or indie pop. A "happy + high energy" user will almost always see pop songs dominate their top results, even if other genres could satisfy their request equally well. This is a dataset bias, not a scoring flaw, but the two are indistinguishable from the user's perspective.

**Energy-only fallback for rare genres.** If the user's favorite genre has only one song in the catalog (e.g., classical, gospel), rankings 2-5 are decided entirely by energy proximity. This means a classical lover may receive EDM or ambient suggestions simply because those songs happened to have a similar energy value.

**No diversity enforcement.** The system does not try to vary the recommendations. If three lofi songs are the top three scorers, all three appear in the list, leaving no room for serendipity.

**Static profile.** The system cannot learn that the user skipped a song or replayed another. Every run produces the same output for the same input.

**Conflicting preferences are silently ignored.** When a user asks for something contradictory — high energy *and* a sad mood — no song satisfies both signals. The genre match (+2.0) dominates by default and the unsatisfied preference disappears from the output with no warning to the user. Tested with `genre: r&b, mood: sad, energy: 0.90`: the top result matched genre but scored only 0.68 on energy, and the mood signal never fired at all.

---

## 7. Evaluation

Three user profiles were tested:

**High-Energy Pop (genre: pop, mood: happy, energy: 0.85)**
"Sunrise City" ranked first with a score of 3.97 — a full genre + mood + energy match. "Gym Hero" came second at 2.92 despite being mood: intense, because genre and energy still aligned. The remaining three slots went to non-pop songs that matched mood or energy but not genre. Result felt accurate: a pop fan would likely enjoy all five songs even if tracks 3-5 are from adjacent genres.

**Chill Lofi (genre: lofi, mood: chill, energy: 0.38, likes_acoustic: True)**
"Library Rain" and "Midnight Coding" tied at ~4.47, separated only by a 0.01 energy difference. "Focus Flow" came third at 3.48 — it matched genre and acoustic but not mood (focused ≠ chill). Positions 4 and 5 were ambient and folk songs, both acoustic and low-energy. This felt realistic: a lofi listener would genuinely enjoy quiet folk and ambient tracks.

**Deep Intense Rock (genre: rock, mood: intense, energy: 0.92)**
"Storm Runner" won decisively at 3.99. The next four were high-energy songs from pop, metal, EDM, and hip-hop — none matched genre. This exposed the catalog's rock scarcity: there is only one rock song. The result felt partially correct (the top pick was right) but the tail of the list relied purely on energy, producing an eclectic mix that a true rock fan would likely reject.

**Experiment — weight shift:** Doubling energy weight and halving genre weight caused "Gym Hero" to overtake "Sunrise City" for the pop profile, confirming that the default genre-heavy weighting is what keeps recommendations thematically coherent.

**Experiment — feature removal:** Removing the mood check collapsed the score gap between "Sunrise City" and "Gym Hero" for the pop profile, demonstrating that mood is the feature that distinguishes vibe within a genre.

---

## 8. Future Work

1. **Embed genres as vectors.** Replace exact string matching with a small similarity matrix so "rock" and "metal" are recognized as close neighbors, reducing the penalty for genre diversity in the catalog.
2. **Diversity enforcement.** After scoring, apply a re-ranking step (Maximal Marginal Relevance) that penalizes the second occurrence of the same genre to give users a more varied list.
3. **Implicit feedback loop.** Let users mark songs as liked or skipped during a session and update their profile weights dynamically, moving VibeFinder closer to a hybrid collaborative + content-based system.
4. **Valence and danceability scoring.** Both features are in the CSV but unused. Adding them would let the system distinguish "happy but calm" from "happy and danceable," improving precision for nuanced profiles.

---

## 9. Personal Reflection

Building VibeFinder made visible something that is invisible in real apps: every recommendation is just arithmetic. A song gets points, points get summed, lists get sorted. What feels like "Spotify knows me" is actually a very large version of the same loop running on billions of rows instead of twenty.

The most unexpected discovery was how decisive the acoustic bonus turned out to be. A half-point sounds small, but when four lofi songs all share the same genre and mood ceiling, that single flag (likes_acoustic) is what separates them from each other. That felt like a lesson about feature engineering: the value of a feature is not its size but how much unique information it carries relative to everything else.

Using AI tools during this project was helpful for generating boilerplate and explaining Python idioms like `sorted()` vs `.sort()`, but every algorithmic decision — what to weight, what to skip, how to structure the output — required human judgment. The AI could tell me how to implement an idea; it could not tell me whether the idea was right. That boundary felt important to locate.

If I extended this project, I would try adding a small user study: show five people their recommendations and ask whether the results matched their expectation. A system that feels wrong to real listeners is broken regardless of what the scores say.
