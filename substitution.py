#!/usr/bin/env python3
#-*- coding: utf-8 -*-

def substitution(axiome, regles, niveau):
    """Effectue des remplacement successif des 'a' et 'b' de l'axiome par les regles un nombre niveau de fois"""
    # Variable qui va augmenter au fur et à mesure des substitutions
    axiomeFinal = axiome

    # Si il n'y a pas de règle, alors la ligne final de substitution sera un axiome
    if regles != []:
        # On fait la substitution le nombre de fois qu'il y'a de niveau
        for _ in range(0, int(niveau)):
            # On fait la substitution des 2 règles si il y'en a 2, une sinon
            for regle in regles:
                # On remplace la première lettre de la regle dans l'axiome 
                # par ce a quoi est egale la regle
                axiomeFinal = axiomeFinal.replace(regle[0], regle[2:])     

    return axiomeFinal


# Partie qui permet d'utiliser ce scripts séparement si vous voulez verifier sa qualité

if __name__ == "__main__":
    chaine = substitution("a", "a=b", 1)
    print(chaine)