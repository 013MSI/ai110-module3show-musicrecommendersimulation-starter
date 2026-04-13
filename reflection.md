# Reflection

## Profile Comparisons

### High-Energy Pop vs. Chill Lofi

These two profiles produced the most visually different outputs. The pop profile surfaced bright, upbeat tracks with fast tempos and high energy; the lofi profile surfaced slow, acoustic, introspective songs. What was interesting was *how* the system arrived at those results. For pop, the top slot was decided by a triple match (genre + mood + energy). For lofi, two songs tied almost perfectly and the winner was determined by a difference of just 0.01 in energy. This shows that when a genre is well-represented in the catalog, the continuous energy score becomes a precise tiebreaker rather than a blunt instrument.

### Chill Lofi vs. Deep Intense Rock

Both profiles had a strong first-place result — a song that matched genre, mood, and energy cleanly. The difference showed up in positions 2-5. Lofi had enough qualifying songs to fill the list with genre matches. Rock had only one rock song in the catalog, so slots 2-5 went to high-energy songs from completely different genres (pop, metal, EDM, hip-hop). For a chill lofi listener, recommendations 2-5 felt plausible. For an intense rock listener, they would likely feel wrong. The output is valid from the algorithm's perspective but invalid from a listener's perspective — which is a real-world AI problem worth naming.

### High-Energy Pop vs. Deep Intense Rock

Both profiles ask for high energy, but pop targets happy moods and rock targets intense moods. Despite that difference, "Gym Hero" (pop, intense, energy 0.93) appeared in the top five for *both* profiles: it matched the rock profile on mood and energy, and matched the pop profile on genre and energy. This one song appearing in two very different lists highlights that mood and genre interact in non-obvious ways. "Intense pop" and "intense rock" share emotional DNA even when they belong to different genre buckets.

---

## What I Learned

The biggest learning moment was realizing that "recommendation" is just "scoring + sorting." The magic feeling of a good suggestion comes entirely from which features you measure and how much you weight each one. If you weight genre too heavily, you get a genre filter, not a recommender. If you weight energy too heavily, you get a BPM sorter. The balance between the two is what produces something that feels like musical taste.

AI tools helped me move quickly through boilerplate — CSV loading, dataclass definitions, sorting idioms — but every judgment call about feature weights came from thinking about what actually makes songs feel similar. No prompt could answer that; it required listening to the music mentally and asking "would I put these two songs in the same playlist?" That question is inherently human.

What surprised me most about simple algorithms is that they can feel surprisingly accurate for well-represented profiles and surprisingly broken for underrepresented ones. The lofi profile worked beautifully because the catalog happened to have several lofi songs with consistent attributes. The rock profile felt hollow because there was only one rock song. Real Spotify has 100 million tracks, which is essentially their solution to this problem: add more data until every taste has enough examples to rank meaningfully.

If I extended this project, I would add a feedback loop — let users thumbs-up or thumbs-down results after each session and shift the weights accordingly. That single change would move VibeFinder from a static lookup table to a system that actually learns, which is the threshold between a toy and a real AI application.
