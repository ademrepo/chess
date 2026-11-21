# Oral — l'énoncé point par point (quoi dire, où est le code)

**Idée en 3 phrases.** Un cavalier = une suite de 63 mouvements (les gènes). On crée 50 cavaliers au
hasard, on **répare** les mouvements illégaux, on mesure combien de cases chaque cavalier visite
(fitness), puis on fabrique une nouvelle génération (tournoi → croisement → mutation). On répète
jusqu'à ce qu'un cavalier visite les 64 cases.

---

## 1. Classe `Chromosome` — `chromosome.py`

| Énoncé | Code | À dire |
|--------|------|--------|
| `genes` : tableau de 63 mouvements | `self.genes` | 64 cases − la case de départ = **63 mouvements**. Chaque gène est un entier de 1 à 8. |
| `init(genes)` | `__init__(genes=None)` | Sans argument (population initiale) → 63 gènes tirés au hasard ; sinon on copie les gènes reçus. |
| `crossover(partner)` | `crossover` | **Un point** de coupure tiré entre 1 et 62. Enfant 1 = début du parent 1 + fin du parent 2 ; enfant 2 = l'inverse. Retourne les 2 enfants. |
| `mutation()` | `mutation` | Chaque gène a une probabilité (0,01) de devenir un mouvement aléatoire. Sert à **explorer** de nouveaux mouvements. |

```python
point = random.randint(1, NB_GENES - 1)
child1 = Chromosome(self.genes[:point] + partner.genes[point:])
child2 = Chromosome(partner.genes[:point] + self.genes[point:])
```

Questions probables
- *Pourquoi 63 et pas 64 ?* Le cavalier est déjà sur la case (0,0) : il lui reste 63 cases à visiter.
- *Pourquoi un point de coupure entre 1 et 62 ?* Pour que chaque enfant reçoive au moins un gène de chaque parent.
- *Pourquoi 0,01 ?* Environ 0,6 gène muté par chromosome : assez pour garder de la diversité, pas assez pour détruire une bonne solution. Trop faible → la population stagne.

---

## 2. Classe `Knight` — `knight.py`

Variables : `position` (x, y), `chromosome`, `path`, `fitness`.

**`__init__(chromosome=None)`** : sans chromosome, il en crée un aléatoire. Position (0, 0),
fitness 0, `path = [(0, 0)]`.

**Les 8 directions** (`board.py`, y vers le bas, (0,0) en haut à gauche) :

| 1 haut-droite | 2 droite-haut | 3 droite-bas | 4 bas-droite | 5 bas-gauche | 6 gauche-bas | 7 gauche-haut | 8 haut-gauche |
|---|---|---|---|---|---|---|---|
| (+1, −2) | (+2, −1) | (+2, +1) | (+1, +2) | (−1, +2) | (−2, +1) | (−2, −1) | (−1, −2) |

**`move_forward(direction)`** : ajoute le déplacement à la position et ajoute la nouvelle position
à `path`.
**`move_backward(direction)`** : l'inverse. On retranche le déplacement et on retire la dernière
position de `path`. Sert à **annuler** un mouvement illégal.

**`check_moves()`** — le point le plus important. On rejoue le chromosome depuis (0, 0) :

```python
step = random.choice((1, -1))                 # sens du cycle, tiré UNE fois : +1 avant, -1 arrière
for i, direction in enumerate(genes):
    for k in range(8):                        # k = 0 : le gène lui-même, puis le cycle
        chosen = (direction - 1 + step * k) % 8 + 1
        self.move_forward(chosen)
        if (on_board(self.position) and self.position not in visited) or k == 7:
            break                             # légal, ou dernier essai : on le garde
        self.move_backward(chosen)            # illégal : on annule et on essaie le suivant
    genes[i] = chosen
    visited.add(self.position)
```

Un mouvement est **illégal** s'il sort de l'échiquier **ou** va sur une case déjà visitée.
Exemple de l'énoncé, gène 4 illégal :
- cycle avant → 5, 6, 7, 8, 1, 2, 3
- cycle arrière → 3, 2, 1, 8, 7, 6, 5

