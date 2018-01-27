import pickle

colonne=["ordre","sec","libre"]
coups=["1","2","3","4","5","6","st","Bonus","full","moins","plus","carre","suite","yam"]

print("\nCe programme est très simple d'utilisation, parlez lui comme à un être humain et si il ne vous comprend pas, il vous le fera savoir. Il est aussi possible si besoin de lui demander de l'aide à tout moment pour qu'il vous explique ce qu'il vous est possible de faire. Sur ce bonne chance pour vos futures parties.")


def affiche_partie(nom, ens_joueur):
    print("\n{}:".format(nom.upper()))

    for col in colonne:
        print("|{:<25}".format(col.upper()), end = "")
    print()

    for coup in coups:
        for col in colonne:
            print("|{:<15}{:>10}".format(coup, ens_joueur[nom][col][coup]), end = "")
        print()

def sous_total(nom, ens_joueur):
    for col in colonne:
        res = 0
        for i in range(1, 7):
            score = ens_joueur[nom][col][str(i)]
            if score != "XXXX":
                res += int(score)
        ens_joueur[nom][col]["st"] = res

def total(nom, ens_joueur):
    res=0

    for col in colonne:
        for coup in coups:
            score = ens_joueur[nom][col][coup]
            if score != "XXXX" and coup != "st":
                res += int(score)

    return res

def verifier(ens_joueur):
    for nom in ens_joueur:
        for col in colonne:
            for coup in coups:
                if "XXXX" == ens_joueur[nom][col][coup]:
                    return True
    return False

def moyenne(nom, rec):
    total = 0

    for i in rec[nom]:
        total += rec[nom][i]

    return total/len(rec[nom])

def ecart_type(nom, rec):
    ec=0

    for i in rec[nom]:
        ec += (rec[nom][i]-rec["moyenne"][nom])**2

    return (ec/len(rec[nom]))**0.5

def imprimer_score(rec):
    print(" "*10 + "|", end="")

    for nom in rec:
        if not(nom in ["moyenne", "nombre de parties", "ecart-type"]):
            print(" {} |".format(nom), end="")
    print()

    for i in range(1, rec["nombre de parties"]+1):
        print("partie{:<4}|".format(i%10000), end = "")
        for nom in rec:
            if not(nom in ["moyenne", "nombre de parties", "ecart-type"]):
                if "partie "+str(i) in rec[nom]:
                    print(("{:>"+str(len(nom)+2)+"}|").format(rec[nom]["partie "+str(i)]), end = "")
                else:
                    print((" "*(len(nom)+1))+"X|", end = "")
        print()

    print("moyenne   |", end = "")
    for nom in rec:
        if not(nom in ["moyenne", "nombre de parties", "ecart-type"]):
            print(("{:>"+str(len(nom)+2)+"}|").format(int(rec["moyenne"][nom])), end = "")
    print()

    print("ecart-type|", end = "")
    for nom in rec:
        if not(nom in ["moyenne", "nombre de parties", "ecart-type"]):
            print(("{:>"+str(len(nom)+2)+"}|").format(int(rec["ecart-type"][nom])), end = "")
    print()


def init_vars_game(liste, ens_joueur):
    print("Vous venez de commencer une nouvelle partie avec :")
    for nom in (input("Qui sont les joueurs qui vont jouer? ")).split(" "):
        if nom != "":
            print("\t->", nom)
            ens_joueur[nom] = dict()
            liste.append(nom)
            for c in colonne:
                ens_joueur[nom][c] = dict()
                for coup in coups:
                    ens_joueur[nom][c][coup] = "XXXX"

def one_loop_of_game(ind, liste, ens_joueur):
    for i in range(ind, len(liste)):
        case = [""]
        affiche_partie(liste[i], ens_joueur)
        print("TOTAL:", total(liste[i], ens_joueur))
        case = (input("Où voulez vous mettre vos points? ")).split(" ")

        #mauvaise entrée
        while not(("abandon" in case[0]) or ("stop" in case[0]) or ("arret" in case[0]) or ("quitte" in case[0]) or (len(case) == 2 and (case[0] in colonne) and (case[1] in coups))):
            if not("aide" in case[0]):
                print("Non ce n'est pas possible connard réessaye encore...")
            else:
                print("Il est ici simplement possible de sélectionner une case en me donnant son nom ou de quitter la partie en cours.")
            case = (input("Où voulez vous mettre vos points? ")).split(" ")

        #abandon de la partie
        if ("abandon" in case[0]) or ("stop" in case[0]) or ("arret" in case[0]) or ("quitte" in case[0]) or ("sop" in case[0]):
            enr = input("Voulez vous enregistrer la partie en cours? ")
            if ("oui" in enr) or ("yes" in enr):
                with open("partie_enr", "wb") as fiche:
                    mo = pickle.Pickler(fiche)
                    mo.dump([])
                with open("partie_enr","wb") as fiche:
                    mo = pickle.Pickler(fiche)
                    mo.dump([ens_joueur, liste, i])
                    print("la partie a été enregistré.")
            else :
                print("La partie n'a pas été enregistré.")
            main()
            exit()

        ens_joueur[liste[i]][case[0]][case[1]] = input("Combien avez vous fait? ")
        sous_total(liste[i], ens_joueur)
        for col in colonne:
            if ens_joueur[liste[i]][col]["st"] >= 60:
                ens_joueur[nom][col]["Bonus"] = 20


