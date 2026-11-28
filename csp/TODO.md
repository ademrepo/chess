# Projet 3 — Knight's Tour as a CSP (Dr. Meriem SEBAI, USTHB)

Source : `Project 3.pdf` (3 pages, non versionné). Branche : `camelia`.
Légende : `[x]` fait · `[ ]` à faire

## 0. Mise en place
- [x] Branche `camelia`, dossier `csp/`
- [x] `Project 3.pdf` ajouté au `.gitignore`
- [x] `csp/README.md` (lancer, formulation, fichiers, résultat)

## 1. Objectif 1 — Backtracking simple (fidèle au PDF) — FAIT
- [x] Variables X0…X63, X0 = (0,0), domaines, les 3 contraintes (`knight_csp.py`)
- [x] Classe `Knight` : `assignment`, `possibleMoves()`, `consistent(move)`, `addMove(move)`, `removeMove()`
- [x] `backtracking(knight)` recopié du PDF (`backtracking.py`), arrêt à `len(assignment) == 64`
- [x] Tests (`test_csp.py`, 7 tests) et lanceur terminal (`main_backtracking.py`)
- [x] Ordre des 8 mouvements choisi : les autres ordres testés ne finissent pas (à expliquer, voir `README.md`)
- [x] Compteur de coups essayés (`Knight.nodes`), affiché dans l'interface
- [x] Visualisation façon Figure 2 : échiquier, cavalier, cases numérotées, impasses et retours en arrière

## 2. Objectif 2 — Backtracking + heuristiques CSP — À FAIRE (pas dans cette version)
Le PDF ne précise pas lesquelles. Idée : garder le même `backtracking()` du PDF et mettre les
heuristiques dans le `Knight` (`possibleMoves` ordonne, `consistent` détecte les impasses).
- [ ] MRV (moins de coups restants d'abord, règle de Warnsdorff)
- [ ] Degree heuristic (départage des égalités MRV)
- [ ] Forward checking (case non visitée sans voisin libre = coup refusé)
- [ ] (option) LCV, AC-3
- [ ] `csp/heuristics.py`, tests, `csp/benchmark.py` (coups essayés et temps : simple vs heuristiques)
- [ ] Choix « simple / avec heuristiques » dans l'interface (colonne « Project 3 » du menu)

## 3. Interface — fait
Le projet avait déjà un échiquier et deux écrans (jeu + chat) : réutilisés, avec deux styles.
- [x] Écran de départ : **Chess Classic** (vert, cavalier) ou **Cavalier Jack** (bois, chat), touches 1 / 2
- [x] Mêmes fonctions dans les deux styles : jeu, résolution génétique, résolution CSP, labo, CSP pas à pas, réglages
- [x] Menu : « Play » puis Settings / Change style / Quit, puis deux colonnes « Project 2 » (algorithme génétique) et « Project 3 » (CSP)
- [x] Écran « Play » : boutons « Solve with Genetic Algorithm » et « Solve with CSP (Backtracking) » ; celui qui tourne reste allumé avec une bordure, l'autre est grisé
- [x] Écran « CSP backtracking (step by step) » : lecture, pas en avant / en arrière, vitesse, saut à la fin, stats
- [x] Écrans « Watch (cat) » : le chat rejoue le tour (cartes : cases visitées, ce que l'algorithme a fait, runs)
- [x] Cavalier Jack : kit en bois dessiné en Python (`gui/wood.py`), chat dans `gui/cat.py` (sprites de `assets/cat_sprite.png`)
- [x] Chat : de profil quand il avance, de face à l'arrêt, de dos quand il recule (CSP pas à pas), promenade dans le menu
- [x] Calcul dans un thread (`gui/csp_job.py`), la fenêtre ne gèle pas, bouton Cancel

## 4. Tests à la main (à faire par toi, `python main.py`)
- [ ] Menu : tous les boutons ouvrent le bon écran, dans les deux styles
- [ ] « CSP backtracking (step by step) » : Play, Pause, Step, Step back, vitesses, Jump to end, Restart, Esc
- [ ] « Watch the backtracking (cat) » et « Watch the algorithm (cat) » : replay, vitesse, New run, Menu
- [ ] « Play » : jouer à la main, Solve génétique, Solve CSP, Cancel, New game, Undo
- [ ] Ouvrir et fermer plusieurs écrans à la suite (pas de plantage)
- [ ] Vérifier que l'algorithme génétique du projet 2 marche toujours (Play, labo, Watch)
- [ ] Regarder le rendu des deux styles dans une vraie fenêtre

## 5. Rendu / finitions
- [ ] `assets/ui.png` n'est plus utilisé par le code : le garder ou le retirer (voir `specs/ASSETS.md`)
- [ ] Remplir l'auteur / la source / la licence de `ui.png` et `cat_sprite.png` (`specs/ASSETS.md`, ligne « TO FILL IN »)
- [ ] Relecture : tout colle bien à l'énoncé (noms des méthodes, formulation)
- [ ] Préparer l'explication orale (comme `docs/ORAL_POINT_PAR_POINT.md` du projet 2)
