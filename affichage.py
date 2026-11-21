"""Interface pygame : anime le chemin du meilleur cavalier trouvé par l'algorithme génétique."""

import math
import os

import pygame

import knight_tour as kt

# --- Réglages de l'animation ---
DUREE_SAUT = 0.5          # secondes par saut à la vitesse x1
VITESSES = (0.5, 1, 2, 4)  # multiplicateurs proposés par le bouton engrenage
VITESSE_INITIALE = 1       # indice dans VITESSES
HAUTEUR_SAUT = 46          # hauteur de l'arc du saut, en pixels
FONDU_TEINTE = 1.0         # une case se teinte complètement en 1 saut
DUREE_IMAGE_IDLE = 180     # millisecondes par image d'idle
IMAGES_PAR_SECONDE = 60
NB_RUNS_AFFICHES = 4

# --- Fenêtre et mise en page ---
TITRE = "Knight's Tour"
TAILLE_FENETRE = (1220, 740)
POSITION_DAMIER = (20, 50)
TAILLE_CASE = 64
COLONNE_X = 660
COLONNE_LARGEUR = 540
RECT_PLAQUE_ECRAN = pygame.Rect(COLONNE_X, 20, COLONNE_LARGEUR, 80)
RECT_PANNEAU_ECRAN = pygame.Rect(COLONNE_X, 110, COLONNE_LARGEUR, 540)
LARGEUR_RUBAN, HAUTEUR_RUBAN = 260, 62
TAILLE_BARRE = (480, 101)
TAILLE_BOUTON = (68, 68)
TAILLE_BOUTON_RETOUR = (96, 68)
Y_BOUTONS = 664
ECART_BOUTONS = 24
RECT_LECTURE = pygame.Rect((COLONNE_X, Y_BOUTONS), TAILLE_BOUTON)
RECT_RELANCER = pygame.Rect((RECT_LECTURE.right + ECART_BOUTONS, Y_BOUTONS), TAILLE_BOUTON_RETOUR)
RECT_VITESSE = pygame.Rect((RECT_RELANCER.right + ECART_BOUTONS, Y_BOUTONS), TAILLE_BOUTON)
MARGE_HAUT_PANNEAU = 22
HAUTEUR_LIGNE = 26
ECART_SECTION = 8
RAYON_COORDONNEE = 11
DECALAGE_COORDONNEES = 26  # distance entre la grille et les chiffres 1 à 8 dans la marge

# --- Mesures faites sur les images de assets/ (rectangles x, y, largeur, hauteur) ---
IMAGE_UI = os.path.join("assets", "ui.png")
IMAGE_CHAT = os.path.join("assets", "cat spirte.png")
RECT_DAMIER = (45, 42, 643, 690)
ORIGINE_GRILLE = (99, 100)   # coin haut-gauche de la 1re case, dans ui.png
TAILLE_GRILLE = (535, 565)   # les 8 cases, non carrées (≈ 66,9 × 70,6)
RECT_CADRE_SOMBRE = (710, 47, 321, 324)
RECT_PLAQUE = (1055, 50, 277, 141)
RECT_PLAY = (1054, 198, 80, 80)
RECT_PAUSE = (1141, 290, 78, 82)
RECT_ENGRENAGE = (1141, 198, 78, 80)
RECT_RETOUR = (1227, 296, 106, 76)
RECT_RUBAN = (1051, 394, 276, 73)
RECT_BARRE = (727, 603, 610, 129)
# Compartiments de la barre, en fraction de sa largeur, et hauteur de leur centre
COMPARTIMENTS_BARRE = ((0.03, 0.26), (0.28, 0.72), (0.74, 0.97))
CENTRE_Y_BARRE = 0.40