def game():
    ens_joueur = dict()
    liste = list()

    with open("partie_enr","rb") as fiche:
        mo = pickle.Unpickler(fiche)
        rep = mo.load()
        taille = len(rep)

    #si une partie est enregistrée
    if taille > 0:
        answer = input("Voulez vous reprendre la partie enregistré? ")
        if "oui" in answer:
            print("Vous venez de reprendre une partie enregistrée avec comme joueurs:")

            ind = rep[2]
            liste += rep[1]
            ens_joueur = rep[0]

            for nom in liste:
                print("\t->", nom)

            one_loop_of_game(ind, liste, ens_joueur)
        elif "non" in answer:
            if "oui" in input("Voulez-vous supprimer la partie sauvegardé? "):
                with open("partie_enr", "wb") as fiche:
                    mo = pickle.Pickler(fiche)
                    mo.dump([])
                    print("Vous venez de supprimer votre sauvegarde")
            else:
                print("Votre ancienne sauvegarde a été conservé")
            init_vars_game(liste, ens_joueur)
    else:
        init_vars_game(liste, ens_joueur)

    while verifier(ens_joueur):
        one_loop_of_game(0, liste, ens_joueur)

    #fin de la partie, affichage vainqueur(s)/scores
    print("La partie est finie, Les scores sont de:")
    maxim = list()
    for nom in liste:
        maxim += [nom]
    maxi = [maxim[0]]
    print("-"+str(maxim[0]), ":", total(maxim[0], ens_joueur), "points")
    for nom in maxim[1:]:
        print("-"+str(nom), ":", total(nom, ens_joueur), "points")
        if total(nom, ens_joueur) > total(maxi[0], ens_joueur):
            maxi = [nom]
        elif total(nom, ens_joueur) == total(maxi[0], ens_joueur):
            maxi += [nom]
    if len(maxi) == 1:
        print("Le gagnant est donc", maxi[0])
    elif len(maxi) > 1:
        print("Les gagnants sont donc ", end = "")
        for i in range(len(maxi)-1):
            print(maxi[i]+", ", end = "")
        print(maxi[len(maxi)-1]+".")

    #sauvegarde des scores
    with open("save","rb") as fiche:
        mon_d = pickle.Unpickler(fiche)
        rec = mon_d.load()
    rec["nombre de parties"] += 1
    for nom in ens_joueur:
        if not(nom in rec):
            rec[nom] = dict()
        rec[nom]["partie "+str(rec["nombre de parties"])] = total(nom, ens_joueur)
        rec["moyenne"][nom] = moyenne(nom, rec)
        rec["ecart-type"][nom] = ecart_type(nom, rec)
    with open("save","wb") as fiche:
        mon_pickler = pickle.Pickler(fiche)
        mon_pickler.dump(rec)

def init_scores():
    answer = input("Etes-vous sûr de vouloir réinitialiser les scores? ")
    if ("oui" in answer) or ("yes" in answer) or answer == "o":
        with open("save","wb") as op:
            mo = pickle.Pickler(op)
            mo.dump({"nombre de parties" : 0, "moyenne" : {}, "ecart-type" : {}})
            print("Vous venez de réinitialiser la sauvegarde des scores.")
    else:
        print("Vous n'avez pas réinitialisé les scores !")


def main():
    # print("\n/!\\ Le système de sauvegarde bug, il n'écrase pas les parties pour la nouvelle sauvegarde\n")
    # exit(1)

    while True:
        print()
        choix = str(input("Que voulez vous faire? "))

        #partie jeu
        if ("jeu" in choix) or ("joue" in choix) or ("parti" in choix):
            game()

        #partie réinitialisation des scores
        elif ("0" in choix) or ("initial" in choix):
            init_scores()

        #partie affichage des scores
        elif "score" in choix:
            with open("save","rb") as fiche:
                mon_d=pickle.Unpickler(fiche)
                rec=mon_d.load()
                if len(rec)==3:
                    print("Il n'y a encore aucun score enregistré pour le moment")
                else:
                    imprimer_score(rec)

        #partie aide
        elif "aide" in choix:
            print("\t[GESTIONNAIRE DE PARTIE DE YAMS]\nDans ce programme, il vous est possible de lancer une nouvelle partie comme une déjà enregistrée (attention, vous ne pouvez garder qu'une seule partie enregistrée), d'afficher la table des scores passés, de réinitialiser cette table, ou de quitter tout simplement le programme.")

        #partie quitter le programme
        elif ("quitte" in choix) or ("stop" in choix) or ("arret" in choix) or ("sop" in choix):
            exit()

        else:
            print("Je ne vous ai pas compris, pourriez-vous reformuler?")


main()
