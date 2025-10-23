from tkinter import *
import copy
from PIL import Image, ImageTk


root_created = False

class Plateau:
    """
    0 = vide                            blanc
    1 = case ciblé sans bateaus         viollet
    2 = case avec bateau                noir
    3 = case touché avec bateau         vert
    4 = case avec bateau prévisualisé   gris
    5 = bateau coulé
    x=ligne 
    y=colonne"""

    def __init__(self):
        self.plateau = []
        self.liste_bateau_restant = []
        self.liste_bateau_total = []
        self.liste_bateaux_a_poser = []

    def creation_plateau(self):
        #Fonction qui créer le plateau vide, en 10x10, rempli de 0
        self.plateau = []
        for i in range(10):
            ligne = []
            for j in range(10):
                ligne.append(Case(i, j, 0))
            self.plateau.append(ligne)
        return self.plateau

    def afficher_plateau(self, afficher_1, afficher_2):
        #Fonction qui affiche dans la console le plateau
        print("  0 1 2 3 4 5 6 7 8 9")
        for numero_ligne, ligne_plateau in enumerate(self.plateau):
            ligne_print = str(numero_ligne) + ' '
            for case in ligne_plateau:
                if case.type == 0:
                    ligne_print += '· '
                elif case.type == 1:
                    if afficher_1:
                        ligne_print += 'X '
                    else:
                        ligne_print += '· '
                elif case.type == 2:
                    if afficher_2:
                        ligne_print += '□ '
                    else:
                        ligne_print += '· '
                elif case.type == 3:
                    ligne_print += '☒ '
            print(ligne_print + str(numero_ligne))
        print("  0 1 2 3 4 5 6 7 8 9")

    def modifier_case(self, coordonees_x, coordonees_y, valeur, taille_bateau = None, position_sur_bateau = None, orientation_bateau = None):
        self.plateau[coordonees_x][coordonees_y].coordonees_x = coordonees_x
        self.plateau[coordonees_x][coordonees_y].coordonees_y = coordonees_y
        self.plateau[coordonees_x][coordonees_y].type = valeur
        
        if taille_bateau != None:
            self.plateau[coordonees_x][coordonees_y].taille_bateau = taille_bateau
        if position_sur_bateau != None:
            self.plateau[coordonees_x][coordonees_y].position_sur_bateau = position_sur_bateau
        if orientation_bateau != None:
            self.plateau[coordonees_x][coordonees_y].orientation_bateau = orientation_bateau
           
    
    def cible_case(self, coordonees_x, coordonees_y):
        # retourne True si est un bateau est présent
        if self.plateau[coordonees_x][coordonees_y].type == 2 or self.plateau[coordonees_x][coordonees_y].type == 5:
            return True
        else:
            return False

      
    def is_possible_cible(self, coordonees_x, coordonees_y):
        # retourne True si c'est possible de cibler la case
        if coordonees_x>9 or coordonees_x<0 or coordonees_y>9 or coordonees_y<0:
            return False
        else:
            if self.plateau[coordonees_x][coordonees_y].type == 1 or self.plateau[coordonees_x][coordonees_y].type == 3 or self.plateau[coordonees_x][coordonees_y].type == 5:
                return False
            else :
                return True


    def ajouter_bateau(self, coordonees_x, coordonees_y, orientation, taille, can_touch, juste_test_possible = False): #orientation = 0 -> droite, 1 -> bas
        #Ajoute renvoir True ou False si l'ajout est possible, et si oui l'ajoute
        
        #Renvoie False si le bateau est en dehors de l'écran ou si il y a déja un bateau sur le terrain

        if coordonees_x <0 or coordonees_x >9 or coordonees_y<0 or coordonees_y>9:
            return False 

        if orientation == 0:
            if not can_touch:
                #on regarde si les trois cases à droite et à gauche du bateau sont déja pleines ou non
                for i in range(-1, 2):
                    try:
                        if self.plateau[coordonees_x+i][coordonees_y-1].type != 0:
                            return False
                    except:
                        pass
                    
                    try:
                        if self.plateau[coordonees_x+i][coordonees_y+taille].type != 0:
                            return False
                    except:
                        pass

            for i in range(coordonees_y, coordonees_y+taille):
                if i >= 10  :   
                    return False
                if self.plateau[coordonees_x][i].type != 0:
                    return False
                if not can_touch:
                    try:
                        if self.plateau[coordonees_x-1][i].type != 0:
                            return False
                    except:
                        pass
                    
                    try:
                        if self.plateau[coordonees_x+1][i].type != 0:
                            return False
                    except:
                        pass

        elif orientation == 1:
            #on regarde si les trois cases en haut et en bas du bateau sont déja pleines ou non
            for i in range(-1, 2):
                    try:
                        if self.plateau[coordonees_x-1][coordonees_y+i].type != 0:
                            return False
                    except:
                        pass
                    
                    try:
                        if self.plateau[coordonees_x+taille][coordonees_y+i].type != 0:
                            return False
                    except:
                        pass
            for i in range(coordonees_x, coordonees_x+taille):
                if i >= 10:
                    return False
                if self.plateau[i][coordonees_y].type != 0:
                    return False
                if not can_touch:
                    try:
                        if self.plateau[i][coordonees_y-1].type != 0:
                            return False
                    except:
                        pass
                    
                    try:
                        if self.plateau[i][coordonees_y+1].type != 0:
                            return False
                    except:
                        pass
        else:
            return False
        
        if juste_test_possible == False:
            self.liste_bateau_restant.append([taille,[]])
            #modifie la matrice plateau avec les bonnes valeurs
            if orientation == 1:
                for index, i in enumerate(range(coordonees_x, coordonees_x+taille)):
                    self.modifier_case(i, coordonees_y, 2, taille, index, orientation)
                    self.liste_bateau_restant[-1][1].append([i, coordonees_y])
                    

            elif orientation == 0:
                for index, i in enumerate(range(coordonees_y, coordonees_y+taille)):
                    self.modifier_case(coordonees_x, i, 2, taille, index, orientation)
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

        #Permet de créer un fenêtre principal et un fenêtre secondaire pour éviter les bug de gestion de la souris
        global root_created
        if not root_created:
            self.fenetre = Tk()
            root_created = True
        else:
            self.fenetre = Toplevel()
            
        self.fenetre.title(nom)

        self._clicked = BooleanVar()
        self.croix_id = None



        #Ajout des textes sur la fenêtre
        canvas_num_gauche = Canvas(self.fenetre, width=476, height=40, background='#f0f0f0')
        canvas_num_gauche.grid(row=0, column=0, columnspan=10, pady=(15, 0), padx=10)

        for i in range(1, 11):
            x_pos = (i - 0.5) * 47.6
            canvas_num_gauche.create_text(x_pos, 20, text=str(i), font=("Courier", 30), anchor='center')

        canvas_lettres = Canvas(self.fenetre, width=40, height=476, background='#f0f0f0')
        canvas_lettres.grid(row=1, column=10, rowspan=10, padx=5)

        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        for i, k in enumerate(alphabet):
            y_pos = (i + 0.5) * 47.6
            canvas_lettres.create_text(20, y_pos, text=k, font=("Courier", 30), anchor='center')

        canvas_num_droite = Canvas(self.fenetre, width=476, height=40, background='#f0f0f0')
        canvas_num_droite.grid(row=0, column=11, columnspan=10, pady=(15, 0), padx=10)

        for i in range(1, 11):
            x_pos = (i - 0.5) * 47.6
            canvas_num_droite.create_text(x_pos, 20, text=str(i), font=("Courier", 30), anchor='center')     
        
        self.canva_gauche = Canvas(self.fenetre, width=476, height=476, background='#589ddc')
        self.canva_gauche.grid(row=1, column=0, columnspan=10, rowspan=10, padx=10, pady=(0, 5) )

        self.canva_droite = Canvas(self.fenetre, width=476, height=476, background='green')
        self.canva_droite.grid(row=1, column=11, columnspan=10, rowspan=10, padx=10, pady=(0, 5))

        self.phrase = Label(self.fenetre, text="Sert à viser l'adversaire", font=("Courier", 12))
        self.phrase.grid(row=11, column=0, columnspan=10)
        self.phrase = Label(self.fenetre, text="Sert à voir vos bateaux touchés", font=("Courier", 12))
        self.phrase.grid(row=11, column=11, columnspan=10)
        
        
        #Gestion des différentes images
        self.images = []
        self.taille_case = 45
        self.img_bleu = PhotoImage(file='images/bleu.png', master=self.fenetre)
        
        self.img_gris = PhotoImage(file='images/gris.png', master=self.fenetre)
        self.img_croix = PhotoImage(file='images/croix.png', master=self.fenetre)
        self.img_cible = PhotoImage(file='images/cible.png', master=self.fenetre)
        self.img_touche = PhotoImage(file='images/touché.png', master=self.fenetre)

        self.img_bateau_1 = PhotoImage(file='Images/Bateaux/1.png', master=self.fenetre)
        self.img_bateau_2 = PhotoImage(file='Images/Bateaux/2.png', master=self.fenetre)
        self.img_bateau_3 = PhotoImage(file='Images/Bateaux/3.png', master=self.fenetre)
        self.img_bateau_4 = PhotoImage(file='Images/Bateaux/4.png', master=self.fenetre)
        self.img_bateau_5 = PhotoImage(file='Images/Bateaux/5.png', master=self.fenetre)

        self.liste_img_bateaux = [self.img_bateau_1, self.img_bateau_2, self.img_bateau_3, self.img_bateau_4, self.img_bateau_5]

    def afficher_plateau(self, plateau, afficher_1, afficher_2, position_canva):
        
        #permet de créer ces deux listes seulement une fois, la première fois que afficher_plateau() est appelée.
        if not hasattr(self, 'images_gauche'):
            self.images_gauche = []
        if not hasattr(self, 'images_droite'):
            self.images_droite = []

        if position_canva == 'gauche':
            self.canva_gauche.delete("all")
            # on réinitialise uniquement la liste gauche
            self.images_gauche = []
        else:
            self.canva_droite.delete("all")
            # on réinitialise uniquement la liste droite
            self.images_droite = []

        for index_ligne, ligne in enumerate(plateau):
            for index_colonne, colonne in enumerate(ligne):
                x = index_colonne * self.taille_case + index_colonne * 3 + 1
                y = index_ligne * self.taille_case + index_ligne * 3 + 1


                # Affiche toujours l'image bleue en fond
                if position_canva == 'gauche':
                    self.canva_gauche.create_image(x, y, image=self.img_bleu, anchor=NW)
                else:
                    self.canva_droite.create_image(x, y, image=self.img_bleu, anchor=NW)
                if colonne.type == 0:
                    image = self.img_bleu
                elif colonne.type == 1:
                    image = self.img_cible if afficher_1 else self.img_bleu
                elif (not afficher_2) and (colonne.type == 2):
                    image = self.img_bleu

                elif (colonne.type == 2 and afficher_2) or (colonne.type == 3 and position_canva != 'gauche') or colonne.type == 5:
                    img_original_pil = Image.open(f'Images/Bateaux/{colonne.taille_bateau}.png')
                    if colonne.type == 5:
                        img_original_pil = img_original_pil.convert("RGBA")
                    x1 = (colonne.position_sur_bateau)*45+(colonne.position_sur_bateau-1)*3
                    x2 = x1 + 48  
                    image_cropped = img_original_pil.crop((x1, 0, x2, 45))
                    
                    if colonne.orientation_bateau == 1:
                        image_cropped = image_cropped = image_cropped.rotate(-90, expand=True)
                    
                    if colonne.type == 5:
                        alpha = image_cropped.split()[-1]
                        alpha = alpha.point(lambda p: p * 0.5)  # 0.5 = 50% transparent
                        image_cropped.putalpha(alpha)

                    image = ImageTk.PhotoImage(image_cropped, master=self.fenetre)
                

                elif colonne.type == 3:
                    image = self.img_touche

                
                else:  # colonne.type == 4
                    image = self.img_gris
                

                if position_canva == 'gauche':
                    self.images_gauche.append(image)
                    self.canva_gauche.create_image(x, y, image=image, anchor=NW)
                else:
                    self.images_droite.append(image)
                    self.canva_droite.create_image(x, y, image=image, anchor=NW)
                    if colonne.type == 3:
                        self.canva_droite.create_image(x, y, image=self.img_touche, anchor=NW)
                

    def click_to_case(self, coordonnee_click_x, coordonnee_click_y):
        #Retourne les coordonnées de la case cliquée
        return (int(coordonnee_click_y/(self.taille_case+3)), int(coordonnee_click_x/(self.taille_case+3)))

    def attendre_click_case(self):
        #Attend qu'un clic de souris soit effectué sur la fenêtre, puis retourne les coordonnées de la case cliquée.      
        
        self.click_coord = (0,0)
        self._clicked.set(False)
        self.fenetre.bind("<Button-1>", self.on_click)
        self.fenetre.wait_variable(self._clicked) 
        return self.click_coord  # retourne un tuple (x_case, y_case)
    
    def on_click(self, event):
        #Fonction qui récupère les coordonnées du click de la souris
        x_pixel = event.x
        y_pixel = event.y

        self.click_coord = self.click_to_case(x_pixel, y_pixel)
        self.fenetre.unbind("<Button-1>")
        self._clicked.set(True)

    def afficher_previsualisation(self, plateau, x, y, orientation, taille, position_canva, can_touch):
        
        if plateau.ajouter_bateau(x, y, orientation, taille, can_touch, True) == False:
            possible = False
        else:
            possible = True

        # Efface uniquement la prévisualisation précédente
        if position_canva == 'gauche':
            self.canva_gauche.delete("preview")
        else:
            self.canva_droite.delete("preview")

        for i in range(taille):
            if orientation == 0:
                case_x, case_y = x, y + i
            else:
                case_x, case_y = x + i, y
            if 0 <= case_x < 10 and 0 <= case_y < 10:
                img_path = f'Images/Bateaux/{taille}.png'
                img_pil = Image.open(img_path).convert("RGBA")
                x1 = i * self.taille_case + i * 3
                x2 = x1 + self.taille_case + 3
                image_cropped = img_pil.crop((x1, 0, x2, self.taille_case))
                if orientation == 1:
                    image_cropped = image_cropped.rotate(-90, expand=True)
                # Semi-transparence
                alpha = image_cropped.split()[-1]
                alpha = alpha.point(lambda p: p * 0.5)
                image_cropped.putalpha(alpha)
                # Si placement impossible, applique filtre rouge
                if not possible:
                    # Crée un overlay rouge semi-transparent
                    rouge = Image.new("RGBA", image_cropped.size, (255, 0, 0, 120))
                    image_cropped = Image.alpha_composite(image_cropped, rouge)
                image = ImageTk.PhotoImage(image_cropped, master=self.fenetre)
                if not hasattr(self, 'preview_images'):
                    self.preview_images = []
                self.preview_images.append(image)
                px = case_y * self.taille_case + case_y * 3 + 1
                py = case_x * self.taille_case + case_x * 3 + 1
                if position_canva == 'gauche':
                    self.canva_gauche.create_image(px, py, image=image, anchor=NW, tags="preview")
                else:
                    self.canva_droite.create_image(px, py, image=image, anchor=NW, tags="preview")
    
    def afficher_croix(self, event):
        # Supprime l'ancienne croix si elle existe
        if self.croix_id is not None:
            self.canva_gauche.delete(self.croix_id)
        # Affiche la croix à la position de la souris
        self.croix_id = self.canva_gauche.create_image(event.x, event.y, image=self.img_cible)

    def cacher_croix(self, event):
        if self.croix_id is not None:
            self.canva_gauche.delete(self.croix_id)
            self.croix_id = None