Si les 8 sont illégaux, le **dernier essayé est gardé** (et la fitness s'arrêtera là).
Le gène est **réécrit** avec le mouvement réellement joué (le chromosome correspond au chemin).
Le `set` `visited` rend le test « déjà visitée ? » instantané (plus rapide qu'une recherche dans la liste).

**`evaluate_fitness()`** : on parcourt `path`, on compte les cases jusqu'à la première invalide
(hors échiquier ou déjà vue). Maximum 64 = tour complet.

Questions probables
- *Pourquoi le sens du cycle est-il le même pour tout le chromosome ?* C'est l'énoncé ; cela rend la réparation déterministe une fois le sens tiré.
- *Pourquoi réécrire les gènes ?* Sinon on corrigerait le même gène illégal différemment à chaque génération et les bons enfants ne transmettraient pas leur réparation.
- *Pourquoi la fitness vaut-elle au moins 1 ?* La case de départ compte.
- *Pourquoi `move_backward` prend `direction` ?* Pour savoir quel déplacement retrancher.

---

## 3. Classe `Population` — `population.py`

Attributs : `population_size` (50), `generation` (1 au départ), `knights`.

| Fonction | Rôle |
|----------|------|
| `__init__(population_size)` | Crée `population_size` cavaliers aléatoires, `generation = 1`. |
| `check_population()` | Appelle `check_moves()` sur chaque cavalier. |
| `evaluate()` | Appelle `evaluate_fitness()` sur chacun, **retourne (meilleure fitness, meilleur cavalier)**. |
| `tournament_selection(size)` | Tire `size` (=3) cavaliers au hasard, les trie par fitness, garde les **2 meilleurs** comme parents. |
| `create_new_generation()` | Répète jusqu'à avoir autant d'enfants que de parents : 2 parents (tournoi) → croisement → mutation des 2 enfants. Puis `generation += 1`. |

```python
parent1, parent2 = self.tournament_selection(self.tournament_size)
child1, child2 = parent1.chromosome.crossover(parent2.chromosome)
child1.mutation(p);  child2.mutation(p)
```

Questions probables
- *Pourquoi un tournoi ?* Les bons se reproduisent plus souvent, mais un moyen peut encore gagner contre des faibles : on garde de la diversité.
- *Pourquoi pas de « meilleur gardé » (élitisme) ?* Ce n'est pas demandé ; la meilleure fitness peut donc baisser d'une génération à l'autre, mais la solution à 64 est détectée dès qu'elle apparaît.
- *Si la taille est impaire ?* On génère par paires puis on coupe à `population_size`.

---

## 4. La fonction `main` — `main.py`

C'est **exactement** la boucle de l'énoncé :

```python
population = Population(50)
while True:
    population.check_population()                 # réparer
    maxFit, bestSolution = population.evaluate()  # mesurer
    if maxFit == 64: break                        # tour complet → fini
    population.create_new_generation()            # nouvelle génération
```

Lancer : `python main.py` (interface : menu, paramètres, laboratoire, jeu, chat) ou
`python main.py --console --seed 1` (terminal, reproductible).

Questions probables
- *L'algorithme s'arrête-t-il toujours ?* Pas garanti en théorie (hasard), mais dans nos essais il s'arrête toujours : 2 à 165 générations, moins de 3 s.
- *Deux exécutions donnent-elles le même résultat ?* Non (population initiale, tournoi, coupure, mutation, sens du cycle sont aléatoires). `--seed` rend un run reproductible.
- *Complexité d'une génération ?* Environ `taille_population × 63` mouvements : linéaire.

---

## 5. Montrer le calcul à la prof : le laboratoire (interface)

Menu → **Algorithm lab**, Espace = une génération. On voit, pour la génération courante :
1. le **tournoi** (échantillon, les 2 parents),
2. le **croisement** (parents, enfant, point de coupure, 1 couleur = 1 mouvement),
3. la **mutation** (gènes mutés en rouge),
4. la **réparation** (combien de gènes `check_moves` a corrigés),
5. la **fitness** (meilleure, moyenne, pire) + la courbe, et pourquoi le meilleur chemin s'arrête.

Menu → **Settings** : population, mutation, tournoi, limite (utile pour montrer l'effet des paramètres).

---

## 6. Ordre conseillé pour l'explication (2 minutes)

1. Un gène = un mouvement ; 63 gènes = un chemin.
2. Un chromosome aléatoire sort vite de l'échiquier → `check_moves` le répare par cycle.
3. Fitness = nombre de cases valides (max 64).
4. Tournoi (3, on garde 2) → croisement à un point → mutation 1 %.
5. On répète jusqu'à 64. Démonstration dans le labo.
