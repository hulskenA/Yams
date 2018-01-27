import pickle
colonne=["ordre","sec","libre"]
coups=["1","2","3","4","5","6","st","Bonus","full","moins","plus","carre","suite","yam"]
print("Ce programme est très simple d'utilisation, parlez lui comme à un être humain et si il ne vous comprend pas, il vous le fera savoir. Il est aussi possible si besoin de lui demander de l'aide à tout moment pour qu'il vous explique ce qu'il vous est possible de faire. Sur ce bonne chance pour vos futures parties.")

def affiche_partie(nom,ens_joueur):
    print("\n"+nom.upper(),':')
    i=''
    for c in colonne:
        while len(c+i)<25:
            i+=' '
        print("|"+c.upper()+i,end="")
    print("")
    for coup in coups:
        for c in colonne:
            e=''
            r=''
            while len(coup+e)<15:
                e+=" "
            while len(str(ens_joueur[nom][c][coup])+r)<10:
                r+=" "
            print(("|"+coup+e+str(ens_joueur[nom][c][coup])+r),end="")
        print('')

def sous_total(nom,ens_joueur):
    for c in colonne:
        st=0
        for i in range(1,7):
            if not((ens_joueur[nom][c][str(i)])=="XXXX"):
                st+=int(ens_joueur[nom][c][str(i)])
        ens_joueur[nom][c]['st']=st

def total(nom,ens_joueur):
    tot=0
    for c in colonne:
        for coup in coups:
            if not((ens_joueur[nom][c][coup])=="XXXX") and coup!='st':
                tot+=int(ens_joueur[nom][c][coup])
    return tot


def verifier(ens_joueur):
    for nom in ens_joueur:
        for c in colonne:
            for coup in coups:
                if 'XXXX'==ens_joueur[nom][c][coup]:
                    return True
    return False

def moyenne(nom,rec):
    moy=0
    for i in rec[nom]:
        moy+=rec[nom][i]
    return moy/len(rec[nom])

def ecart_type(nom,rec):
    ec=0
    for i in rec[nom]:
        ec+=(rec[nom][i]-rec['moyenne'][nom])**2
    return (ec/len(rec[nom]))**0.5

def imprimer_score(rec):
    print("          |",end="")
    for nom in rec:
        if nom!='moyenne' and nom!='nombre de parties' and nom!='ecart-type':
            print(' '+nom+' |',end='')
    print("")
    for i in range(1,rec['nombre de parties']+1):
        e=''
        while len(e)+9<12:
            e+=' '
        print('partie'+str(i)+e+'|',end="")
        for nom in rec:
            if nom!='moyenne' and nom!='nombre de parties' and nom!='ecart-type' and ('partie '+str(i) in rec[nom]):
                f=''
                while len(f+str(rec[nom]['partie '+str(i)]))<len(nom)+2:
                    f+=' '
                print(f+str(rec[nom]['partie '+str(i)])+"|",end="")
            elif nom!='moyenne' and nom!='nombre de parties' and nom!='ecart-type' and not('partie '+str(i) in rec[nom]):
                f=''
                while len(f+"X")<len(nom)+2:
                    f+=' '
                print(f+"X|",end="")
        print('')
    print("moyenne   |",end='')
    for nom in rec:
        if nom!='moyenne' and nom!='nombre de parties' and nom!='ecart-type':
            f=''
            while len(f+str(int(rec['moyenne'][nom])))<len(nom)+2:
                f+=' '
            print(f+str(int(rec['moyenne'][nom]))+'|',end="")
    print('')
    print("ecart-type|",end="")
    for nom in rec:
        if nom!='moyenne' and nom!='nombre de parties' and nom!='ecart-type':
            f=''
            while len(f+str(int(rec['ecart-type'][nom])))<len(nom)+2:
                f+=' '
            print(f+str(int(rec['ecart-type'][nom]))+'|',end='')