class Case:
    def __init__(self,coordonnee_x, coordonnee_y, type, taille_bateau = None, position_sur_bateau = None, orientation_bateau = None):
        self.coordonnee_x = coordonnee_x
        self.coordonnee_y = coordonnee_y
        self.type = type
        self.taille_bateau = taille_bateau
        self.position_sur_bateau = position_sur_bateau
        self.orientation_bateau = orientation_bateau

        if self.type == 3 or self.type == 4:
            self.is_beateau = True
        else:
            self.is_beateau = False


        


def on_mouvement(event, fenetre, plateau, orientation, taille, position_canva, can_touch):
    x_case, y_case = fenetre.click_to_case(event.x, event.y)
    fenetre.afficher_previsualisation(plateau, x_case, y_case, orientation, taille, position_canva, can_touch)

def on_molette(event, fenetre, plateau, orientation, taille, position_canva, can_touch):
    orientation[0] = 1 - orientation[0]  # alterne entre 0 et 1
    x_case, y_case = fenetre.click_to_case(event.x, event.y)
    fenetre.afficher_previsualisation(plateau, x_case, y_case, orientation[0], taille, position_canva, can_touch)

def on_clique_droit(event, plateau, fenetre, canva_placement, text_ids):

    
    x_case, y_case = fenetre.click_to_case(event.x, event.y)    #Converti les coordonnée de px en coordonnée de cases
    if plateau.plateau[x_case][y_case].type == 2:   #On regarde si la case cliquée est bien un bateau
        bateau_touche = [0,[0,0]]

        #On parcourt la liste de bateau sur le plateau pour trouver les autres cases du bateau
        for bateau in plateau.liste_bateau_restant: 
            for case in bateau[1]:
                if case == [x_case, y_case]:
                    bateau_touche = bateau
        taille_bateau = bateau_touche[0]

        #On convertit les cases de bateaux en cases vides
        for case_a_supprimer in bateau_touche[1]:
            plateau.plateau[case_a_supprimer[0]][case_a_supprimer[1]].type = 0

        fenetre.afficher_plateau(plateau.plateau, True, True, 'droit') #Mise à jour de l'affichage
        plateau.liste_bateaux_a_poser.append(taille_bateau)            #Mise à jour de la liste des bateaux à poser

        index = taille_bateau - 1
        canva_placement.itemconfig(text_ids[index], text='× ' + str(plateau.liste_bateaux_a_poser.count(taille_bateau))) #Mise à jour de l'affichage du nombre restant de bateaux à poser
        return taille_bateau
    return None

