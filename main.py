"""Point d'entrée : un run de l'algorithme génétique, puis l'affichage de la solution."""

import sys

import affichage
import knight_tour


def main():
    # Accents corrects dans la console, y compris Git Bash
    sys.stdout.reconfigure(encoding="utf-8")
    resultat = knight_tour.lancer_run()
    # Création de l'interface pour afficher la solution
    affichage.jouer(resultat)


if __name__ == "__main__":
    main()
