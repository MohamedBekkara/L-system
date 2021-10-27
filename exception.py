#!/usr/bin/env python3
#-*- coding: utf-8 -*-

class Erreur(Exception):
    """Classe de base pour les exceptions de lecture de fichiers."""
    pass


class ErreurLigneDeCommande(Erreur):
    """Erreur qui est levé lorsque les arguments en ligne de commandes ne sont pas bon"""
    pass

class ErreurDefinition(Erreur):
    """Erreur qui est levé lorsque la définition d'une des lignes
    fichier est incorrect."""
    pass

class ErreurValeur(Erreur):
    """Erreur qui est levé lorsque la valeur d'un des mots du 
    fichier n'est pas pris en charge ou incorrect."""
    pass

class ErreurSynthaxe(Erreur):
    """Erreur qui est levé lorsque la synthaxe du fichier est incorrect"""
    pass