def recuperer_taille_bateaux():

    #On test si les valeurs rentrées par l'utilisateur sont valides
    try:
        nb_bateaux_1 = int(form_nb_bateaux_1.get())
        nb_bateaux_2 = int(form_nb_bateaux_2.get())
        nb_bateaux_3 = int(form_nb_bateaux_3.get())
        nb_bateaux_4 = int(form_nb_bateaux_4.get())
        nb_bateaux_5 = int(form_nb_bateaux_5.get())
    #inon on met des valeurs par défaut
    except:
        nb_bateaux_1 = 0
        nb_bateaux_2 = 1
        nb_bateaux_3 = 2
        nb_bateaux_4 = 1
        nb_bateaux_5 = 1


    

    return {1 : nb_bateaux_1, 2 : nb_bateaux_2, 3 : nb_bateaux_3, 4 : nb_bateaux_4, 5 : nb_bateaux_5}

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



plateau_joueur1 = Plateau()
plateau_joueur2 = Plateau()

plateau_joueur1.creation_plateau()
plateau_joueur2.creation_plateau()

fenetre1 = IU("joueur 1")
fenetre1.afficher_plateau(plateau_joueur1.plateau, True, True, 'gauche')
fenetre1.afficher_plateau(plateau_joueur2.plateau, True, True, 'droit')
fenetre2 = IU("Joueur 2")
fenetre2.afficher_plateau(plateau_joueur1.plateau, True, True, 'gauche')
fenetre2.afficher_plateau(plateau_joueur2.plateau, True, True, 'droit')

