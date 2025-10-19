class Plateau:
    """
    0 = vide
    1 = case ciblé sans bateaus
    2 = case avec bateau
    3 = case touché avec bateau
    x=ligne
    y=colonne"""

    def __init__(self):
        self.plateau = []
        self.liste_bateau_restant = []

    def creation_plateau(self):
        #Fonction qui créer le plateau vide, en 10x10, rempli de 0
        self.plateau = []
        for i in range(10):
            ligne = []
            for j in range(10):
                ligne.append(0)
            self.plateau.append(ligne)
        return self.plateau

    def afficher_plateau(self, afficher_1, afficher_2):
        #Fonction qui affiche dans la console le plateau
        print("  0 1 2 3 4 5 6 7 8 9")
        for numero_ligne, ligne_plateau in enumerate(self.plateau):
            ligne_print = str(numero_ligne) + ' '
            for case in ligne_plateau:
                if case==0:
                    ligne_print += '· '
                elif case == 1:
                    if afficher_1:
                        ligne_print += 'X '
                    else:
                        ligne_print += '· '
                elif case == 2:
                    if afficher_2:
                        ligne_print += '□ '
                    else:
                        ligne_print += '· '
                elif case == 3:
                    ligne_print += '☒ '
            print(ligne_print + str(numero_ligne))
        print("  0 1 2 3 4 5 6 7 8 9")

    def modifier_case(self, coordonees_x, coordonees_y, valeur):
        self.plateau[coordonees_x][coordonees_y] = valeur
   
    
    def cible_case(self, coordonees_x, coordonees_y):
        # retourne True si est un bateau est présent
        if self.plateau[coordonees_x][coordonees_y]==2:
            return True
        else:
            return False

      
    def is_possible_cible(self, coordonees_x, coordonees_y):
        # retourne True si c'est possible de cibler la case
        if coordonees_x>9 or coordonees_x<0 or coordonees_y>9 or coordonees_y<0:
            return False
        else:
            if self.plateau[coordonees_x][coordonees_y]==1 or self.plateau[coordonees_x][coordonees_y]==3:
                return False
            else :
                return True


    def ajouter_bateau(self, coordonees_x, coordonees_y, orientation, taille): #orientation = 0 -> droite, 1 -> bas
        #Ajoute renvoir True ou False si l'ajout est possible, et si oui l'ajoute
        
        #Renvoie False si le bateau est en dehors de l'écran ou si il y a déja un bateau sur le terrain

        if coordonees_x <0 or coordonees_x >9 or coordonees_y<0 or coordonees_y>9:
            return False 

        if orientation == 0:
            for i in range(coordonees_y, coordonees_y+taille):
                if i >= 10  :   
                    return False
                if self.plateau[coordonees_x][i] != 0:
                    return False
        elif orientation == 1:
            for i in range(coordonees_x, coordonees_x+taille):
                if i >= 10:
                    return False
                if self.plateau[i][coordonees_y] != 0:
                
                    return False
        else:
            return False
        

        self.liste_bateau_restant.append([taille,[]])
        #modifie la matrice plateau avec les bonnes valeurs
        if orientation == 1:
            for i in range(coordonees_x, coordonees_x+taille):
                self.modifier_case(i, coordonees_y, 2)
                self.liste_bateau_restant[-1][1].append([i, coordonees_y])
                

        elif orientation == 0:
            for i in range(coordonees_y, coordonees_y+taille):
                self.modifier_case(coordonees_x, i, 2)
                self.liste_bateau_restant[-1][1].append([coordonees_x, i])

        return True

    def enlever_case_bateau(self, coordonees_x, coordonees_y):
        #remove dans la liste des bateaux la case corespondante
        #renvoie la taille initial du bateau et la taille après le ciblage 
        for index_bateau, bateau in enumerate(self.liste_bateau_restant):
            for coordonees_case_bateau in bateau[1]:
                if coordonees_case_bateau == [coordonees_x, coordonees_y]:
                    self.liste_bateau_restant[index_bateau][1].remove(coordonees_case_bateau)
                    return (bateau[0], len(bateau[1]))
    
    def nb_bateau_restant(self):
        #renvoie le nombre de bateau de bateau encore en vie
        output = 0
        for bateau in self.liste_bateau_restant:
            if len(bateau[1]) != 0:
                output += 1
        return output


plateau_joueur1 = Plateau()
plateau_joueur2 = Plateau()

plateau_joueur1.creation_plateau()
plateau_joueur2.creation_plateau()

tour = 1

#Demande le nombre de bateaux de taille 1 à 6 à poser dans le plateau
dico_bateaux_a_poser = {}
for i in range(1,6):  
    dico_bateaux_a_poser[i] = int(input(f"Combien de bateaux de taille {i} voulez vous ajouter ? "))
liste_bateaux_a_poser = []
for clef in dico_bateaux_a_poser:
    for i in range(dico_bateaux_a_poser[clef]):
        liste_bateaux_a_poser.append(clef)


#Bloucle qui demande au deux joueurs de donner la position de leurs bateau à poser sur leur plateau respéctif, tout en 
for joueur in [1,2]:
    for indice, taille in enumerate(liste_bateaux_a_poser):
        if joueur == 1:
            plateau_joueur1.afficher_plateau(True, True)
        else:
            plateau_joueur2.afficher_plateau(True, True)
        bonne_position_bateau = False  
        while not bonne_position_bateau:
            coordonnee_case_x = int(input(f"Dans quel numéro de ligne veut tu placer le coin de ton bateau n° {indice+1} de taille {taille} ? : "))
            coordonnee_case_y = int(input(f"Dans quel numéro de colonne veut tu placer le coin de ton bateau n° {indice+1} de taille {taille} ? : "))
            orientation = int(input("Dans quel orientation ? (0 = droite, 1 = bas)"))
            if joueur == 1:
                bonne_position_bateau = plateau_joueur1.ajouter_bateau(coordonnee_case_x, coordonnee_case_y, orientation, taille)
                plateau_joueur1.afficher_plateau(True, True)
            else:
                bonne_position_bateau = plateau_joueur2.ajouter_bateau(coordonnee_case_x, coordonnee_case_y, orientation, taille)
   
                plateau_joueur2.afficher_plateau(True, True)
"""
tour = 1
while 1:
    print("\n","Ton propre plateau qui sert à viser l'adversaire")
    if tour == 1:
        plateau_joueur1.afficher_plateau()
        print("\n" , "Ton plateau avec tes bateaux")
        plateau_joueur1_allier.afficher_plateau()

        bonne_position_cible = False
        while not bonne_position_cible:
            coordonner_case_x = input("Dans quel numero de ligne veux tu cibler ?")
            coordonner_case_y = input("Dans quel numero de colonne veux tu cibler ?")
            bonne_position_cible = plateau_joueur2_allier.is_possible_cible(coordonner_case_x, coordonner_case_y)

        if plateau_joueur2_allier.cible_case == True:
            plateau_joueur2_allier.enlever_case_bateau(coordonner_case_x, coordonner_case_y)
            plateau_joueur2_allier.modifier_case(coordonner_case_x, coordonner_case_y, 3)
            plateau_joueur1_adversaire.modifier_case(coordonner_case_x, coordonner_case_y, 3)
        else:
            plateau_joueur2_allier.modifier_case(coordonner_case_x, coordonner_case_y, 1)
            plateau_joueur1_adversaire.modifier_case(coordonner_case_x, coordonner_case_y, 1)
"""
