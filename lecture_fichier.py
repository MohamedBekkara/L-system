#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys

from exception import ErreurDefinition, ErreurValeur
from recuperation_chaine import lecture_definition, lecture_chaine, lecture_regle, lecture_nombre, lecture_nombres

from enum import Enum

class Lsystem(Enum):
    "Enumération des definitions du lsystem qui permettent de simplifier le code"
    AXIOME = 0
    REGLE = 1
    ANGLE = 2
    TAILLE = 3
    NIVEAU = 4
    VITESSE = 5
    COULEUR = 6
    POSITION = 7
    EPAISSEUR = 8


def enlever_espaces(chaine):
    "Enleve tout les caractères de type whitespaces dans une chaine"
    pos_actuel = 0
    
    while(pos_actuel < len(chaine)):
        if(chaine[pos_actuel].isspace()):
            chaine = chaine[:pos_actuel] + chaine[pos_actuel+1:]
        else:
            pos_actuel += 1

    return chaine


def verif_multiple(definition, nbApparition, apparitionMax = 1):
    if(nbApparition >= apparitionMax):
        raise ErreurDefinition("La definition {} est apparu {} fois alors quelle ne devrais apparatre que {} fois".format(definition, nbApparition+1, apparitionMax))
    else:
        return nbApparition + 1

def lecture_fichier(chaine):
    """Fonction principale du script qui s'occupe de lire toute la chaine de caractère et d'affecter aux variables les bonnes valeurs du Lsystem"""
    # Variables du Lsystem
    axiome = ""
    regles = []
    angle = 0
    taille = 10
    niveau = 0
    vitesse = 0 # C'est la vitesse la plus rapide
    couleur = (0, 0, 0) # La couleur sera de type (r, g, b)
    position = (100, 100)
    epaisseur = 2

    # Dictionnaire qui permet de verifier le nombre de fois que chaque définition va être appeler
    # Chaque valeur du dictionnaire est associé à une définition
    verif = {Lsystem.AXIOME: 0, Lsystem.REGLE: 0, Lsystem.ANGLE: 0, Lsystem.TAILLE: 0, Lsystem.NIVEAU: 0, 
    Lsystem.VITESSE: 0, Lsystem.COULEUR: 0, Lsystem.POSITION: 0, Lsystem.EPAISSEUR: 0 }

    # Position du "curseur" dans lequel on est dans le fichier
    pos_actuel = 0 

    # Les caractères vide au début et à la fin ne nous intérèsse pas dans le fichier
    chaine = enlever_espaces(chaine)

    # On lit le fichier jusqua la fin
    # On utilise while et pas un for pour avoir plus de flexibilité
    while pos_actuel < len(chaine):
        definition, pos_actuel = lecture_definition(chaine, pos_actuel) 

        # On effectue les affectations de variables demandé en fonction de la définition
        # Et on vérifie que les definitions ne soit pas déclarer plusieurs fois
        if(definition == "axiome"):
            axiome, pos_actuel = lecture_chaine(chaine, pos_actuel, "axiome")
            verif[Lsystem.AXIOME] = verif_multiple(definition, verif[Lsystem.AXIOME])
        elif(definition == "regle" or definition == "regles"):
            regles, pos_actuel = lecture_regle(chaine, pos_actuel, regles)
            verif[Lsystem.REGLE] = verif_multiple(definition, verif[Lsystem.REGLE], 2) # On peut avoir max 2 règles
        elif(definition == "angle"):
            angle, pos_actuel = lecture_nombre(definition, chaine, pos_actuel)
            verif[Lsystem.ANGLE] = verif_multiple(definition, verif[Lsystem.ANGLE])
        elif(definition == "taille"):
            taille, pos_actuel = lecture_nombre(definition, chaine, pos_actuel)
            verif[Lsystem.TAILLE] = verif_multiple(definition, verif[Lsystem.TAILLE])
        elif(definition == "niveau"):
            niveau, pos_actuel = lecture_nombre(definition, chaine, pos_actuel)
            verif[Lsystem.NIVEAU] = verif_multiple(definition, verif[Lsystem.NIVEAU])
        elif(definition == "vitesse"):
            vitesse, pos_actuel = lecture_nombre(definition, chaine, pos_actuel)
            verif[Lsystem.VITESSE] = verif_multiple(definition, verif[Lsystem.VITESSE])
        elif(definition == "couleur"):
            couleur, pos_actuel = lecture_nombres(definition, chaine, pos_actuel, 3)
            verif[Lsystem.COULEUR] = verif_multiple(definition, verif[Lsystem.COULEUR])
        elif(definition == "position"):
            position, pos_actuel = lecture_nombres(definition, chaine, pos_actuel, 2, True)
            verif[Lsystem.POSITION] = verif_multiple(definition, verif[Lsystem.POSITION])
        elif(definition == "epaisseur"):
            epaisseur, pos_actuel = lecture_nombre(definition, chaine, pos_actuel)
            verif[Lsystem.EPAISSEUR] = verif_multiple(definition, verif[Lsystem.EPAISSEUR])
        else:
            raise ErreurDefinition("La définition '{}' n'est pas prise en compte : ".format(definition))

    if(verif[Lsystem.AXIOME] == 0):
        raise ErreurDefinition("Il manque la défintion 'axiome' qui doit être obligatoire")
    elif(verif[Lsystem.ANGLE] == 0):
        raise ErreurDefinition("Il manque la défintion 'angle' qui doit être obligatoire")
    elif(verif[Lsystem.NIVEAU] == 0):
        raise ErreurDefinition("Il manque la défintion 'niveau' qui doit être obligatoire")

    return axiome, regles, angle, taille, niveau, vitesse, couleur, position, epaisseur
    
def lecture_final(nomfichier):
    """Gère les erreurs de la fonction lecture_fichier"""
    try:
        with open(nomfichier, "r") as fichier:
            chaine = fichier.read()
            return lecture_fichier(chaine)
    except FileNotFoundError:
        print("Le fichier '{}' n'existe pas dans le repertoire actuel".format(nomfichier))
    except:
        print("Exception lancé - {} : {}".format(sys.exc_info()[1], sys.exc_info()[1]))

    # Si rien n'est returner à ce moment là, une exception a été lancé donc on quitte le programme
    sys.exit()


# Partie qui permet d'utiliser ce scripts séparement si vous voulez verifier sa qualité

def afficher(axiome, regles, angle, taille, niveau, vitesse, couleur, position, epaisseur):
    "Affiche dans un terminal les variables du Lsystem"
    print("axiome : \"{}\"".format(axiome))
    for regle in regles:
        print("regle : \"{}\"".format(regle))
    print("angle : \"{}\"".format(angle))
    print("taille : \"{}\"".format(taille))
    print("niveau : \"{}\"".format(niveau))
    print("vitesse : \"{}\"".format(vitesse))
    print("couleur : \"{}\"".format(couleur))
    print("position : \"{}\"".format(position))
    print("epaisseur : \"{}\"".format(epaisseur))

if __name__ == "__main__":
    chaine = "axiome = 'a-a-a-a' regle = 'a=a+a*a+a+aa*aa+a+a*a+a' 'b=b++' angle = 90.5 taille = 10 niveau = 4 vitesse = 58 couleur = 72, 4, 5 position = -112, 45 epaisseur = 5"

    axiome, regles, angle, taille, niveau, vitesse, couleur, position, epaisseur = lecture_fichier(chaine)
    afficher(axiome, regles, angle, taille, niveau, vitesse, couleur, position, epaisseur)

    # regle = 'a=a+a*a+a+aa*aa+a+a*a+a' 'b=b++'