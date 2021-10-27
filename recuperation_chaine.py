#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from exception import ErreurDefinition, ErreurValeur, ErreurSynthaxe

def estUnAxiome(caractere):
    """Verifie si le caractère fait partie des caractères qui constituent normalement un axiome"""
    if(caractere == 'a' or caractere == 'b' or caractere == '+' or caractere == '-' or 
    caractere == '*' or caractere == '[' or caractere == ']'):
        return True
    else:
        return False

def estUneRegle(caractere):
    """Verifie si le caractère fait partie des caractères qui constituent normalement une règle"""
    if(estUnAxiome(caractere) or caractere == '='):
        return True
    else:
        return False

def verif_synthaxe_regle(regle):
    """Verifie que la valeur de la règle entre guillemet est bien écrite"""
    # La regle doit être de la forme "a=quelquechose" ou "b=quelquechose"
    if(not(len(regle) >= 3 and (regle[0] == "a" or regle[0] == "b") and regle[1] == "=")):
        raise ErreurValeur("La synthaxe de la chaine associé à la règle : '{}' est fausse".format(regle))
    
    # On verifie que les crochets "[" et "]" ont bien une fin et un début 
    nombreCrochet = 0
    for caractere in regle:
        if(caractere == "["):
            nombreCrochet += 1
        elif(caractere == "]"):
            if(nombreCrochet == 0): # On a eu un crochet qui se ferme sans crochet qui s'ouvre
                raise ErreurValeur("Crochet qui se ferme dans la regle alors qu'il n'a pas été ouvert")
            nombreCrochet -= 0      
    if(nombreCrochet != 0): # Il n'y a pas le même nombres de "[" et "]"
        raise ErreurValeur("Crochet qui a été ouvert dans la regle sans qu'il soit ferme")


def lecture_chaine(chaine, pos_actuel, definition, tailleRegle=0):
    """Lit une chaine de caractères entouré de guillemets sans prendre en compte les espaces"""
    # Si la variable tailleRegle != 0 alors on a affaire à une règle

    if(chaine[pos_actuel] == chaine[-1]):
        if(tailleRegle == 0):
            raise ErreurValeur("Il n'y a pas de valeur associé à l'/la {}".format(definition))
        else: # Il y'a au moins 1 chaines de caracteres associé à la regle
            return "", pos_actuel

    # On verifie si la synthaxe de la chaine de caractère est bonne 
    # en verifiant quelle commence par des guillemets
    if(chaine[pos_actuel] != '\"' and chaine[pos_actuel] != "\'"):
        if(tailleRegle == 0):
            raise ErreurSynthaxe("La chaine associé à l'{} doit commencer par des guillemets et non par : '{}'".format(definition, chaine[pos_actuel]))
        else: # Il y'a au moins 1 chaines de caracteres associé à la regle
            return "", pos_actuel

    # Variable qui permet de sauvegarder le type du guillemet utilisé
    guillemet = chaine[pos_actuel] 
    # Le caractere actuel est un guillemet, on passe au caractère suivant
    pos_actuel += 1
    # On sauvegarde le début de la chaine
    pos_debut = pos_actuel 

    # On lit toute la chaine de caractère
    while(chaine[pos_actuel] != '\"' and chaine[pos_actuel] != "\'"):
        if(chaine[pos_actuel] == chaine[-1]):
            raise ErreurSynthaxe("La chaine associé à l'{} doit se finir par des guillemets".format(definition))
        # On verifie que les caractères respectent bien leurs synthaxe par rapport a leur definition
        elif(definition == "axiome" and not(estUnAxiome(chaine[pos_actuel]))):
            raise ErreurValeur("La chaine associé à l'axiome comporte des caractères non pris en charge")
        elif((definition == "regle" or definition == "regles") and not(estUneRegle(chaine[pos_actuel]))):
            raise ErreurValeur("La chaine associé à la regle comporte des caractères non pris en charge")
        pos_actuel += 1

    if(guillemet != chaine[pos_actuel]):
        ErreurSynthaxe("Le guillemet qui ouvre la chaine et le guillemet qui la ferme ne sont pas les mêmes")

    return chaine[pos_debut:pos_actuel], pos_actuel+1 # Le caractère actuel est un guillemet, on peut passer au suivant

def lecture_regle(chaine, pos_actuel, regles):
    """Lit une ou plusieurs (ou aucune) chaines de caractères entourés de guillemets sans prendre en compte les espaces et retourne une liste de ces chaines de caractères"""
    # On lit les règles jusqu'a la fin du fichier s'il le faut
    while(pos_actuel < len(chaine)):
        regle, pos_actuel = lecture_chaine(chaine, pos_actuel, "regle", len(regles))

        # Cela veut dire que l'on a fini de lire toute les chaines de caractères de la regle
        if(regle == ""):
            break
        elif(len(regles) >= 2):
            raise ErreurValeur("Il ne peut y avoir au maximum que 2 regles (une pour a et une b)")

        verif_synthaxe_regle(regle)

        regles.append(regle)

    return regles, pos_actuel