def main ():
    print("")
    choix=str(input("Que voulez vous faire? "))
    while True:
        ens_joueur=dict()
        liste=list()
        #partie jeu
        if ('jeu' in choix) or ('joue' in choix) or ('parti' in choix):
            with open('partie_enr','rb') as fiche:
                mo=pickle.Unpickler(fiche)
                l=mo.load()
                taille=len(l)
            #si une partie est enregistrée
            if taille>0:
                tp=input("Voulez vous reprendre la partie enregistré? ")
                if "oui" in tp:
                    with open('partie_enr','rb') as fiche:
                        mo=pickle.Unpickler(fiche)
                        rep=mo.load()
                        print("Vous venez de reprendre une partie enregistrée avec comme joueurs:")
                    ind=rep[2]
                    liste+=rep[1]
                    ens_joueur=rep[0]
                    with open('partie_enr','wb') as fiche:
                        mo=pickle.Pickler(fiche)
                        mo.dump([])
                    for nom in liste:
                        print('-'+nom,)
                    for i in range(ind,len(liste)):
                        affiche_partie(liste[i],ens_joueur)
                        print("TOTAL:",total(liste[i],ens_joueur))
                        case=str(input("Où voulez vous mettre vos points? ")).split(' ')
                        #mauvaise entrée
                        while not(((case[0] in colonne) and (case[1] in coups)) or ('abandon' in case[0]) or ('stop' in case[0]) or ('arret' in case[0]) or ('quitte' in case[0])):
                            if not('aide' in case[0]):
                                print("Non ce n'est pas possible connard réessaye encore...")
                            else:
                                print("Il est ici simplement possible de sélectionner une case en me donnant son nom ou de quitter la partie en cours.")
                            case=str(input("Où voulez vous mettre vos points? ")).split(' ')
                        #abandon de la partie
                        if ('abandon' in case[0]) or ('stop' in case[0]) or ('arret' in case[0]) or ('quitte' in case[0]):
                            enr=input("Voulez vous enregistrer la partie en cours? ")
                            if ('oui' in enr) or ('yes' in enr):
                                with open('partie_enr','wb') as fiche:
                                    mo=pickle.Pickler(fiche)
                                    mo.dump([ens_joueur,liste,liste.index])
                                    print("la partie a été enregistré.")
                            else :
                                print("La partie n'a pas été enregistré.")
                            main()
                            return None
                        ens_joueur[liste[i]][case[0]][case[1]]=input("Combien avez vous fait? ")
                        sous_total(liste[i],ens_joueur)
                        for c in colonne:
                            if ens_joueur[liste[i]][c]['st']>=60:
                                ens_joueur[nom][c]['Bonus']=20
            case=['']
            inp=str(input("Qui sont les joueurs qui vont jouer? ")).split(" ")
            for nom in inp:
                if nom!='':
                    ens_joueur[nom]=dict()
                    liste+=[nom]
                    for c in colonne:
                        ens_joueur[nom][c]=dict()
                        for coup in coups:
                            ens_joueur[nom][c][coup]='XXXX'
            while verifier(ens_joueur) and (not('abandon' in case[0]) or not('stop' in case[0]) or not('arret' in case[0])):
                for f in liste:
                    affiche_partie(f,ens_joueur)
                    print("TOTAL:",total(f,ens_joueur))
                    case=str(input("Où voulez vous mettre vos points? ")).split(' ')
                    #mauvaise entrée
                    while not(((case[0] in colonne) and (case[1] in coups)) or ('abandon' in case[0]) or ('stop' in case[0]) or ('arret' in case[0]) or ('quitte' in case[0])):
                        if not('aide' in case[0]):
                            print("Non ce n'est pas possible connard réessaye encore...")
                        else:
                            print("Il est ici simplement possible de sélectionner une case en me donnant son nom ou de quitter la partie en cours.")
                        case=str(input("Où voulez vous mettre vos points? ")).split(' ')
                        #abandon de la partie
                    if ('abandon' in case[0]) or ('stop' in case[0]) or ('arret' in case[0]) or ('quitte' in case[0]):
                        enr=input("Voulez vous enregistrer la partie en cours? ")
                        if ('oui' in enr) or ('yes' in enr):
                            with open('partie_enr','wb') as fiche:
                                mo=pickle.Pickler(fiche)
                                mo.dump([ens_joueur,liste,liste.index(f)])
                                print("la partie a été enregistré.")
                        else :
                            print("La partie n'a pas été enregistré.")
                        main()
                        return None
                    ens_joueur[f][case[0]][case[1]]=input("Combien avez vous fait? ")
                    sous_total(f,ens_joueur)
                    for c in colonne:
                        if ens_joueur[f][c]['st']>=60:
                            ens_joueur[nom][c]['Bonus']=20
            #fin de la partie, affichage vainqueur(s)/scores
            print("La partie est finie, Les scores sont de:")
            maxim=list()
            for nom in liste:
                maxim+=[nom]
            maxi=[maxim[0]]
            print("-"+str(maxim[0]),':',total(maxim[0],ens_joueur),"points")
            for nom in maxim[1:]:
                print("-"+str(nom),":",total(nom,ens_joueur),"points")
                if total(nom,ens_joueur)>total(maxi[0],ens_joueur):
                    maxi=[nom]
                elif total(nom,ens_joueur)==total(maxi[0],ens_joueur):
                    maxi+=[nom]
            if len(maxi)==1:
                print("Le gagnant est donc",maxi[0])
            elif len(maxi)>1:
                print("Les gagnants sont donc ",end='')
                for i in range(len(maxi)-1):
                    print(maxi[i]+', ',end="")
                print(maxi[len(maxi)-1]+'.')
            #sauvegarde des scores
            with open('save','rb') as fiche:
                mon_d=pickle.Unpickler(fiche)
                rec=mon_d.load()
            rec['nombre de parties']+=1
            for nom in ens_joueur:
                if not(nom in rec):
                    rec[nom]=dict()
                rec[nom]['partie '+str(rec['nombre de parties'])]=total(nom,ens_joueur)
                rec['moyenne'][nom]=moyenne(nom,rec)
                rec['ecart-type'][nom]=ecart_type(nom,rec)
            with open('save','wb') as fiche:
                mon_pickler = pickle.Pickler(fiche)
                mon_pickler.dump(rec)
        #partie réinitialisation des scores
        elif ('0' in choix) or ('initial' in choix):
            dem=input('Etes-vous sûr de vouloir réinitialiser les scores? ')
            if ('oui' in str(dem)) or ('yes' in str(dem)):
                with open('save','wb')as op:
                    mo=pickle.Pickler(op)
                    mo.dump({'nombre de parties':0,'moyenne':{},'ecart-type':{}})
                    print('Vous venez de réinitialiser la sauvegarde des scores.')
            elif not('oui' in str(dem)) or ('yes' in str(dem)):
                print("Vous n'avez pas réinitialisé les scores")
        #partie affichage des scores
        elif 'score' in choix:
            with open('save','rb') as fiche:
                mon_d=pickle.Unpickler(fiche)
                rec=mon_d.load()
                if len(rec)==3:
                    print("Il n'y a encore aucun score enregistré pour le moment")
                else:
                    imprimer_score(rec)
        #partie aide
        elif 'aide' in choix:
            print("Dans ce programme, il vous est possible de lancer une nouvelle partie comme une déjà enregistrée (attention, vous ne pouvez garder qu'une seule partie enregistrée), d'afficher la table des scores passés, de réinitialiser cette table, ou de quitter tout simplement le programme.")
        #partie quitter le programme
        elif ('quitte' in choix) or ('stop' in choix) or ('arret' in choix):
            break
        print('')
        choix=str(input("Que voulez vous faire? "))

main()
