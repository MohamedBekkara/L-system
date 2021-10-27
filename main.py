#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from lecture_fichier import lecture_final
from substitution import substitution
from creation_programme import creation_instruction, creation_fichier
from ligne_commande import lecture_ligne_commande

def main():
    "Fonction principal du projet, qui rassemble toute les partie"
    fichierEntree, fichierSortie = lecture_ligne_commande()

    axiome, regles, angle, taille, niveau, vitesse, couleur, position, epaisseur = lecture_final(fichierEntree)

    axiomeFinal = substitution(axiome, regles, niveau)

    instruction = creation_instruction(axiomeFinal, angle, taille, vitesse, couleur, position, epaisseur)

    creation_fichier(instruction, fichierSortie)

if __name__ == "__main__":
    main()