#Demande le nombre de bateaux de taille 1 à 6 à poser dans le plateau
"""dico_bateaux_a_poser = {}
for i in range(1,6):  
    dico_bateaux_a_poser[i] = int(input(f"Combien de bateaux de taille {i} voulez vous ajouter ? "))"""

#On met des valeurs par défaut si le joueur ferme la fenêtre
print(dico_bateaux_a_poser)
if dico_bateaux_a_poser == {}:
    plateau_joueur1.liste_bateaux_a_poser = [2,3,3,4,5]
    plateau_joueur2.liste_bateaux_a_poser = [2,3,3,4,5]
    dico_bateaux_a_poser = {1:0,2:1,3:2,4:1,5:1}
else:
    liste_bateaux_a_poser = []
    for clef in dico_bateaux_a_poser:
        for i in range(dico_bateaux_a_poser[clef]):
            plateau_joueur1.liste_bateaux_a_poser.append(clef)
            plateau_joueur2.liste_bateaux_a_poser.append(clef)
    print(liste_bateaux_a_poser)



text_placement_bateau_fenetre_1 = Label(fenetre1.fenetre, text="C'est à vous de poser les bateaux", font=("Courier", 15),wraplength=280,justify='center')
text_placement_bateau_fenetre_1.grid(row=1,column=22, padx=(0,3))
text_placement_bateau_fenetre_2 = Label(fenetre2.fenetre, text="C'est à l'adversaire de poser ces bateaux",font=("Courier", 15),wraplength=280,justify='center')
text_placement_bateau_fenetre_2.grid(row=1,column=22, padx=(0,3))

