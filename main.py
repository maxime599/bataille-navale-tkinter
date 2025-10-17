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

    def afficher_plateau(self):
        #Fonction qui affiche dans la console le plateau
        print("  0 1 2 3 4 5 6 7 8 9")
        for numero_ligne, ligne_plateau in enumerate(self.plateau):
            ligne_print = str(numero_ligne) + ' '
            for case in ligne_plateau:
                if case==0:
                    ligne_print += '· '
                elif case == 1:
                    ligne_print += 'X '
                elif case == 2:
                    ligne_print += '□ '
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
                if self.plateau[i][coordonees_y] != 0:
                    return False
        elif orientation == 1:
            for i in range(coordonees_x, coordonees_x+taille):
                if i >= 10:
                    return False
                if self.plateau[coordonees_x][i] != 0:
                    return False
        else:
            return False
        

        self.liste_bateau_restant.append([taille,[]])
        #modifie la matrice plateau avec les bonnes valeurs
        if orientation == 0:
            for i in range(coordonees_x, coordonees_x+taille):
                plateau.modifier_case(i, coordonees_y, 2)
                self.liste_bateau_restant[-1][1].append([i, coordonees_y])
                

        elif orientation == 1:
            for i in range(coordonees_y, coordonees_y+taille):
                plateau.modifier_case(coordonees_x, i, 2)
                self.liste_bateau_restant[-1][1].append([coordonees_x, i])

        return True

    def nb_vie_bateau(self, coordonees_x, coordonees_y):
        #renvoie la taille initial du bateau et la taille après le ciblage 
        for index_bateau, bateau in enumerate(self.liste_bateau_restant):
            for coordonees_case_bateau in bateau[1]:
                if coordonees_case_bateau == [coordonees_x, coordonees_y]:
                    self.liste_bateau_restant[index_bateau][1].remove(coordonees_case_bateau)
                    return (bateau[0], len(bateau[1]))



plateau = Plateau()
plateau.creation_plateau()
plateau.afficher_plateau()

plateau.ajouter_bateau(7, 2, 1, 2)
plateau.afficher_plateau()
print(plateau.liste_bateau_restant)

print(plateau.nb_vie_bateau(7 , 2))
print(plateau.liste_bateau_restant)
