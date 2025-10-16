class Plateau:
    """
    0 = vide
    1 = case ciblé sans bateaus
    2 = case avec bateau
    3 = case touché avec bateau
    """
    # x=ligne
    # y=colonne
    def __init__(self):
        self.plateau = []

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
   
    # retourne True si est un bateau est présent
    def cible_case(self, coordonees_x, coordonees_y):
        if self.plateau[coordonees_x][coordonees_y]==2:
            return True
        else:
            return False

    # retourne True si c'est possible de cibler la case  
    def is_possible_cible(self, coordonees_x, coordonees_y):
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
        

        if orientation == 0:
            for i in range(coordonees_x, coordonees_x+taille):
                plateau.modifier_case(i, coordonees_y, 2)
        elif orientation == 1:
            for i in range(coordonees_y, coordonees_y+taille):
                plateau.modifier_case(coordonees_x, i, 2)

        return True


plateau = Plateau()
plateau.creation_plateau()
plateau.afficher_plateau()

plateau.ajouter_bateau(7, 2, 1, 2)
plateau.afficher_plateau()