# Images d'idle du chat : 4 images par rangée
IMAGES_CHAT = {
    "face": [(84, 50, 208, 213), (417, 51, 207, 212), (755, 51, 204, 213), (1083, 51, 205, 213)],
    "cote": [(88, 294, 242, 216), (419, 296, 244, 214), (766, 295, 242, 216), (1086, 295, 241, 214)],
    "dos": [(113, 534, 201, 214), (427, 538, 213, 210), (758, 534, 233, 214), (1101, 533, 217, 215)],
}
ECHELLE_CHAT = 0.32
TAILLE_OMBRE = (40, 12)
ALPHA_OMBRE = 90

# --- Couleurs ---
CREME = (245, 230, 190)
BRUN_FONCE = (74, 44, 26)
OR = (255, 205, 80)
COULEUR_TEINTE = (230, 150, 60)
ALPHA_TEINTE = 120
FOND_COORDONNEE = (38, 22, 14)  # disque derrière les chiffres 1 à 8, par-dessus les clous
BLANC_CREME = (255, 248, 225)
BLEU_DEPART = (70, 140, 255)
JAUNE_COURANT = (255, 215, 40)
FOND = (28, 18, 14)

# Facteurs d'étirement du damier pour que les cases deviennent carrées (64 × 64)
ECHELLE_X = TAILLE_CASE / (TAILLE_GRILLE[0] / kt.TAILLE_PLATEAU)
ECHELLE_Y = TAILLE_CASE / (TAILLE_GRILLE[1] / kt.TAILLE_PLATEAU)
ORIGINE_ECRAN = (
    POSITION_DAMIER[0] + round((ORIGINE_GRILLE[0] - RECT_DAMIER[0]) * ECHELLE_X),
    POSITION_DAMIER[1] + round((ORIGINE_GRILLE[1] - RECT_DAMIER[1]) * ECHELLE_Y),
)


def decouper(feuille, rect, taille=None):
    """Extrait un morceau de la planche, éventuellement redimensionné (avec lissage)."""
    morceau = feuille.subsurface(rect).copy()
    return pygame.transform.smoothscale(morceau, taille) if taille else morceau


def charger_numeros(police, couleur):
    return {n: police.render(str(n), True, couleur) for n in range(1, kt.FITNESS_MAX + 1)}


def charger_ressources():
    ui = pygame.image.load(IMAGE_UI).convert_alpha()
    feuille_chat = pygame.image.load(IMAGE_CHAT).convert_alpha()

    taille_damier = (round(RECT_DAMIER[2] * ECHELLE_X), round(RECT_DAMIER[3] * ECHELLE_Y))
    chats = {}
    for rangee, rects in IMAGES_CHAT.items():
        chats[rangee] = []
        for rect in rects:
            taille = (round(rect[2] * ECHELLE_CHAT), round(rect[3] * ECHELLE_CHAT))
            chats[rangee].append(decouper(feuille_chat, rect, taille))

    police_numero = pygame.font.Font(None, 30)
    return {
        "damier": decouper(ui, RECT_DAMIER, taille_damier),
        "panneau": decouper(ui, RECT_CADRE_SOMBRE, RECT_PANNEAU_ECRAN.size),
        "plaque": decouper(ui, RECT_PLAQUE, RECT_PLAQUE_ECRAN.size),
        "ruban": decouper(ui, RECT_RUBAN, (LARGEUR_RUBAN, HAUTEUR_RUBAN)),
        "barre": decouper(ui, RECT_BARRE, TAILLE_BARRE),
        "play": decouper(ui, RECT_PLAY, TAILLE_BOUTON),
        "pause": decouper(ui, RECT_PAUSE, TAILLE_BOUTON),
        "engrenage": decouper(ui, RECT_ENGRENAGE, TAILLE_BOUTON),
        "retour": decouper(ui, RECT_RETOUR, TAILLE_BOUTON_RETOUR),
        "chats": chats,
        "numeros_creme": charger_numeros(police_numero, CREME),
        "numeros_bruns": charger_numeros(police_numero, BRUN_FONCE),
        "police_titre": pygame.font.Font(None, 54),
        "police_ruban": pygame.font.Font(None, 30),
        "police": pygame.font.Font(None, 26),
        "police_petite": pygame.font.Font(None, 20),
        "police_grande": pygame.font.Font(None, 36),
    }