def lecture_nombre(definition, chaine, pos_actuel, valeurNegatif=False):
    """Prend une chaines de caractères constitué d'un nombre et retourne un entier"""
    nombre = ""

    # Dans le cas où le nombre est négatif
    if(chaine[pos_actuel] == "-" and valeurNegatif == True):
        nombre += chaine[pos_actuel]
        pos_actuel += 1
        if(pos_actuel >= len(chaine)):
            raise ErreurSynthaxe("Signe '-' sans aucun chiffre après")

    while(chaine[pos_actuel].isdigit()):
        nombre += chaine[pos_actuel]
        pos_actuel += 1
        if(pos_actuel >= len(chaine)):
            break # On sort de la boucle pour voir ce qu'on va faire

    # Il faut aussi lire le point du nombre et les nombres après la virgule s'il y'en a 
    if(pos_actuel < len(chaine) and chaine[pos_actuel] == "."):
        nombre += chaine[pos_actuel]
        pos_actuel += 1
        while(pos_actuel < len(chaine) and chaine[pos_actuel].isdigit()):
            nombre += chaine[pos_actuel]
            pos_actuel += 1
            if(pos_actuel >= len(chaine)):
                break # On sort de la boucle pour voir ce qu'on va faire

    # Si nombre est vide ou juste egale a un point il y'a une erreur (venant du break forcé ou pas)
    if(nombre == "" or nombre == "."):
        raise ErreurValeur("La valeur associé à {} n'est pas un entier ou est vide".format(definition))

    # On le transforme en entier (on peut toujours transformé un ou 
    # plusieurs digit en entier, il n y aura donc pas d'erreur)
    return float(nombre), pos_actuel

def lecture_nombres(definition, chaine, pos_actuel, tailleListe, valeurNegatif=False):
    """Lit une chaine de caractère constitué de plusieurs nombre et retourne une liste de ces entiers"""
    nombres = ()

    nombre, pos_actuel = lecture_nombre(definition, chaine, pos_actuel, valeurNegatif)
    nombres += (nombre,) # Methode pour ajouté un nombre a un tuple

    # On lit un nombre tailleListe de nombres
    while(len(nombres) < tailleListe):
        # Les différents nombres doivent être séparé par des égalité
        if(pos_actuel >= len(chaine) or chaine[pos_actuel] != ","):
            raise ErreurValeur("La valeur associé à {} ne contient que {} nombres alors qu'il en faudrait {}, possible erreur de synthaxe".format(definition, len(nombres), tailleListe))
        nombre, pos_actuel = lecture_nombre(definition, chaine, pos_actuel+1)
        nombres += (nombre,) # Methode pour ajouté un nombre a un tuple
    
    return nombres, pos_actuel

def lecture_definition(chaine, pos_actuel):
    """Lit une des définitions du Lsystem"""
    # Lecture du premier mot de la ligne (d'une des definitions)
    pos_debut = pos_actuel
    # Dès qu'on arrive a la fin du mot on doit normalement avoir le caractère "="
    while(chaine[pos_actuel] != "="):
        # Le mot de la definition ne doit pas contenir d'autre caractère que des alphanumerics
        if(not(chaine[pos_actuel].isalpha())):
            if(pos_actuel == pos_debut):
                raise ErreurSynthaxe("Un caractere non pris en charge : '{}' apparait alors qu'on devrait avoir une définition ou la fin du programme".format(chaine[pos_actuel]))
            else:
                raise ErreurDefinition("Une definition n'a pas été lu, caractère non valide lu ou signe '=' manquant : '{}'".format(chaine[pos_debut:pos_actuel+1]))
        elif(chaine[pos_actuel] == chaine[-1]):
            raise ErreurSynthaxe("Signe '=' manquant, une définition n'est pas valide")
        pos_actuel += 1

    # On vérifiera dans "lecture_fichier" que le mot fait partie des définitions proposé
    # A noter qu'on retourne "pos_actuel+1" car le caractère "=" ne nous interesse pas

    # On s'assure que l'on est pas a la fin du fichier
    if(pos_actuel >= len(chaine)):
        raise ErreurValeur("La valeur associé à {} est vide".format(chaine[pos_debut:pos_actuel].lower()))

    # On met aussi la définition en caractère bas pour pouvoir lire 
    # tout type de casses concernant la police
    return chaine[pos_debut:pos_actuel].lower(), pos_actuel+1
