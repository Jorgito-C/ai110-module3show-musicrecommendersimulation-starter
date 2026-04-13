# Reflection on Profile Comparisons

This reflection compares how different user profiles changed the top recommendations and why those changes make sense.

## Pair 1: High-Energy but Sad Pop vs No-Match Genre/Mood, Energy-Dominant

Both profiles asked for high energy, so both lists were full of energetic songs. The difference is that the first profile still gave some credit to `pop`, while the second profile used unknown labels (`opera`, `furious`) so the model mostly fell back to energy matching. In plain language: if the system cannot find your genre or mood, it still tries to satisfy your "activity level" request.

## Pair 2: Out-of-Range High Energy vs Out-of-Range Low Energy

When energy was very high, the list shifted toward intense tracks like "Storm Runner" and "Gym Hero." When energy was very low, the list shifted toward calmer tracks like lofi and ambient songs. This makes sense because the energy score is the strongest numeric driver in the formula, so it acts like a volume knob for intensity.

## Pair 3: High-Energy but Sad Pop vs Tempo/Valence Exploit Candidate

The first profile mostly rewarded songs that were energetic and pop-adjacent, while the tempo/valence profile promoted songs that matched extra numeric targets even without genre alignment. This shows that adding more numeric preferences can outweigh category preferences and change the top songs in ways a listener may not expect.

## Why "Gym Hero" Keeps Appearing for "Happy Pop"-Like Requests

"Gym Hero" keeps showing up because it has very high energy and also matches pop/intense-style signals that the current formula rewards heavily. Even when a user asks for a softer emotional tone, the strong energy score can push it near the top. In non-programmer terms: the model is currently better at matching "how intense should this feel" than matching subtle emotional mood.
