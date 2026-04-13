# 🎧 Model Card: Music Recommender Simulation

## Model Name

**VibeFinder 1.0**

---

## Goal / Task

This recommender suggests songs from a small catalog.  
It tries to match what a user wants by genre, mood, and energy.  
It ranks songs and returns the top 5 results.

---

## Data Used

The dataset has **18 songs** in `data/songs.csv`.  
Each song has genre, mood, energy, tempo, valence, danceability, and acousticness.  
I also added advanced fields: popularity, release decade, detailed mood tag, vocal intensity, lyrical density, and live energy.  
The dataset includes many styles, but it is still very small.  
Because the catalog is small, some songs appear often across different profiles.

---

## Algorithm Summary

The model gives points for matching genre and mood.  
It gives stronger points when a song's energy is close to the user's target energy.  
If the user includes extra preferences (tempo, valence, popularity, decade, mood tags, vocal style), it adds more points for those too.  
After base scoring, it applies diversity penalties to avoid repeating the same artist or genre too often in the top results.  
Then it returns the highest final scores.

---

## Observed Behavior / Biases

Energy has a very strong effect on ranking.  
High-energy requests often return the same intense songs, even when mood is different.  
This can create a filter bubble around energetic tracks.  
Out-of-range energy inputs still produce scores, which can lead to odd results.

---

## Evaluation Process

I tested multiple profiles, including conflicting and edge-case inputs.  
Examples: High-Energy Sad Pop, No-Match Genre/Mood, and out-of-range energy values.  
I ran a logic experiment by lowering genre weight and increasing energy weight.  
I compared top-5 outputs and checked whether changes felt meaningful or just different.  
I also added screenshots and profile comparisons in the project docs.

---

## Intended Use and Non-Intended Use

### Intended Use

This project is for classroom learning and experimentation.  
It is useful for understanding how recommendation scores work.  
It is designed for small, transparent demos.

### Non-Intended Use

It should not be used for real production music platforms.  
It should not be used to make high-stakes or personalized decisions.  
It does not learn from real user behavior, history, or context.

---

## Ideas for Improvement

1. Clamp user inputs (like energy) to safe ranges.  
2. Rebalance weights so mood is not overpowered by energy.  
3. Add diversity rules to reduce repeated artists or similar songs in the top results.

---

## Personal Reflection

My biggest learning moment was seeing how one weight change could shift almost every recommendation. I changed the energy weight and suddenly the system started pushing intense songs much more often, even when mood did not match. That helped me understand that recommender systems are very sensitive to design choices.

AI tools helped me move faster when testing profiles, generating edge cases, and documenting results clearly. But I had to double-check outputs by rerunning the code and reading score breakdowns, because AI suggestions can sound correct even when they miss context. I learned to treat AI as a strong assistant, not an automatic source of truth.

I was surprised that a simple point-based algorithm could still feel like a real recommender. Even without machine learning, it gave results that often looked believable. If I extended this project, I would add better input validation, a stronger diversity step, and adaptive weights that change based on user feedback over time.
