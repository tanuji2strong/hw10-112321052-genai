# Round 4: manual override of the three-round stop rule

- Decision: the user chose option 1 (allow one more round) after round 3 ended with ai_review FAIL.
- Scope: fixes for the round-3 review only (slide 4 blocking; slides 6, 7, 8, 10, 11 minor, incl. stop_reason gloss).
- Gates run directly with ROUND=4 (run.py refuses rounds above 3 by design).
- Next: fresh ai_review on round 4. If it still fails, stop and report; no round 5 without a new decision.