canva_placement_bateaux_fenetre1 = Canvas(fenetre1.fenetre, width=260, height=220, background="#f8f9fb", highlightthickness=0)
canva_placement_bateaux_fenetre1.grid(row=2, column=22, padx=6, pady=6)

canva_placement_bateaux_fenetre1.create_rectangle(4, 4, 256, 216, outline="#cfcfcf", width=2, fill="#ffffff")
canva_placement_bateaux_fenetre1.create_text(130, 18, text='Vos bateaux à poser', fill="#1f2f3f", font=("Helvetica", 14, "bold"))

canva_placement_bateaux_fenetre2 = Canvas(fenetre2.fenetre, width=260, height=220, background="#f8f9fb", highlightthickness=0)
canva_placement_bateaux_fenetre2.grid(row=2, column=22, padx=6, pady=6)
canva_placement_bateaux_fenetre2.create_rectangle(4, 4, 256, 216, outline="#cfcfcf", width=2, fill="#ffffff")
canva_placement_bateaux_fenetre2.create_text(130, 18, text='Vos bateaux à poser', fill="#1f2f3f", font=("Helvetica", 14, "bold"))

im_carre_bleu = PhotoImage(file='images/carre_bateau_bleu.png', master=fenetre1.fenetre)
im_carre_bleu2 = PhotoImage(file='images/carre_bateau_bleu.png', master=fenetre2.fenetre)


