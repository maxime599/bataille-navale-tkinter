from tkinter import *
from time import *

root_created = False

class Plateau:
    """
    0 = vide                            blanc
    1 = case ciblé sans bateaus         viollet
    2 = case avec bateau                noir
    3 = case touché avec bateau         vert
    4 = case avec bateau prévisualisé   gris
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


    def ajouter_bateau(self, coordonees_x, coordonees_y, orientation, taille, can_touch): #orientation = 0 -> droite, 1 -> bas
        #Ajoute renvoir True ou False si l'ajout est possible, et si oui l'ajoute
        
        #Renvoie False si le bateau est en dehors de l'écran ou si il y a déja un bateau sur le terrain

        if coordonees_x <0 or coordonees_x >9 or coordonees_y<0 or coordonees_y>9:
            return False 

        if orientation == 0:
            if not can_touch:
                #on regarde si les trois cases à droite et à gauche du bateau sont déja pleines ou non
                for i in range(-1, 2):
                    try:
                        if self.plateau[coordonees_x+i][coordonees_y-1] != 0:
                            return False
                    except:
                        pass
                    
                    try:
                        if self.plateau[coordonees_x+i][coordonees_y+taille] != 0:
                            return False
                    except:
                        pass

            for i in range(coordonees_y, coordonees_y+taille):
                if i >= 10  :   
                    return False
                if self.plateau[coordonees_x][i] != 0:
                    return False
                if not can_touch:
                    try:
                        if self.plateau[coordonees_x-1][i] != 0:
                            return False
                    except:
                        pass
                    
                    try:
                        if self.plateau[coordonees_x+1][i] != 0:
                            return False
                    except:
                        pass

        elif orientation == 1:
            #on regarde si les trois cases en haut et en bas du bateau sont déja pleines ou non
            for i in range(-1, 2):
                    try:
                        if self.plateau[coordonees_x-1][coordonees_y+i] != 0:
                            return False
                    except:
                        pass
                    
                    try:
                        if self.plateau[coordonees_x+taille][coordonees_y+i] != 0:
                            return False
                    except:
                        pass
            for i in range(coordonees_x, coordonees_x+taille):
                if i >= 10:
                    return False
                if self.plateau[i][coordonees_y] != 0:
                    return False
                if not can_touch:
                    try:
                        if self.plateau[i][coordonees_y-1] != 0:
                            return False
                    except:
                        pass
                    
                    try:
                        if self.plateau[i][coordonees_y+1] != 0:
                            return False
                    except:
                        pass
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
        return (0,0)

    def nb_bateau_restant(self):
        #renvoie le nombre de bateau de bateau encore en vie
        output = 0
        for bateau in self.liste_bateau_restant:
            if len(bateau[1]) != 0:
                output += 1
        return output


class IU:
    def __init__(self, nom):
        global root_created
        if not root_created:
            self.fenetre = Tk()
            root_created = True
        else:
            self.fenetre = Toplevel()
        self.fenetre.title(nom)

        self._clicked = BooleanVar()

        for i in range (1,11):
            self.chiffre_plateau = Label(self.fenetre, text=str(i), font=("Courier", 30))
            if i == 10:
                padx = 0
            else:
                padx = 8
            self.chiffre_plateau.grid(row=0, column=i-1, padx=(padx,0), pady=(15, 0))

        alphabet=["A","B","C","D","E","F","G","H","I","J"]
        for i,k in enumerate(alphabet):
            self.chiffre_plateau = Label(self.fenetre, text=str(k), font=("Courier", 30))
            if i == 9:
                pady = 10
            else:
                pady = 0
            self.chiffre_plateau.grid(row=i+1, column=10, padx=5, pady=(0,pady))

        for i in range (1,11):
            self.chiffre_plateau = Label(self.fenetre, text=str(i), font=("Courier", 30))
            if i == 10:
                padx = 0
            else:
                padx = 8
            self.chiffre_plateau.grid(row=0, column=i+10, padx=(padx,0), pady=(15, 0))

        
        
        self.canva_gauche = Canvas(self.fenetre, width=476, height=476, background='red')
        self.canva_gauche.grid(row=1, column=0, columnspan=10, rowspan=10, padx=10, pady=(0, 5) )

        self.canva_droite = Canvas(self.fenetre, width=476, height=476, background='green')
        self.canva_droite.grid(row=1, column=11, columnspan=10, rowspan=10, padx=10, pady=(0, 5))

        self.phrase = Label(self.fenetre, text="Sert à viser l'adversaire", font=("Courier", 12))
        self.phrase.grid(row=11, column=0, columnspan=10)
        self.phrase = Label(self.fenetre, text="Sert à voir vos bateaux touchés", font=("Courier", 12))
        self.phrase.grid(row=11, column=11, columnspan=10)
        
        self.images = []

        self.taille_case = 45

        self.img_blanc = PhotoImage(file='images/blanc.png', master=self.fenetre)
        self.img_viollet = PhotoImage(file='images/viollet.png', master=self.fenetre)
        self.img_noir = PhotoImage(file='images/noir.png', master=self.fenetre)
        self.img_vert = PhotoImage(file='images/vert.png', master=self.fenetre)
        self.img_gris = PhotoImage(file='images/gris.png', master=self.fenetre)

    def afficher_plateau(self, plateau, afficher_1, afficher_2, position_canva):
        self.images = []
        if position_canva == 'gauche':
            self.canva_gauche.delete("all")
        else:
            self.canva_droite.delete("all")
        for index_ligne, ligne in enumerate(plateau):
            for index_colonne, colonne in enumerate(ligne):
                if colonne == 0:
                    image = self.img_blanc
                elif colonne == 1:
                    image = self.img_viollet if afficher_1 else self.img_blanc
                elif colonne == 2:
                    image = self.img_noir if afficher_2 else self.img_blanc
                elif colonne == 3:
                    image = self.img_vert
                else:  # colonne == 4
                    image = self.img_gris
                self.images.append(image)
                if position_canva == 'gauche':
                    self.canva_gauche.create_image(index_colonne*self.taille_case+index_colonne*3+1, index_ligne*self.taille_case+index_ligne*3+1, image=image, anchor=NW)
                else:
                    self.canva_droite.create_image(index_colonne*self.taille_case+index_colonne*3+1, index_ligne*self.taille_case+index_ligne*3+1, image=image, anchor=NW)

    def click_to_case(self, coordonnee_click_x, coordonnee_click_y):
        return (int(coordonnee_click_y/(self.taille_case+3)), int(coordonnee_click_x/(self.taille_case+3)))

    def attendre_click_case(self):
        self.click_coord = (0,0)
        self._clicked.set(False)
        self.fenetre.bind("<Button-1>", self.on_click)
        self.fenetre.wait_variable(self._clicked) 
        return self.click_coord  # retourne un tuple (x_case, y_case)
    
    def on_click(self, event):
        x_pixel = event.x
        y_pixel = event.y

        self.click_coord = self.click_to_case(x_pixel, y_pixel)
        self.fenetre.unbind("<Button-1>")
        self._clicked.set(True)


    def afficher_previsualisation(self, plateau, x, y, orientation, taille, position_canva):
        plateau_preview = [row[:] for row in plateau]
        # Place le bateau en gris (valeur 4) si possible
        if orientation == 0:
            for i in range(taille):
                if 0 <= y + i < 10:
                    plateau_preview[x][y + i] = 4
        else:
            for i in range(taille):
                if 0 <= x + i < 10:
                    plateau_preview[x + i][y] = 4
        self.afficher_plateau(plateau_preview, True, True, position_canva)


def on_motion(event, fenetre, plateau, orientation, taille, position_canva):
    x_case, y_case = fenetre.click_to_case(event.x, event.y)
    fenetre.afficher_previsualisation(plateau, x_case, y_case, orientation, taille, position_canva)

def on_wheel(event, fenetre, plateau, orientation, taille, position_canva):
    orientation[0] = 1 - orientation[0]  # alterne entre 0 et 1
    x_case, y_case = fenetre.click_to_case(event.x, event.y)
    fenetre.afficher_previsualisation(plateau, x_case, y_case, orientation[0], taille, position_canva)


def recuperer_taille_bateaux():
    return {1 : int(form_nb_bateaux_1.get()), 2 : int(form_nb_bateaux_2.get()), 3 : int(form_nb_bateaux_3.get()), 4 : int(form_nb_bateaux_4.get()), 5 : int(form_nb_bateaux_5.get()), }

def valider_et_quitter():
    global dico_bateaux_a_poser
    dico_bateaux_a_poser = recuperer_taille_bateaux()
    fenetre_nb_bateau.destroy()


option_can_touch = False

dico_bateaux_a_poser = {}
fenetre_nb_bateau = Tk()
for i in range(5):
    label_bateaux_1 = Label(fenetre_nb_bateau, text=f'Nombre de bateau de taille {i+1}')
    label_bateaux_1.grid(row = i, column = 0, padx = 3, pady = 3)


form_nb_bateaux_1 = Entry(fenetre_nb_bateau, textvariable=StringVar())
form_nb_bateaux_1.grid(row = 0, column = 1, padx = 3, pady = 3)
form_nb_bateaux_2 = Entry(fenetre_nb_bateau, textvariable=StringVar())
form_nb_bateaux_2.grid(row = 1, column = 1, padx = 3, pady = 3)
form_nb_bateaux_3 = Entry(fenetre_nb_bateau, textvariable=StringVar())
form_nb_bateaux_3.grid(row = 2, column = 1, padx = 3, pady = 3)
form_nb_bateaux_4 = Entry(fenetre_nb_bateau, textvariable=StringVar())
form_nb_bateaux_4.grid(row = 3, column = 1, padx = 3, pady = 3)
form_nb_bateaux_5 = Entry(fenetre_nb_bateau, textvariable=StringVar())
form_nb_bateaux_5.grid(row = 4, column = 1, padx = 3, pady = 3)

bouton_valider = Button(fenetre_nb_bateau, text='Valider', command=valider_et_quitter)
bouton_valider.grid(row = 6, column = 0, padx = 3, pady = 3)
mainloop()

#Demande le nombre de bateaux de taille 1 à 6 à poser dans le plateau
"""dico_bateaux_a_poser = {}
for i in range(1,6):  
    dico_bateaux_a_poser[i] = int(input(f"Combien de bateaux de taille {i} voulez vous ajouter ? "))"""
liste_bateaux_a_poser = []
for clef in dico_bateaux_a_poser:
    for i in range(dico_bateaux_a_poser[clef]):
        liste_bateaux_a_poser.append(clef)


plateau_joueur1 = Plateau()
plateau_joueur2 = Plateau()

plateau_joueur1.creation_plateau()
plateau_joueur2.creation_plateau()

fenetre1 = IU("joueur 1")
fenetre1.afficher_plateau(plateau_joueur1.plateau, True, True, 'gauche')
fenetre1.afficher_plateau(plateau_joueur2.plateau, True, True, 'droit')
fenetre2 = IU("fenetre 2")
fenetre2.afficher_plateau(plateau_joueur1.plateau, True, True, 'gauche')
fenetre2.afficher_plateau(plateau_joueur2.plateau, True, True, 'droit')





#Bloucle qui demande au deux joueurs de donner la position de leurs bateau à poser sur leur plateau respéctif, tout en 
for joueur in [1,2]:
    if joueur == 1:
        plateau_joueur1.afficher_plateau(True, True)
        fenetre1.afficher_plateau(plateau_joueur1.plateau, True, True, 'droit')
    else:
        plateau_joueur2.afficher_plateau(True, True)
        fenetre2.afficher_plateau(plateau_joueur2.plateau, True, True, 'droit')
    for indice, taille in enumerate(liste_bateaux_a_poser):

        bonne_position_bateau = False  
        while not bonne_position_bateau:
            #coordonnee_case_x = int(input(f"Dans quel numéro de ligne veut tu placer le coin de ton bateau n° {indice+1} de taille {taille} ? : "))
            #coordonnee_case_y = int(input(f"Dans quel numéro de colonne veut tu placer le coin de ton bateau n° {indice+1} de taille {taille} ? : "))

            #orientation = int(input("Dans quel orientation ? (0 = droite, 1 = bas)"))

            orientation = [0]



            if joueur == 1:
                fenetre1.canva_droite.bind("<Motion>", lambda event: on_motion(event, fenetre1, plateau_joueur1.plateau, orientation[0], taille, 'droite'))
                fenetre1.canva_droite.bind("<MouseWheel>", lambda event: on_wheel(event, fenetre1, plateau_joueur1.plateau, orientation, taille, 'droite'))
            else:
                fenetre2.canva_droite.bind("<Motion>", lambda event: on_motion(event, fenetre2, plateau_joueur2.plateau, orientation[0], taille, 'droite'))
                fenetre2.canva_droite.bind("<MouseWheel>", lambda event: on_wheel(event, fenetre2, plateau_joueur2.plateau, orientation, taille, 'droite'))

            if joueur == 1:
                coordonnee_case = fenetre1.attendre_click_case()
            else:
                coordonnee_case = fenetre2.attendre_click_case()

            fenetre1.canva_droite.unbind("<Motion>")
            fenetre1.canva_droite.unbind("<MouseWheel>")
            fenetre2.canva_droite.unbind("<Motion>")
            fenetre2.canva_droite.unbind("<MouseWheel>")

            coordonnee_case_x = coordonnee_case[0]
            coordonnee_case_y = coordonnee_case[1]

            if joueur == 1:
                bonne_position_bateau = plateau_joueur1.ajouter_bateau(coordonnee_case_x, coordonnee_case_y, orientation[0], taille, option_can_touch)
                plateau_joueur1.afficher_plateau(True, True)
                fenetre1.afficher_plateau(plateau_joueur1.plateau, True, True, 'droite')
            else:
                bonne_position_bateau = plateau_joueur2.ajouter_bateau(coordonnee_case_x, coordonnee_case_y, orientation[0], taille, option_can_touch)   
                plateau_joueur2.afficher_plateau(True, True)
                fenetre2.afficher_plateau(plateau_joueur2.plateau, True, True, 'droite')


joueur = 1
fin_du_jeux = False
coordonnee_case_x, coordonnee_case_y = 0,0
while  not fin_du_jeux:
    # affiche les plateaux
    print("\n","Ton propre plateau qui sert à viser l'adversaire")
    if joueur == 1:
        plateau_joueur2.afficher_plateau(True, False)
        print("\n" , "Ton plateau avec tes bateaux")
        plateau_joueur1.afficher_plateau(True, True)

    if joueur == 2:
        plateau_joueur1.afficher_plateau(True, False)
        print("\n" , "Ton plateau avec tes bateaux")
        plateau_joueur2.afficher_plateau(True, True)
        
    
    fenetre1.afficher_plateau(plateau_joueur2.plateau, True, False, 'gauche')
    fenetre1.afficher_plateau(plateau_joueur1.plateau, True, True, 'droite')
    fenetre2.afficher_plateau(plateau_joueur1.plateau, True, False, 'gauche')
    fenetre2.afficher_plateau(plateau_joueur2.plateau, True, True, 'droite')


    print(f"C'est au joueur du joueur {joueur} de jouer")

    # demande la case à ciblé
    bonne_position_cible = False
    while not bonne_position_cible:
        #coordonner_case_x = int(input("Dans quel numero de ligne veux tu cibler ?"))
        #coordonner_case_y = int(input("Dans quel numero de colonne veux tu cibler ?"))

        if joueur == 1:
            coordonnee_case = fenetre1.attendre_click_case()
        else:
            coordonnee_case = fenetre2.attendre_click_case()
            
        coordonnee_case_x = coordonnee_case[0]
        coordonnee_case_y = coordonnee_case[1]

        if joueur == 1:
            bonne_position_cible = plateau_joueur2.is_possible_cible(coordonnee_case_x, coordonnee_case_y)
        else:
            bonne_position_cible = plateau_joueur1.is_possible_cible(coordonnee_case_x, coordonnee_case_y)

    # cible une case et gestion bateaux plus fin de game
    if joueur == 1:
        if plateau_joueur2.cible_case(coordonnee_case_x, coordonnee_case_y) == True: # si bateau présent
            taille_bateau_restant = plateau_joueur2.enlever_case_bateau(coordonnee_case_x, coordonnee_case_y)
            plateau_joueur2.modifier_case(coordonnee_case_x, coordonnee_case_y, 3)
            if taille_bateau_restant[1] != 0: # s'il reste des parties non découvertes du bateau trouvé
                print(f"Le bateau de taille {taille_bateau_restant[0]} a été touché il lui reste {taille_bateau_restant[1]} vie(s)")
            else: # si tout le bateau a été découvert
                nb_bateaux_restant = plateau_joueur2.nb_bateau_restant()
                print(f"Le bateau de taille {taille_bateau_restant[0]} a été coulé")
                if nb_bateaux_restant != 0: # s'il reste des bateaux
                    print(f"Il reste {nb_bateaux_restant} bateau(x) en vie")
                else: # s'il n'y a plus de bateau restant
                    print("Partie terminée, le joueur 1 a gagné")
                    fin_du_jeux = True
        else: # une case vide
            plateau_joueur2.modifier_case(coordonnee_case_x, coordonnee_case_y, 1)
            print("La case ne contient pas de bateaux")
            joueur = 2

    elif joueur == 2:
        if plateau_joueur1.cible_case(coordonnee_case_x, coordonnee_case_y) == True: # si bateau présent
            taille_bateau_restant = plateau_joueur1.enlever_case_bateau(coordonnee_case_x, coordonnee_case_y)
            plateau_joueur1.modifier_case(coordonnee_case_x, coordonnee_case_y, 3)
            if taille_bateau_restant[1] != 0: # s'il reste des parties non découvertes du bateau trouvé
                print(f"Le bateau de taille {taille_bateau_restant[0]} a été touché il lui reste {taille_bateau_restant[1]} vie(s)")
            else: # si tout le bateau a été découvert
                nb_bateaux_restant = plateau_joueur1.nb_bateau_restant()
                print(f"Le bateau de taille {taille_bateau_restant[0]} a été coulé")
                if nb_bateaux_restant != 0: # s'il reste des bateaux
                    print(f"Il reste {nb_bateaux_restant} bateau(x) en vie")
                else: # s'il n'y a plus de bateau restant
                    print("Partie terminée, le joueur 1 a gagné")
                    fin_du_jeux = True
        else: # une case vide
            plateau_joueur1.modifier_case(coordonnee_case_x, coordonnee_case_y, 1)
            print("La case ne contient pas de bateaux")
            joueur = 1

fenetre1.afficher_plateau(plateau_joueur2.plateau, True, False, 'gauche')
fenetre1.afficher_plateau(plateau_joueur1.plateau, True, True, 'droite')
fenetre2.afficher_plateau(plateau_joueur1.plateau, True, False, 'gauche')
fenetre2.afficher_plateau(plateau_joueur2.plateau, True, True, 'droite')
mainloop()