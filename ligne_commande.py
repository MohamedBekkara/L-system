#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, getopt
from exception import ErreurLigneDeCommande

def lecture():
    """Lit la ligne de commande et retourne le fichier d'entrée (option -i) et fichier de sortie (option -o)"""
    fichierEntree = ""
    fichierSortie = ""

    # On récupère les options et valeurs de la ligne de commande (les arguments seront inutiles)
    optionsEtValeurs, argument = getopt.getopt(sys.argv[1:], "i:o:")

    # L'utilisateur n'est pas sensé lancé le programme avec des arguments
    if(argument != []):
        raise ErreurLigneDeCommande("Argument inutile au programme : '{}'".format(argument))

    # On lit toute la liste et on analyse les tuples (option, valeur)
    for optionEtValeur in optionsEtValeurs:
        if(optionEtValeur[0] == "-i"):
            if(fichierEntree != ""): # On a déjà affecter une valeur à l'argument "-i"
                raise ErreurLigneDeCommande("Répétition de l'arguments '-i'")
            fichierEntree = optionEtValeur[1]
        elif(optionEtValeur[0] == "-o"):
            if(fichierSortie != ""): # On a déjà affecter une valeur à l'argument "-o"
                raise ErreurLigneDeCommande("Répétition de l'arguments '-o'")
            fichierSortie = optionEtValeur[1]
        else:
            raise ErreurLigneDeCommande("Option '{}' non prise en compte".format(optionEtValeur[0]))

    if(fichierEntree == ""):
        raise ErreurLigneDeCommande("Vous n'avez pas précisé de fichier d'entrée (option '-i')") 

    # Il faut que le fichier de sortie soit un fichier python
    index = fichierSortie.find(".")
    if(fichierSortie == ""):
        fichierSortie = "sortie.py"
    elif(index == -1):
        fichierSortie = fichierSortie + ".py"
    elif(fichierSortie[index:] != ".py"):
        fichierSortie = fichierSortie[:index] + ".py"

    return fichierEntree, fichierSortie

def lecture_ligne_commande():
    """Gère les erreurs de la fonctions lecture"""
    try:
        return lecture()
    except:
        print("Exception lancé  - {} : {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        sys.exit()
    