canva1_text_ids = []
canva2_text_ids = []
for bateau in range(5):
    y = 40 + 36 * bateau
    img_x = 20
    for i in range(0, bateau+1):
        canva_placement_bateaux_fenetre1.create_image(img_x + 14*i, y+6, image=im_carre_bleu, anchor=NW)
        canva_placement_bateaux_fenetre2.create_image(img_x + 14*i, y+6, image=im_carre_bleu2, anchor=NW)
    text_x = img_x + 14 * (bateau + 1) + 12
    tid1 = canva_placement_bateaux_fenetre1.create_text(text_x, y + 10, text='× ' + str(plateau_joueur1.liste_bateaux_a_poser.count(bateau + 1)), fill="#2b3a42", font=("Helvetica", 12), anchor='w')
    tid2 = canva_placement_bateaux_fenetre2.create_text(text_x, y + 10, text='× ' + str(plateau_joueur2.liste_bateaux_a_poser.count(bateau + 1)), fill="#2b3a42", font=("Helvetica", 12), anchor='w')
    canva1_text_ids.append(tid1)
    canva2_text_ids.append(tid2)

#Boucle qui demande au deux joueurs de donner la position de leurs bateau à poser sur leur plateau
for joueur in [1,2]:
    if joueur == 1:
        plateau_joueur1.afficher_plateau(True, True)
        fenetre1.afficher_plateau(plateau_joueur1.plateau, True, True, 'droit')
        liste_bateaux_a_poser = plateau_joueur1.liste_bateaux_a_poser
    else:
        plateau_joueur2.afficher_plateau(True, True)
        fenetre2.afficher_plateau(plateau_joueur2.plateau, True, True, 'droit')
        liste_bateaux_a_poser = plateau_joueur2.liste_bateaux_a_poser


    indice = 0
    while indice < len(liste_bateaux_a_poser):
        taille = liste_bateaux_a_poser[indice]
        bonne_position_bateau = False  
        bateau_supprime = False
        while not bonne_position_bateau:
            #coordonnee_case_x = int(input(f"Dans quel numéro de ligne veut tu placer le coin de ton bateau n° {indice+1} de taille {taille} ? : "))
            #coordonnee_case_y = int(input(f"Dans quel numéro de colonne veut tu placer le coin de ton bateau n° {indice+1} de taille {taille} ? : "))

            #orientation = int(input("Dans quel orientation ? (0 = droite, 1 = bas)"))

            orientation = [0]

            if joueur == 1:
                fenetre1.canva_droite.bind("<Motion>", lambda event: on_mouvement(event, fenetre1, plateau_joueur1, orientation[0], taille, 'droite', option_can_touch))
                fenetre1.canva_droite.bind("<MouseWheel>", lambda event: on_molette(event, fenetre1, plateau_joueur1, orientation, taille, 'droite', option_can_touch))
                fenetre1.canva_droite.bind("<Button-3>", lambda event: on_clique_droit(event, plateau_joueur1, fenetre1, canva_placement_bateaux_fenetre1, canva1_text_ids))

            else:
                fenetre2.canva_droite.bind("<Motion>", lambda event: on_mouvement(event, fenetre2, plateau_joueur2, orientation[0], taille, 'droite', option_can_touch))
                fenetre2.canva_droite.bind("<MouseWheel>", lambda event: on_molette(event, fenetre2, plateau_joueur2, orientation, taille, 'droite', option_can_touch))
                fenetre2.canva_droite.bind("<Button-3>", lambda event: on_clique_droit(event, plateau_joueur2, fenetre2, canva_placement_bateaux_fenetre2, canva2_text_ids))

            if joueur == 1:
                coordonnee_case = fenetre1.attendre_click_case()
            else:
                coordonnee_case = fenetre2.attendre_click_case()

            fenetre1.canva_droite.unbind("<Motion>")
            fenetre1.canva_droite.unbind("<MouseWheel>")
            fenetre1.canva_droite.unbind("<Button-3>")
            fenetre2.canva_droite.unbind("<Motion>")
            fenetre2.canva_droite.unbind("<MouseWheel>")
            fenetre2.canva_droite.unbind("<Button-3>")

            coordonnee_case_x = coordonnee_case[0]
            coordonnee_case_y = coordonnee_case[1]

            if joueur == 1:
                bonne_position_bateau = plateau_joueur1.ajouter_bateau(coordonnee_case_x, coordonnee_case_y, orientation[0], taille, option_can_touch)
                plateau_joueur1.afficher_plateau(True, True)
                fenetre1.afficher_plateau(plateau_joueur1.plateau, True, True, 'droite')
                if bonne_position_bateau == True:
                    liste_bateaux_a_poser.remove(taille)
                    index = taille - 1
                    canva_placement_bateaux_fenetre1.itemconfig(canva1_text_ids[index], text='× ' + str(liste_bateaux_a_poser.count(taille)))
                num_joueur = 2
            else:
                bonne_position_bateau = plateau_joueur2.ajouter_bateau(coordonnee_case_x, coordonnee_case_y, orientation[0], taille, option_can_touch)   
                plateau_joueur2.afficher_plateau(True, True)
                fenetre2.afficher_plateau(plateau_joueur2.plateau, True, True, 'droite')
                if bonne_position_bateau == True:
                    liste_bateaux_a_poser.remove(taille)
                    index = taille - 1
                    canva_placement_bateaux_fenetre2.itemconfig(canva2_text_ids[index], text='× ' + str(liste_bateaux_a_poser.count(taille)))

    text_placement_bateau_fenetre_1.configure(text="C'est à l'adversaire de poser ces bateaux")
    text_placement_bateau_fenetre_2.configure(text="C'est à vous de poser les bateaux")