def ecrire(ecran, texte, police, couleur, **ancre):
    """Écrit un texte ; ancre = center=(x, y), topleft=(x, y), midright=(x, y)..."""
    image = police.render(texte, True, couleur)
    ecran.blit(image, image.get_rect(**ancre))


def rect_de_case(case):
    x, y = case
    return pygame.Rect(
        ORIGINE_ECRAN[0] + x * TAILLE_CASE, ORIGINE_ECRAN[1] + y * TAILLE_CASE,
        TAILLE_CASE, TAILLE_CASE,
    )


def dessiner_coordonnee(ecran, img, texte, centre):
    pygame.draw.circle(ecran, FOND_COORDONNEE, centre, RAYON_COORDONNEE)
    ecrire(ecran, texte, img["police_petite"], CREME, center=centre)


def dessiner_coordonnees(ecran, img):
    for i in range(kt.TAILLE_PLATEAU):
        x, y = rect_de_case((i, i)).center
        dessiner_coordonnee(ecran, img, str(i + 1), (x, ORIGINE_ECRAN[1] - DECALAGE_COORDONNEES))
        dessiner_coordonnee(ecran, img, str(i + 1), (ORIGINE_ECRAN[0] - DECALAGE_COORDONNEES, y))


def dessiner_case_visitee(ecran, img, case, numero, avancement):
    """Teinte la case et écrit son numéro d'ordre ; avancement va de 0 à 1 (fondu)."""
    teinte = pygame.Surface((TAILLE_CASE, TAILLE_CASE), pygame.SRCALPHA)
    teinte.fill((*COULEUR_TEINTE, round(ALPHA_TEINTE * avancement)))
    rect = rect_de_case(case)
    ecran.blit(teinte, rect)

    case_claire = sum(case) % 2 == 0
    numeros = img["numeros_bruns"] if case_claire else img["numeros_creme"]
    image = numeros[numero].copy()
    image.set_alpha(round(255 * avancement))
    ecran.blit(image, image.get_rect(center=rect.center))


def dessiner_cadre(ecran, case, couleur):
    pygame.draw.rect(ecran, couleur, rect_de_case(case).inflate(-4, -4), width=4, border_radius=8)


def direction_du_saut(chemin, numero_saut):
    """Rangée de sprite et retournement selon l'axe de déplacement dominant."""
    (x1, y1), (x2, y2) = chemin[numero_saut], chemin[numero_saut + 1]
    dx, dy = x2 - x1, y2 - y1
    if abs(dy) > abs(dx):
        return ("dos" if dy < 0 else "face"), False
    return "cote", dx < 0  # le chat de côté regarde vers la droite


