# EXPLICATION — le projet en bref (pour l'oral)

## 1. Le problème

Trouver une suite de **63 mouvements de cavalier**, depuis la case (0, 0), qui visite les **64 cases une
seule fois**. On utilise un **algorithme génétique** (Chapitre 2) : une population de solutions
candidates qui évolue par sélection, croisement et mutation.

## 2. Chapitre 2 → code

| Algorithme génétique | Dans le code |
|----------------------|--------------|
| Individu = tableau de gènes | `Chromosome.genes` : 63 entiers de 1 à 8 (un gène = un mouvement) |
| Fonction de fitness (max = meilleur) | `Knight.evaluate_fitness()` : nb de cases valides, max 64 |
| Population initiale aléatoire | `Population.__init__` : 50 cavaliers au chromosome aléatoire |
| Sélection | `Population.tournament_selection(3)` |
| Croisement à un point | `Chromosome.crossover(partner)` |
| Mutation (faible probabilité) | `Chromosome.mutation(p)` |
| Nouvelle génération, on recommence | `Population.create_new_generation()` + la boucle `while` de `main.py` |
| Arrêt | fitness == 64 |

## 3. Les fichiers (un fichier = une classe de l'énoncé)

- `board.py` : constantes et table `MOVES`. Direction 1 = haut-droite = (+1, −2), puis sens horaire
  (2 : (+2,−1), 3 : (+2,+1), 4 : (+1,+2), 5 : (−1,+2), 6 : (−2,+1), 7 : (−2,−1), 8 : (−1,−2)).
  L'axe y va vers le bas, (0, 0) est le coin en haut à gauche.
- `chromosome.py` : `crossover`, `mutation`.
- `knight.py` : `move_forward`, `move_backward`, `check_moves`, `evaluate_fitness`.
- `population.py` : `check_population`, `evaluate`, `tournament_selection`, `create_new_generation`.
- `genetic_algorithm.py` : la boucle `main` de l'énoncé sous forme de fonction (console, GUI).
- `main.py` : point d'entrée (console ou interface).
- `game.py` : jeu manuel, réutilise `Knight`.
- `gui/` : écrans pygame. `settings_screen.py` (paramètres), `lab_screen.py` (laboratoire pas à pas),
  `game_screen.py`, `replay_screen.py` (chat), `home_screen.py`.
- `test_core.py` : 12 tests, sans pygame.

## 3 bis. Le laboratoire (à montrer à la prof)

Menu → *Algorithm lab*. Il utilise les **vraies** classes ; un clic sur *Step* = une génération.
Panneau de droite, de haut en bas :
1. **Statistiques** : génération, meilleure fitness, moyenne, pire, meilleure de tous les temps.
2. **Courbes** de fitness (meilleure en vert, moyenne en jaune) : on voit la population progresser.
3. **Comment la génération a été calculée** : (1) échantillon du tournoi et les 2 parents ;
   (2) croisement : parent 1, parent 2, enfant, trait blanc = point de coupure (1 couleur = 1 mouvement) ;
   (3) mutation : gènes mutés entourés en rouge, nombre attendu ≈ taille × 63 × p ;
   (4) réparation : nombre de gènes illégaux remplacés par `check_moves` ; (5) fitness.
Le plateau montre le meilleur chemin et **pourquoi il s'arrête** (sort de l'échiquier ou case déjà visitée).
Menu *Settings* : population, mutation, tournoi, limite ; ces valeurs servent aussi au jeu et au chat.

## 4. `check_moves` (le point le plus délicat)

Pour chaque gène, dans l'ordre :

1. `move_forward(gène)`.
2. Si la case est **hors de l'échiquier** ou **déjà visitée** → `move_backward`, puis on essaie les
   directions suivantes **en cycle**, dans un sens tiré **une seule fois par chromosome** (avant ou arrière).
   Ex. : gène 4 illégal, cycle avant → 5, 6, 7, 8, 1, 2, 3 ; cycle arrière → 3, 2, 1, 8, 7, 6, 5.
3. Si les 8 directions sont illégales, **le dernier mouvement essayé est gardé** (comme dit l'énoncé) ;
   `evaluate_fitness` s'arrêtera à cette case.
4. Le gène est **réécrit** avec le mouvement réellement joué.

Optimisation : un `set` de cases visitées (test en O(1) au lieu de parcourir la liste `path`) →
`check_moves` est environ 3× plus rapide.

## 5. Les trois opérateurs

- **Tournoi de taille 3** : 3 cavaliers distincts tirés au hasard, triés par fitness, les 2 meilleurs sont
  les parents. Les bons se reproduisent plus souvent, mais un faible peut gagner contre deux plus faibles :
  la diversité est conservée.
- **Croisement à un point** : point de coupure entre 1 et 62. Enfant 1 = début du parent 1 + fin du
  parent 2 ; enfant 2 = l'inverse. Tout mélange de mouvements est un chromosome valide (la réparation
  corrige la légalité ensuite), donc pas besoin de PMX/OX comme pour le TSP.
- **Mutation** : chaque gène devient un mouvement aléatoire avec probabilité 0,01 (≈ 0,6 gène par
  chromosome).

## 6. Paramètres : population 50, mutation 0,01

Mesures (seeds 1 à 5, `python main.py --console --seed N`) : 2, 9, 79, 147 et 165 générations, soit
0,02 à 3 s. La variance est normale : l'algorithme est stochastique. Une mutation trop faible (0,001) fait
parfois stagner la population dans un optimum local ; 0,01 maintient assez de diversité.
Essayer d'autres valeurs : `python main.py --console --population 100 --mutation 0.02`.

## 7. Questions probables

**Pourquoi `check_moves` réécrit les gènes ?** Pour que le chromosome corresponde au chemin réellement
parcouru ; sinon le même mouvement illégal serait réparé différemment à chaque génération.

**Pourquoi le croisement est toujours appliqué ?** Probabilité 1, valeur du Chapitre 2. Pas d'élitisme
(non demandé) : la meilleure fitness peut baisser d'une génération à l'autre, mais la solution à 64 est
détectée dès qu'elle apparaît.

**L'algorithme s'arrête-t-il toujours ?** Pas garanti en théorie (stochastique), mais dans nos essais
il s'arrête toujours. `main` suit l'énoncé : `while True` sans limite.

**Deux exécutions donnent-elles la même solution ?** Non (population initiale, sélection, point de
coupure, mutation, sens du cycle sont aléatoires). `--seed` rend une exécution reproductible.

**Complexité d'une génération ?** `taille_population × 63` mouvements pour la réparation et
l'évaluation, plus `taille_population` croisements de 63 gènes : linéaire.

**Pourquoi fitness = 64 maximum ?** On compte les cases valides du chemin, départ inclus : 64 cases =
tour complet.

**D'où vient l'image du cavalier ?** Jeu de pièces libre *cburnett* (GPLv2+), détails et empreintes dans
`specs/ASSETS.md`.
