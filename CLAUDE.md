# CLAUDE.md — rules of the project

Project 2 of "Problem Solving" (Master 1 Visual Computing, USTHB): the Knight's Tour solved with a
genetic algorithm, plus a pygame interface. Same working method as the Sokoban project.

## Read before coding (in this order)

1. `specs/SPEC.md` — the statement (Project 2) and what Chapter 2 gives us. **Never contradict it.**
2. `docs/PLAN.md` — the checklist: where we are and what the next step is.
3. `docs/logs/` — the 2 or 3 most recent session logs.
4. `specs/ASSETS.md` — every asset, its author, source and licence.

## Rules

- **Follow the statement and Chapter 2.** Class names, attribute names and function names come from the
  statement (`Chromosome`, `Knight`, `Population`, `check_moves`, `tournament_selection`...). Do not add
  algorithms that are not in Chapter 2 (no Warnsdorff heuristic, no elitism, no other crossover) unless
  the team asks.
- **Simple student code.** Short functions, no clever tricks, comments in English that explain *why*.
  Everything must be explainable orally (`docs/EXPLICATION.md`).
- **One class per file**: `chromosome.py`, `knight.py`, `population.py`. The loop of the statement's
  `main` is `genetic_algorithm.py`. The interface lives in `gui/` and never contains algorithm logic.
- **Assets: trusted sources only.** The teacher wants every asset sourced. Never use chess.com files.
  Before adding any file to `specs/assets/`, add its row (author, URL, licence, date, SHA-256) to
  `specs/ASSETS.md`. Prefer open licences. When unsure of the licence, do not add the file.
- **No sound or image added "because it looks nice"** without the row in `specs/ASSETS.md`.
- **Tests:** `python test_core.py` must pass before ending a session (no pytest needed).
- **Logs:** at the end of every session create `docs/logs/YYYY-MM-DD_session-NN.md` (format of the
  existing logs) and tick the step in `docs/PLAN.md`.
- Language: code and docs in English (the statement is in English).

## Commands

```
pip install -r requirements.txt     # pygame-ce, once
python main.py                      # interface: home screen -> game
python main.py --console --seed 1   # algorithm only, in the terminal
python test_core.py                 # tests
```

## Map of the files

```
main.py               entry point (interface or --console)
board.py              constants (8x8, 63 genes, 8 moves) and helpers
chromosome.py         class Chromosome  (statement 1)
knight.py             class Knight      (statement 2)
population.py         class Population  (statement 3)
genetic_algorithm.py  the loop of the statement's main(), reusable
game.py               KnightGame: manual play with ONE knight (reuses Knight)
gui/                  pygame interface (theme, assets_loader, widgets, screens, GA thread)
test_core.py          tests of the core
specs/                SPEC.md, ASSETS.md, the two PDFs, assets/pieces/ (cburnett knights)
docs/                 PLAN.md, EXPLICATION.md, logs/
```