plateau_joueur1.liste_bateau_total = copy.deepcopy(plateau_joueur1.liste_bateau_restant)
plateau_joueur2.liste_bateau_total = copy.deepcopy(plateau_joueur2.liste_bateau_restant)

text_placement_bateau_fenetre_1.destroy()
text_placement_bateau_fenetre_2.destroy()
canva_placement_bateaux_fenetre1.destroy()
canva_placement_bateaux_fenetre2.destroy()

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
        #coordonner_case_y = int(input("Dans quel numero de colonne veux tu cibler ? "))

        if joueur == 1:
            fenetre1.canva_gauche.config(cursor="none")
            fenetre1.canva_gauche.bind("<Motion>", fenetre1.afficher_croix)
            fenetre1.canva_gauche.bind("<Leave>", fenetre1.cacher_croix)
            coordonnee_case = fenetre1.attendre_click_case()
            fenetre1.canva_gauche.config(cursor="arrow")
            fenetre1.canva_gauche.unbind("<Motion>")
            fenetre1.canva_gauche.unbind("<Leave>")
        else:
            fenetre2.canva_gauche.config(cursor="none")
            fenetre2.canva_gauche.bind("<Motion>", fenetre2.afficher_croix)
            fenetre2.canva_gauche.bind("<Leave>", fenetre2.cacher_croix)
            coordonnee_case = fenetre2.attendre_click_case()
            fenetre2.canva_gauche.config(cursor="arrow")
            fenetre2.canva_gauche.unbind("<Motion>")
            fenetre2.canva_gauche.unbind("<Leave>")
            
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

                index_bateau_touche = 0
                for index_bateau, bateau in enumerate(plateau_joueur2.liste_bateau_total):
                    for case in bateau[1]:
                        if case == [coordonnee_case_x, coordonnee_case_y]:
                            index_bateau_touche = index_bateau
                print(plateau_joueur2.liste_bateau_total[index_bateau_touche][1])
                for case in plateau_joueur2.liste_bateau_total[index_bateau_touche][1]:
                    
                    plateau_joueur2.modifier_case(case[0], case[1], 5)
                    
                    
                                

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

                
                index_bateau_touche = 0
                for index_bateau, bateau in enumerate(plateau_joueur1.liste_bateau_total):
                    for case in bateau[1]:
                        if case == [coordonnee_case_x, coordonnee_case_y]:
                            index_bateau_touche = index_bateau

                print(plateau_joueur1.liste_bateau_total[index_bateau_touche][1])
                for case in plateau_joueur1.liste_bateau_total[index_bateau_touche][1]:
                    plateau_joueur1.modifier_case(case[0], case[1], 5)
                    


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