def dessiner_chat(ecran, img, chemin, avancement_saut):
    """Position du chat avec l'arc du saut ; avancement_saut = nombre de sauts faits."""
    dernier_saut = len(chemin) - 2
    numero_saut = min(int(avancement_saut), dernier_saut)
    t = min(avancement_saut - numero_saut, 1)
    x1, y1 = rect_de_case(chemin[numero_saut]).center
    x2, y2 = rect_de_case(chemin[numero_saut + 1]).center
    x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
    hauteur = math.sin(math.pi * t) * HAUTEUR_SAUT
    pieds = (round(x), round(y) + TAILLE_CASE // 2 - 6)

    rangee, retourne = direction_du_saut(chemin, numero_saut)
    numero_image = pygame.time.get_ticks() // DUREE_IMAGE_IDLE % len(img["chats"][rangee])
    image = img["chats"][rangee][numero_image]
    if retourne:
        image = pygame.transform.flip(image, True, False)

    ombre = pygame.Surface(TAILLE_OMBRE, pygame.SRCALPHA)
    pygame.draw.ellipse(ombre, (0, 0, 0, ALPHA_OMBRE), ombre.get_rect())
    ecran.blit(ombre, ombre.get_rect(center=(pieds[0], pieds[1] - 4)))
    ecran.blit(image, image.get_rect(midbottom=(pieds[0], pieds[1] - round(hauteur))))


def dessiner_ruban(ecran, img, titre, midtop):
    """Dessine un ruban titre ; retourne le y de son bord bas."""
    rect = img["ruban"].get_rect(midtop=midtop)
    ecran.blit(img["ruban"], rect)
    ecrire(ecran, titre, img["police_ruban"], CREME, center=rect.center)
    return rect.bottom


def dessiner_barre(ecran, img, valeurs, midtop):
    """Barre à 3 compartiments, (titre, valeur) dans chacun ; retourne le y de son bord bas."""
    rect = img["barre"].get_rect(midtop=midtop)
    ecran.blit(img["barre"], rect)
    y = rect.top + rect.height * CENTRE_Y_BARRE
    for (debut, fin), (titre, valeur) in zip(COMPARTIMENTS_BARRE, valeurs):
        x = rect.left + rect.width * (debut + fin) / 2
        ecrire(ecran, titre, img["police_petite"], CREME, center=(x, y - 14))
        ecrire(ecran, valeur, img["police_grande"], OR, center=(x, y + 10))
    return rect.bottom


def dessiner_panneau(ecran, img, etat):
    """Empile les sections du panneau ; y avance au fur et à mesure."""
    ecran.blit(img["panneau"], RECT_PANNEAU_ECRAN)
    milieu = RECT_PANNEAU_ECRAN.centerx
    y = RECT_PANNEAU_ECRAN.top + MARGE_HAUT_PANNEAU
    cavalier, generations, duree, fitness_moyenne = etat["resultat"]

    y = dessiner_ruban(ecran, img, "Résultat", (milieu, y))
    y = dessiner_barre(ecran, img, (
        ("Génération", str(generations)),
        ("Durée", f"{duree:.2f} s"),
        ("Fitness", str(cavalier.fitness)),
    ), (milieu, y))
    y += ECART_SECTION
    ecrire(ecran, f"Fitness moyenne finale : {fitness_moyenne:.1f}", img["police"], CREME,
           midtop=(milieu, y))
    y += HAUTEUR_LIGNE + ECART_SECTION

    y = dessiner_ruban(ecran, img, "Paramètres", (milieu, y))
    ecrire(ecran, f"Population : {kt.TAILLE_POPULATION}", img["police"], CREME,
           midtop=(milieu, y))
    ecrire(ecran, f"Taux de mutation : {kt.TAUX_MUTATION}", img["police"], CREME,
           midtop=(milieu, y + HAUTEUR_LIGNE))
    y += 2 * HAUTEUR_LIGNE + ECART_SECTION

    y = dessiner_ruban(ecran, img, "Historique", (milieu, y))
    premier = max(0, len(etat["historique"]) - NB_RUNS_AFFICHES)
    for ligne, (generations, duree) in enumerate(etat["historique"][premier:]):
        numero = premier + ligne + 1
        couleur = OR if numero == len(etat["historique"]) else CREME
        ecrire(ecran, f"Run {numero} : {generations} générations, {duree:.2f} s", img["police"],
               couleur, midtop=(milieu, y + ligne * HAUTEUR_LIGNE))


def dessiner_boutons(ecran, img, etat):
    ecran.blit(img["pause" if etat["lecture"] else "play"], RECT_LECTURE)
    ecran.blit(img["retour"], RECT_RELANCER)
    ecran.blit(img["engrenage"], RECT_VITESSE)
    ecrire(ecran, f"x{VITESSES[etat['vitesse']]}", img["police_grande"], OR,
           midleft=(RECT_VITESSE.right + 12, RECT_VITESSE.centery))
    droite = COLONNE_X + COLONNE_LARGEUR
    ecrire(ecran, "Espace : lecture / pause", img["police"], BLANC_CREME,
           midright=(droite, RECT_VITESSE.centery - HAUTEUR_LIGNE // 2))
    ecrire(ecran, "R : relancer", img["police"], BLANC_CREME,
           midright=(droite, RECT_VITESSE.centery + HAUTEUR_LIGNE // 2))


def dessiner(ecran, img, etat):
    chemin = etat["resultat"][0].path
    avancement = etat["avancement"]
    ecran.fill(FOND)

    ecran.blit(img["damier"], POSITION_DAMIER)
    dessiner_coordonnees(ecran, img)
    for numero, case in enumerate(chemin):
        if avancement >= numero:
            fondu = 1 if numero == 0 else min((avancement - numero) / FONDU_TEINTE, 1)
            dessiner_case_visitee(ecran, img, case, numero + 1, fondu)
    dessiner_cadre(ecran, chemin[0], BLEU_DEPART)
    dessiner_cadre(ecran, chemin[int(avancement)], JAUNE_COURANT)
    dessiner_chat(ecran, img, chemin, avancement)

    ecran.blit(img["plaque"], RECT_PLAQUE_ECRAN)
    ecrire(ecran, TITRE, img["police_titre"], BRUN_FONCE, center=RECT_PLAQUE_ECRAN.center)
    dessiner_panneau(ecran, img, etat)
    dessiner_boutons(ecran, img, etat)


def afficher_calcul(ecran, img):
    ecran.fill(FOND)
    ecrire(ecran, "Calcul en cours...", img["police_grande"], CREME,
           center=ecran.get_rect().center)
    pygame.display.flip()


def ajouter_run(etat, resultat):
    """Range le run dans l'historique et relance l'animation sur son chemin."""
    _, generations, duree, _ = resultat
    etat["resultat"] = resultat
    etat["historique"].append((generations, duree))
    etat["avancement"] = 0.0
    etat["lecture"] = True


def nouveau_run(ecran, img, etat):
    """Relance un run complet ; le calcul se fait avant l'animation."""
    afficher_calcul(ecran, img)
    ajouter_run(etat, kt.lancer_run())


def nombre_de_sauts(etat):
    return len(etat["resultat"][0].path) - 1


def basculer_lecture(etat):
    etat["lecture"] = not etat["lecture"]
    if etat["lecture"] and etat["avancement"] >= nombre_de_sauts(etat):
        etat["avancement"] = 0.0  # on rejoue depuis le début


def jouer(premier_resultat):
    """Ouvre la fenêtre et anime le résultat d'un run (celui retourné par lancer_run)."""
    pygame.init()
    pygame.display.set_caption(TITRE)
    ecran = pygame.display.set_mode(TAILLE_FENETRE)
    img = charger_ressources()
    horloge = pygame.time.Clock()

    etat = {"historique": [], "vitesse": VITESSE_INITIALE}
    ajouter_run(etat, premier_resultat)

    en_cours = True
    while en_cours:
        duree_image = horloge.tick(IMAGES_PAR_SECONDE) / 1000
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_SPACE:
                basculer_lecture(etat)
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_r:
                nouveau_run(ecran, img, etat)
            elif evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                if RECT_LECTURE.collidepoint(evenement.pos):
                    basculer_lecture(etat)
                elif RECT_RELANCER.collidepoint(evenement.pos):
                    nouveau_run(ecran, img, etat)
                elif RECT_VITESSE.collidepoint(evenement.pos):
                    etat["vitesse"] = (etat["vitesse"] + 1) % len(VITESSES)

        if etat["lecture"]:
            sauts_faits = duree_image * VITESSES[etat["vitesse"]] / DUREE_SAUT
            etat["avancement"] = min(etat["avancement"] + sauts_faits, nombre_de_sauts(etat))
            etat["lecture"] = etat["avancement"] < nombre_de_sauts(etat)  # fini : icône play

        dessiner(ecran, img, etat)
        pygame.display.flip()
    pygame.quit()
