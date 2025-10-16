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


plateau = Plateau()
plateau.creation_plateau()
plateau.afficher_plateau()