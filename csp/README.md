# Projet 3 — Knight's Tour as a CSP (objectif 1 : backtracking simple)

Énoncé : `Project 3.pdf` (Dr. Meriem SEBAI, USTHB, 2026/2027, non versionné). Ce dossier contient
l'**objectif 1** : le tour du cavalier résolu par un backtracking, fidèle au pseudo-code du PDF.
L'objectif 2 (backtracking + heuristiques CSP) n'est pas dans cette version, voir `TODO.md`.

## Lancer

```
python csp/main_backtracking.py     # affiche le tour 1..64 dans le terminal
python csp/test_csp.py              # 7 tests
python main.py                      # interface, voir plus bas
```

## La formulation (comme dans le PDF)

| PDF | Où dans le code |
|---|---|
| Variables X0…X63, Xk = position du cavalier au coup k | `Knight.assignment` (liste des positions) |
| X0 = (0,0) | `START` dans `knight_csp.py` |
| Domaine D(Xk) : cases non visitées accessibles depuis Xk-1 | `Knight.possibleMoves()` |
| Contrainte 1 : mouvement en L | `consistent` (via `legal_knight_moves`) |
| Contrainte 2 : All-Different | `consistent` (`move not in assignment`) |
| Contrainte 3 : bords de l'échiquier | `consistent` (0 ≤ ligne, colonne < 8) |
| `knight.addMove(move)` / `knight.removeMove()` | `Knight.addMove` / `Knight.removeMove` |
| `backtracking(knight)` | `backtracking.py`, recopié du PDF sans modification |

Une position est `(ligne, colonne)` comme dans l'énoncé ; `(0,0)` est la case en haut à gauche.

## Fichiers

```
knight_csp.py         classe Knight (+ compteur nodes = coups essayés, pour comparer plus tard)
backtracking.py       la fonction backtracking(knight) du PDF
main_backtracking.py  lanceur terminal
test_csp.py           7 tests (domaine, contraintes, add/remove, fin d'un tour, impasse)
TODO.md               ce qui est fait / à faire
```

L'interface (dossier `gui/`) utilise ces classes : `gui/csp_job.py` (calcul dans un thread),
`gui/csp_screen.py` (recherche pas à pas), `gui/replay_screen.py` (le chat rejoue le tour) et le
bouton « Solve with CSP (Backtracking) » de l'écran Play.

## Résultat

Un tour complet de 64 cases en environ 0,3 s : **34 812 coups essayés**, environ 34 750 retours en
arrière. Le résultat est toujours le même (l'algorithme n'a pas de hasard).

## Un point à expliquer : l'ordre des 8 mouvements

Le backtracking simple essaie les mouvements dans l'ordre de `KNIGHT_MOVES`, sans réfléchir. Cet
ordre décide de tout : sur une centaine d'ordres testés, presque aucun ne trouve de tour (plus d'un
million d'essais sans résultat). L'ordre gardé est le seul qui trouve un tour vite. L'algorithme
reste celui du PDF, seul l'ordre de la liste a été choisi. C'est précisément ce que les heuristiques
de l'objectif 2 doivent remplacer par un vrai critère.

## Ce que montre l'écran « CSP backtracking (step by step) »

- les variables assignées (X0…Xk), les points = le domaine de la prochaine variable ;
- une croix rouge quand le cavalier est dans une impasse, puis il revient en arrière ;
- les coups essayés, les retours en arrière, la profondeur maximale.

Il montre que le backtracking simple passe presque tout son temps entre 55 et 63 cases, à défaire
et refaire la fin du parcours.
