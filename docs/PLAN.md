# PLAN — Knight's Tour

One step per work session. Tick, date and link the log as we go. Never contradict `specs/SPEC.md`.

Part 1 — the algorithm (statement of Project 2):

- [x] Step 0 — Read Chapter 2 and Project 2, summary in `specs/SPEC.md` — 2026-11-20 — docs/logs/2026-11-20_session-01.md
- [x] Step 1 — `Chromosome` (63 genes, single-point crossover, mutation) — 2026-11-20 — docs/logs/2026-11-20_session-01.md
- [x] Step 2 — `Knight` (`move_forward`, `move_backward`, `check_moves` with random cycle direction, `evaluate_fitness`) — 2026-11-20 — docs/logs/2026-11-20_session-01.md
- [x] Step 3 — `Population` (tournament selection of size 3, `create_new_generation`) and the loop of `main` — 2026-11-20 — docs/logs/2026-11-20_session-01.md
- [x] Step 4 — Check: 20 runs, every path is a legal tour of 64 distinct squares — 2026-11-20 — docs/logs/2026-11-20_session-01.md

Part 2 — structure, interface, sources (asked by the team on 2026-11-20):

- [x] Step 5 — Project structure like Sokoban: `main.py`, one file per class, `docs/`, `specs/`, `CLAUDE.md` — 2026-11-20 — docs/logs/2026-11-20_session-02.md
- [x] Step 6 — Trusted assets: cburnett knights from the Lichess repository, licence and SHA-256 in `specs/ASSETS.md` — 2026-11-20 — docs/logs/2026-11-20_session-02.md
- [x] Step 7 — Interface: home screen with "Play" — 2026-11-20 — docs/logs/2026-11-20_session-02.md
- [x] Step 8 — Interface: manual play with ONE knight (`game.py`, legal-move dots, undo, new game) — 2026-11-20 — docs/logs/2026-11-20_session-02.md
- [x] Step 9 — Interface: button "Solve with Genetic Algorithm" (background thread, cancel, replay, speed) — 2026-11-20 — docs/logs/2026-11-20_session-02.md and docs/logs/2026-11-20_session-03.md
- [x] Step 10 — chess.com-like look without chess.com files (colours and shapes in the code) — 2026-11-20 — docs/logs/2026-11-20_session-02.md
- [x] Step 11 — Tests (`test_core.py`, 10 tests) — 2026-11-20 — docs/logs/2026-11-20_session-02.md
- [x] Step 12 — Documentation: README, CLAUDE, SPEC, ASSETS, EXPLICATION — 2026-11-20 — docs/logs/2026-11-20_session-02.md

- [x] Step 13 — Interface simplified: centered home screen "Knight's Tour Game", no on-screen explanation texts, calculation not drawn, no chart, no population / mutation controls (not in the statement), slower replay — 2026-11-20 — docs/logs/2026-11-20_session-03.md

- [x] Step 14 — Audit against `Project 2.pdf` and `Chapter 2.pdf`: `def main()` added to `main.py` as in the statement, 2 tests added for the order and the single draw of the `check_moves` cycle (12 tests) — 2026-11-21 — docs/logs/2026-11-21_session-04.md

To do / ideas (not asked yet, only if the team wants):

- [ ] Choose the starting square in manual mode (the statement fixes (0, 0) for the algorithm).
- [ ] Optional elitism (Chapter 2 mentions it) and a comparison table of parameters.
- [ ] Sounds (would need a trusted source added to `specs/ASSETS.md` first).
