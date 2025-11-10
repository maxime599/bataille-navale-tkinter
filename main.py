from tkinter import *
import copy
from PIL import Image, ImageTk
from random import *
from time import *

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
                        if self.plateau[coordonees_x+i][coordonees_y-1].type != 0 and coordonees_x+i>=0 and coordonees_y-1>=0:
                            return False
                    except:
                        pass
                    
                    try:
                        if self.plateau[coordonees_x+i][coordonees_y+taille].type != 0 and coordonees_x+i>=0:
                            return False
                    except:
                        pass

            for i in range(coordonees_y, coordonees_y+taille):
                if i >= 10  :   
                    return False
                if self.plateau[coordonees_x][i].type != 0 and i>=0:
                    return False
                if not can_touch:
                    try:
                        if self.plateau[coordonees_x-1][i].type != 0 and coordonees_x-1>=0 and i>=0:
                            return False
                    except:
                        pass
                    
                    try:
                        if self.plateau[coordonees_x+1][i].type != 0 and i>=0:
                            return False
                    except:
                        pass

        elif orientation == 1:
            #on regarde si les trois cases en haut et en bas du bateau sont déja pleines ou non
            for i in range(-1, 2):
                try:
                    if self.plateau[coordonees_x-1][coordonees_y+i].type != 0  and coordonees_x-1>=0 and coordonees_y+i>=0:
                        return False
                except:
                    pass
                
                try:
                    if self.plateau[coordonees_x+taille][coordonees_y+i].type != 0  and coordonees_x+taille>=0 and coordonees_y+i>=0:
                        return False
                except:
                    pass
            for i in range(coordonees_x, coordonees_x+taille):
                if i >= 10:
                    return False
                if self.plateau[i][coordonees_y].type != 0  and i>=0:
                    return False
                if not can_touch:
                    try:
                        if self.plateau[i][coordonees_y-1].type != 0 and coordonees_y-1>=0 and i>=0:
                            return False
                    except:
                        pass
                    
                    try:
                        if self.plateau[i][coordonees_y+1].type != 0 and i>=0:
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
    
    def nb_bateau_restant_par_taille(self):
        #renvoie le nombre de bateau de bateau encore en vie par taille
        output = []
        for taille in range(1,6):
            output_nb = 0
            for bateau in self.liste_bateau_restant:
                if bateau[0] == taille:
                    if len(bateau[1]) != 0:
                        output_nb += 1
            output.append(output_nb)
        return output

    def nb_bateau_restant_a_pose_par_taille(self):
        #renvoie le nombre de bateau à poser par taille
        output = []
        for taille in range(1,6):
            output_nb = self.liste_bateaux_a_poser.count(taille)
            output.append(output_nb)
        return output

    def pose_bateaux_aleatoire(self, can_touch):
        for taille in self.liste_bateaux_a_poser:
            good_position = False
            while not good_position:
                good_position = self.ajouter_bateau(randint(0,9), randint(0,9), randint(0,1), taille, can_touch, False)

    def coup_aléatoire(self, can_touch):
        bon_coup = False
        coordonnee_coup_x = 0
        coordonnee_coup_y = 0
        while not bon_coup:
            coordonnee_coup_x = randint(0,9)
            coordonnee_coup_y = randint(0,9)
            bon_coup = self.is_possible_cible(coordonnee_coup_x, coordonnee_coup_y)
            if not can_touch: #si les bateaux ne peuvent pas se toucher, alors on exclut la case si elle est à coté d'un bateau coulé
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if 0 <= coordonnee_coup_x + x <= 9 and 0 <= coordonnee_coup_y + y <= 9:
                            if self.plateau[coordonnee_coup_x + x][coordonnee_coup_y + y].type == 5:
                                bon_coup = False
        return (coordonnee_coup_x, coordonnee_coup_y)

    def coup_IA(self, can_touch):
        for index_ligne, ligne in enumerate(self.plateau):
            for index_colonne, case in enumerate(ligne):
                if case.type == 3: #Si on detecte une case précedement touchée
                    liste_cases_touched_autour = []
                    liste_cases_autour_valides = []
                    #on compte combien il y des cases touchées autour et de cases que l'on peut cibler
                    for coordonnee_cases_autour in [[index_ligne-1, index_colonne], [index_ligne, index_colonne - 1], [index_ligne + 1, index_colonne], [index_ligne, index_colonne + 1]]:
                        if 0 <= coordonnee_cases_autour[0] <= 9 and 0 <= coordonnee_cases_autour[1] <= 9:
                            if self.plateau[coordonnee_cases_autour[0]][coordonnee_cases_autour[1]].type == 3:
                                liste_cases_touched_autour.append(coordonnee_cases_autour)
                            else:
                                print('ici')
                                if self.is_possible_cible(coordonnee_cases_autour[0], coordonnee_cases_autour[1]):
                                    print('case valide')
                                    liste_cases_autour_valides.append(coordonnee_cases_autour)
                    if len(liste_cases_touched_autour) == 0:#si il n'y a pas de cases touchée autour, alors on cible une case aléatoir parmit celle que l'on peur cibler
                        return choice(liste_cases_autour_valides)
                    
                    elif len(liste_cases_touched_autour) == 1: #si il y a une autre case touchée autour, alors on tente de viser celle à l'opposé
                        if liste_cases_touched_autour[0] == [index_ligne-1, index_colonne] and self.is_possible_cible(index_ligne+1, index_colonne):
                            return (index_ligne+1, index_colonne)
                        elif liste_cases_touched_autour[0] == [index_ligne, index_colonne - 1] and self.is_possible_cible(index_ligne, index_colonne + 1):
                            return (index_ligne, index_colonne + 1)
                        elif liste_cases_touched_autour[0] == [index_ligne+1, index_colonne] and self.is_possible_cible(index_ligne-1, index_colonne):
                            return (index_ligne-1, index_colonne)
                        elif liste_cases_touched_autour[0] == [index_ligne, index_colonne + 1] and self.is_possible_cible(index_ligne, index_colonne - 1):
                            return (index_ligne, index_colonne - 1)
                        
                    elif len(liste_cases_touched_autour) == 3: #si il y a 3 cases touchés autour, alors on cible la 4eme
                        for element in [[index_ligne-1, index_colonne], [index_ligne, index_colonne - 1], [index_ligne + 1, index_colonne], [index_ligne, index_colonne + 1]]:
                            if element not in liste_cases_touched_autour:
                                return element
        return self.coup_aléatoire(can_touch)

class UI_game:
    def __init__(self, nom, joueur):

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
        self.canva_bind = 'droite' #definie quel canva il faut regarder pour le clique gauche
        self.canva_cacher = False
        self.joueur = joueur

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
        self.croix_fond_rouge = PhotoImage(file='images/croix_fond_rouge.png', master=self.fenetre)
        self.img_cible = PhotoImage(file='images/cible.png', master=self.fenetre)
        self.img_touche = PhotoImage(file='images/touché.png', master=self.fenetre)

        self.img_bateau_1 = PhotoImage(file='Images/Bateaux/1.png', master=self.fenetre)
        self.img_bateau_2 = PhotoImage(file='Images/Bateaux/2.png', master=self.fenetre)
        self.img_bateau_3 = PhotoImage(file='Images/Bateaux/3.png', master=self.fenetre)
        self.img_bateau_4 = PhotoImage(file='Images/Bateaux/4.png', master=self.fenetre)
        self.img_bateau_5 = PhotoImage(file='Images/Bateaux/5.png', master=self.fenetre)

        self.im_carre_bleu = PhotoImage(file="images/carre_bateau_bleu.png", master=self.fenetre)
        self.im_carre_rouge = PhotoImage(file="images/carre_bateau_rouge.png", master=self.fenetre)

        self.liste_img_bateaux = [self.img_bateau_1, self.img_bateau_2, self.img_bateau_3, self.img_bateau_4, self.img_bateau_5]

        self.titres = []
        self.canva_ids = []
        self.canva_text_ids = []

    def afficher_plateau(self, plateau, afficher_1, afficher_2, position_canva, afficher_croix):
        
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
                if afficher_croix:
                    for case_to_check_x in range(-1,2):
                        for case_to_check_y in range(-1,2):
                            if 0 <= (index_ligne + case_to_check_x) <= 9 and 0 <= (index_colonne + case_to_check_y) <= 9:
                                if (case_to_check_x, case_to_check_y) != (0,0) and plateau[index_ligne + case_to_check_x][index_colonne + case_to_check_y].type == 2:
                                    image = self.croix_fond_rouge
                if colonne.type == 1:
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

                
                elif colonne.type != 0:  # colonne.type == 4
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
        if self.canva_bind == 'droite':
            self.canva_droite.bind("<Button-1>", self.on_click)
        else:
            self.canva_gauche.bind("<Button-1>", self.on_click)
            self.canva_droite.bind("<Button-1>", lambda event: self.toogle_cache_noir_droite())
        self.fenetre.wait_variable(self._clicked) 
        return self.click_coord  # retourne un tuple (x_case, y_case)
    
    def on_click(self, event):
        #Fonction qui récupère les coordonnées du click de la souris
        x_pixel = event.x
        y_pixel = event.y

        self.click_coord = self.click_to_case(x_pixel, y_pixel)
        if self.canva_bind == 'droite':
            self.canva_droite.unbind("<Button-1>")
        else:
            self.canva_gauche.unbind("<Button-1>")
            self.canva_droite.unbind("<Button-1>")
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

    def titre_information(self, parent, texte, row, column, taille):
        grand_titre = Label(parent, text=texte, font=("Helvetica", taille), wraplength=280, justify='center')
        grand_titre.grid(row=row, column=column, padx=(0,3))
        self.titres.append(grand_titre)

    def bloc_canva(self, parent, titre, text, text2, row, column, image):
        self.bloc_canva_var = Canvas(parent, width=260, height=220, background="#f8f9fb")
        self.bloc_canva_var.grid(row=row, column=column, padx=6, pady=6)
        self.bloc_canva_var.create_rectangle(4, 4, 260, 220, outline="#cfcfcf", width=2, fill="#ffffff")
        self.bloc_canva_var.create_text(130, 18, text=titre, fill="#1f2f3f", font=("Helvetica", 14, "bold"))
        self.canva_ids.append(self.bloc_canva_var)
        texte_apres_image_liste= []
        for bateau in range(5):
            y = 40 + 36 * bateau
            img_x = 20
            for i in range(0, bateau+1):
                if image == "bleu":
                    self.bloc_canva_var.create_image(img_x + 14*i, y+6, image=self.im_carre_bleu, anchor=NW)
                else:
                    self.bloc_canva_var.create_image(img_x + 14*i, y+6, image=self.im_carre_rouge, anchor=NW)
            text_x = img_x + 14 * (bateau + 1) + 12
            texte_apres_image = self.bloc_canva_var.create_text(text_x, y + 10, text=text + str(text2[bateau]), fill="#2b3a42", font=("Helvetica", 12), anchor='w')
            texte_apres_image_liste.append(texte_apres_image)
        self.canva_text_ids.append(texte_apres_image_liste)

    def vider_ids(self):
        self.canva_ids = []
        self.titres = []
        self.bloc_canva_var = []
        self.canva_text_ids = []

    def toogle_cache_noir_droite(self):
        # Ajoute un rectangle noir couvrant tout le canva de droite
        if self.canva_cacher:
            self.canva_droite.delete("cache_noir")
            if self.joueur == 1:
                self.afficher_plateau(plateau_joueur1.plateau, True, True, 'droite', False)
            else:
                self.afficher_plateau(plateau_joueur2.plateau, True, True, 'droite', False)
            self.canva_cacher = False
        else:
            self.canva_cacher = True
            self.canva_droite.create_rectangle(
                0, 0, self.canva_droite.winfo_width(), self.canva_droite.winfo_height(),
                fill="black", outline="", tags="cache_noir"
            )
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

class UI_menu:
    def __init__(self):
        self.dico_bateaux_a_poser = {}
        self.fenetre_menu = Tk()
        self.can_touch = BooleanVar(value=False)
        self.voir_cibles_adverses = BooleanVar(value=True)
        self.fenetre_menu.title("Bataille navale")
        self.widgets = []
        self.couleur_fond = "#ffffff"
        self.couleur_accent = "#42a5f5"
        self.couleur_texte = "#01579b"
        self.couleur_survol = "#90caf9"
        self.afficher_menu_principal()
        self.fenetre_menu.mainloop()

    def clear_widgets(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []

    def afficher_menu_principal(self):
        self.clear_widgets()
        self.fenetre_menu.configure(bg=self.couleur_fond)
        label_text_principal_menu = Label(self.fenetre_menu, text='Bataille navale', font=('Helvetica', 32, 'bold'), bg=self.couleur_fond, fg="#0277bd", pady=40)
        label_text_principal_menu.grid(row=0, column=0, padx=50, pady=(30, 20))
        self.widgets.append(label_text_principal_menu)
        bouton_jouer = Button(self.fenetre_menu, text='Jouer', command=self.afficher_mode_jeu, font=('Helvetica', 14, 'bold'), bg=self.couleur_accent, fg="#ffffff", activebackground=self.couleur_survol, activeforeground="#ffffff", relief='flat', bd=0, padx=40, pady=15, cursor='hand2')
        bouton_jouer.grid(row=1, column=0, padx=50, pady=15, sticky='ew')
        bouton_jouer.bind("<Enter>", lambda e: e.widget.config(bg=self.couleur_survol))
        bouton_jouer.bind("<Leave>", lambda e: e.widget.config(bg=self.couleur_accent))
        self.widgets.append(bouton_jouer)
        bouton_parametre = Button(self.fenetre_menu, text='Paramètres', command=self.afficher_parametres, font=('Helvetica', 14, 'bold'), bg=self.couleur_accent, fg="#ffffff", activebackground=self.couleur_survol, activeforeground="#ffffff", relief='flat', bd=0, padx=40, pady=15, cursor='hand2')
        bouton_parametre.grid(row=2, column=0, padx=50, pady=15, sticky='ew')
        bouton_parametre.bind("<Enter>", lambda e: e.widget.config(bg=self.couleur_survol))
        bouton_parametre.bind("<Leave>", lambda e: e.widget.config(bg=self.couleur_accent))
        self.widgets.append(bouton_parametre)
        bouton_quitter = Button(self.fenetre_menu, text='Quitter', command=self.quitter_fenetre, font=('Helvetica', 14, 'bold'), bg="#b0bec5", fg=self.couleur_texte, activebackground="#cfd8dc", activeforeground=self.couleur_texte, relief='flat', bd=0, padx=40, pady=15, cursor='hand2')
        bouton_quitter.grid(row=3, column=0, padx=50, pady=15, sticky='ew')
        bouton_quitter.bind("<Enter>", lambda e: e.widget.config(bg="#cfd8dc"))
        bouton_quitter.bind("<Leave>", lambda e: e.widget.config(bg="#b0bec5"))
        self.widgets.append(bouton_quitter)
        self.fenetre_menu.grid_columnconfigure(0, weight=1)

        """bouton_credits = Button(self.fenetre_menu, text='Crédits', command=self.afficher_credits)
        bouton_credits.grid(row=3, column=0, padx=0, pady=0)
        self.widgets.append(bouton_credits)"""

    def afficher_parametres(self):
        self.clear_widgets()
        self.fenetre_menu.configure(bg=self.couleur_fond)
        label_text_principal_parametres = Label(self.fenetre_menu, text='Paramètres', font=('Helvetica', 32, 'bold'), bg=self.couleur_fond, fg="#0277bd", pady=40)
        label_text_principal_parametres.grid(row=0, column=0, padx=50, pady=(30, 20))
        self.widgets.append(label_text_principal_parametres)
        check_can_touch = Checkbutton(self.fenetre_menu, text="Autoriser les bateaux à se toucher", variable=self.can_touch, font=('Helvetica', 12), bg=self.couleur_fond, fg=self.couleur_texte, selectcolor=self.couleur_fond, activebackground=self.couleur_fond, activeforeground=self.couleur_texte, cursor='hand2')
        check_can_touch.grid(row=1, column=0, padx=50, pady=15)
        self.widgets.append(check_can_touch)
        check_voir_cibles_adverses = Checkbutton(self.fenetre_menu, text="Voir les cibles adverses", variable=self.voir_cibles_adverses, font=('Helvetica', 12), bg=self.couleur_fond, fg=self.couleur_texte, selectcolor=self.couleur_fond, activebackground=self.couleur_fond, activeforeground=self.couleur_texte, cursor='hand2')
        check_voir_cibles_adverses.grid(row=2, column=0, padx=50, pady=15)
        self.widgets.append(check_voir_cibles_adverses)
        bouton_bateaux = Button(self.fenetre_menu, text='Nombres de bateaux', command=self.afficher_fenetre_nb_bateaux, font=('Helvetica', 14, 'bold'), bg=self.couleur_accent, fg="#ffffff", activebackground=self.couleur_survol, activeforeground="#ffffff", relief='flat', bd=0, padx=40, pady=15, cursor='hand2')
        bouton_bateaux.grid(row=3, column=0, padx=50, pady=15, sticky='ew')
        bouton_bateaux.bind("<Enter>", lambda e: e.widget.config(bg=self.couleur_survol))
        bouton_bateaux.bind("<Leave>", lambda e: e.widget.config(bg=self.couleur_accent))
        self.widgets.append(bouton_bateaux)
        bouton_retour = Button(self.fenetre_menu, text='Retour', command=self.afficher_menu_principal, font=('Helvetica', 14, 'bold'), bg="#b0bec5", fg=self.couleur_texte, activebackground="#cfd8dc", activeforeground=self.couleur_texte, relief='flat', bd=0, padx=40, pady=15, cursor='hand2')
        bouton_retour.grid(row=4, column=0, padx=50, pady=15, sticky='ew')
        bouton_retour.bind("<Enter>", lambda e: e.widget.config(bg="#cfd8dc"))
        bouton_retour.bind("<Leave>", lambda e: e.widget.config(bg="#b0bec5"))
        self.widgets.append(bouton_retour)
        self.fenetre_menu.grid_columnconfigure(0, weight=1)

    def afficher_fenetre_nb_bateaux(self):
        self.clear_widgets()
        self.fenetre_menu.configure(bg=self.couleur_fond)
        label = Label(self.fenetre_menu, text="Nombre de bateaux de chaque taille", font=('Helvetica', 24, 'bold'), bg=self.couleur_fond, fg="#0277bd", pady=30)
        label.grid(row=0, column=0, columnspan=2, padx=50, pady=(30, 20))
        self.widgets.append(label)
        self.form_nb_bateaux = []
        for i in range(5):
            label_bateau = Label(self.fenetre_menu, text=f'Nombre de bateau de taille {i+1}', font=('Helvetica', 12), bg=self.couleur_fond, fg=self.couleur_texte)
            label_bateau.grid(row=i+1, column=0, padx=20, pady=10, sticky='e')
            self.widgets.append(label_bateau)
            entry = Entry(self.fenetre_menu, font=('Helvetica', 12), bg="#ffffff", fg=self.couleur_texte, relief='flat', bd=2, highlightthickness=1, highlightbackground=self.couleur_accent, highlightcolor=self.couleur_accent)
            entry.grid(row=i+1, column=1, padx=20, pady=10, sticky='w')
            self.widgets.append(entry)
            self.form_nb_bateaux.append(entry)
        bouton_valider = Button(self.fenetre_menu, text='Valider', command=self.valider_et_quitter, font=('Helvetica', 14, 'bold'), bg=self.couleur_accent, fg="#ffffff", activebackground=self.self.couleur_survol, activeforeground="#ffffff", relief='flat', bd=0, padx=40, pady=15, cursor='hand2')
        bouton_valider.grid(row=7, column=0, padx=20, pady=(30, 15), sticky='ew')
        bouton_valider.bind("<Enter>", lambda e: e.widget.config(bg=self.couleur_survol))
        bouton_valider.bind("<Leave>", lambda e: e.widget.config(bg=self.couleur_accent))
        self.widgets.append(bouton_valider)
        bouton_retour = Button(self.fenetre_menu, text='Retour', command=self.afficher_parametres, font=('Helvetica', 14, 'bold'), bg="#b0bec5", fg=self.couleur_texte, activebackground="#cfd8dc", activeforeground=self.couleur_texte, relief='flat', bd=0, padx=40, pady=15, cursor='hand2')
        bouton_retour.grid(row=7, column=1, padx=20, pady=(30, 15), sticky='ew')
        bouton_retour.bind("<Enter>", lambda e: e.widget.config(bg="#cfd8dc"))
        bouton_retour.bind("<Leave>", lambda e: e.widget.config(bg="#b0bec5"))
        self.widgets.append(bouton_retour)
        self.fenetre_menu.grid_columnconfigure(0, weight=1)
        self.fenetre_menu.grid_columnconfigure(1, weight=1)

    def afficher_mode_jeu(self):
        self.clear_widgets()
        self.fenetre_menu.configure(bg=self.couleur_fond)
        label_text_principal_mode = Label(self.fenetre_menu, text='Mode de jeu', font=('Helvetica', 32, 'bold'), bg=self.couleur_fond, fg="#0277bd", pady=40)
        label_text_principal_mode.grid(row=0, column=0, padx=50, pady=(30, 20))
        self.widgets.append(label_text_principal_mode)
        bouton_joueur = Button(self.fenetre_menu, text='Jouer contre un joueur', command=self.jouer_contre_joueur, font=('Helvetica', 14, 'bold'), bg=self.couleur_accent, fg="#ffffff", activebackground=self.couleur_survol, activeforeground="#ffffff", relief='flat', bd=0, padx=40, pady=15, cursor='hand2')
        bouton_joueur.grid(row=1, column=0, padx=50, pady=15, sticky='ew')
        bouton_joueur.bind("<Enter>", lambda e: e.widget.config(bg=self.couleur_survol))
        bouton_joueur.bind("<Leave>", lambda e: e.widget.config(bg=self.couleur_accent))
        self.widgets.append(bouton_joueur)
        bouton_ia = Button(self.fenetre_menu, text='Jouer contre une ia', command=self.jouer_contre_ia, font=('Helvetica', 14, 'bold'), bg=self.couleur_accent, fg="#ffffff", activebackground=self.couleur_survol, activeforeground="#ffffff", relief='flat', bd=0, padx=40, pady=15, cursor='hand2')
        bouton_ia.grid(row=2, column=0, padx=50, pady=15, sticky='ew')
        bouton_ia.bind("<Enter>", lambda e: e.widget.config(bg=self.couleur_survol))
        bouton_ia.bind("<Leave>", lambda e: e.widget.config(bg=self.couleur_accent))
        self.widgets.append(bouton_ia)
        bouton_retour = Button(self.fenetre_menu, text='Retour', command=self.afficher_menu_principal, font=('Helvetica', 14, 'bold'), bg="#b0bec5", fg=self.couleur_texte, activebackground="#cfd8dc", activeforeground=self.couleur_texte, relief='flat', bd=0, padx=40, pady=15, cursor='hand2')
        bouton_retour.grid(row=3, column=0, padx=50, pady=15, sticky='ew')
        bouton_retour.bind("<Enter>", lambda e: e.widget.config(bg="#cfd8dc"))
        bouton_retour.bind("<Leave>", lambda e: e.widget.config(bg="#b0bec5"))
        self.widgets.append(bouton_retour)
        self.fenetre_menu.grid_columnconfigure(0, weight=1)

    def valider_et_quitter(self):
        self.dico_bateaux_a_poser = self.recuperer_taille_bateaux()
        self.afficher_menu_principal()

    def quitter_fenetre(self):
        self.fenetre_menu.destroy()

    def recuperer_taille_bateaux(self):
        #On test si les valeurs rentrées par l'utilisateur sont valides
        try:
            nb_bateaux_1 = int(self.form_nb_bateaux[0].get())
            nb_bateaux_2 = int(self.form_nb_bateaux[1].get())
            nb_bateaux_3 = int(self.form_nb_bateaux[2].get())
            nb_bateaux_4 = int(self.form_nb_bateaux[3].get())
            nb_bateaux_5 = int(self.form_nb_bateaux[4].get())
        #sinon on met des valeurs par défaut
        except:
            nb_bateaux_1 = 0
            nb_bateaux_2 = 1
            nb_bateaux_3 = 2
            nb_bateaux_4 = 1
            nb_bateaux_5 = 1


        return {1 : nb_bateaux_1, 2 : nb_bateaux_2, 3 : nb_bateaux_3, 4 : nb_bateaux_4, 5 : nb_bateaux_5}

    def jouer_contre_ia(self):
        self.mode_jeu = '2_je'
        self.fenetre_menu.destroy()

    def jouer_contre_joueur(self):
        self.mode_jeu = '2_j'
        self.fenetre_menu.destroy()

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

        fenetre.afficher_plateau(plateau.plateau, True, True, 'droit', True) #Mise à jour de l'affichage
        plateau.liste_bateaux_a_poser.append(taille_bateau)            #Mise à jour de la liste des bateaux à poser

        index = taille_bateau - 1
        canva_placement.itemconfig(text_ids[0][index], text='× ' + str(plateau.liste_bateaux_a_poser.count(taille_bateau)))
        return taille_bateau
    return None







dico_bateaux_a_poser = {}



menu = UI_menu()
option_can_touch = menu.can_touch.get()
option_voir_cibles_adverses = menu.voir_cibles_adverses.get()
afficher_croix = False if option_can_touch == True else True
dico_bateaux_a_poser = menu.dico_bateaux_a_poser
mode_jeu = menu.mode_jeu

plateau_joueur1 = Plateau()
plateau_joueur1.creation_plateau()
plateau_joueur2 = Plateau()
plateau_joueur2.creation_plateau()
fenetre1 = UI_game("joueur 1", 1)
fenetre1.afficher_plateau(plateau_joueur1.plateau, True, True, 'gauche', afficher_croix)
fenetre1.afficher_plateau(plateau_joueur2.plateau, option_voir_cibles_adverses, True, 'droit', afficher_croix)
fenetre2 = UI_game("Joueur 2", 2)
fenetre2.afficher_plateau(plateau_joueur1.plateau, True, True, 'gauche', afficher_croix)
fenetre2.afficher_plateau(plateau_joueur2.plateau, option_voir_cibles_adverses, True, 'droit', afficher_croix)
if mode_jeu != '2_j':
    fenetre2.fenetre.withdraw()

#On met des valeurs par défaut si le joueur ferme la fenêtre
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


fenetre1.titre_information(fenetre1.fenetre,"C'est à vous de poser les bateaux",1,22,15)
fenetre1.bloc_canva(fenetre1.fenetre, "Vos bateaux à poser", '× ', plateau_joueur1.nb_bateau_restant_a_pose_par_taille(), 2, 22, "bleu")
fenetre1.titre_information(fenetre1.fenetre,"Click droit pour enlever un bateau",3,22,12)


fenetre2.titre_information(fenetre2.fenetre,"C'est à l'adversaire de poser ces bateaux",1,22,15)
fenetre2.titre_information(fenetre2.fenetre,"Click droit pour enlever un bateau",3,22,12)
fenetre2.bloc_canva(fenetre2.fenetre, "Vos bateaux à poser", '× ', plateau_joueur2.nb_bateau_restant_a_pose_par_taille(), 2, 22, "bleu")
if mode_jeu == '2_j':
    liste_joueur_humain = [1,2]
    liste_joueur_ia = []
else:
    liste_joueur_humain = [1]
    liste_joueur_ia = [2]

#Boucle qui demande aux deux joueurs de donner la position de leurs bateau à poser sur leur plateau
fenetre1.canva_bind = 'droite'
fenetre2.canva_bind = 'droite'

for joueur in liste_joueur_humain:
    if joueur == 1:
        #plateau_joueur1.afficher_plateau(True, True)
        fenetre1.afficher_plateau(plateau_joueur1.plateau, option_voir_cibles_adverses, True, 'droit', afficher_croix)
        liste_bateaux_a_poser = plateau_joueur1.liste_bateaux_a_poser
    else:
        #plateau_joueur2.afficher_plateau(True, True)
        fenetre2.afficher_plateau(plateau_joueur2.plateau, option_voir_cibles_adverses, True, 'droit', afficher_croix)
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
                fenetre1.canva_droite.bind("<Button-3>", lambda event: on_clique_droit(event, plateau_joueur1, fenetre1, fenetre1.bloc_canva_var, fenetre1.canva_text_ids))

            else:
                fenetre2.canva_droite.bind("<Motion>", lambda event: on_mouvement(event, fenetre2, plateau_joueur2, orientation[0], taille, 'droite', option_can_touch))
                fenetre2.canva_droite.bind("<MouseWheel>", lambda event: on_molette(event, fenetre2, plateau_joueur2, orientation, taille, 'droite', option_can_touch))
                fenetre2.canva_droite.bind("<Button-3>", lambda event: on_clique_droit(event, plateau_joueur2, fenetre2, fenetre2.bloc_canva_var, fenetre2.canva_text_ids))

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
                #plateau_joueur1.afficher_plateau(True, True)
                fenetre1.afficher_plateau(plateau_joueur1.plateau, option_voir_cibles_adverses, True, 'droite', afficher_croix)
                if bonne_position_bateau == True:
                    liste_bateaux_a_poser.remove(taille)
                    index = taille - 1
                    fenetre1.bloc_canva_var.itemconfig(fenetre1.canva_text_ids[0][index], text='× ' + str(liste_bateaux_a_poser.count(taille)))
                num_joueur = 2
            else:
                bonne_position_bateau = plateau_joueur2.ajouter_bateau(coordonnee_case_x, coordonnee_case_y, orientation[0], taille, option_can_touch)   
                #plateau_joueur2.afficher_plateau(True, True)
                fenetre2.afficher_plateau(plateau_joueur2.plateau, option_voir_cibles_adverses, True, 'droite', afficher_croix)
                if bonne_position_bateau == True:
                    liste_bateaux_a_poser.remove(taille)
                    index = taille - 1
                    fenetre2.bloc_canva_var.itemconfig(fenetre2.canva_text_ids[0][index], text='× ' + str(liste_bateaux_a_poser.count(taille)))

    fenetre1.titres[0].configure(text="C'est à l'adversaire de poser ces bateaux")
    fenetre2.titres[0].configure(text="C'est à vous de poser les bateaux")
for joueur in liste_joueur_ia:
    if joueur == 1:
        plateau_joueur1.pose_bateaux_aleatoire(option_can_touch)
    else:
        plateau_joueur2.pose_bateaux_aleatoire(option_can_touch)

plateau_joueur1.liste_bateau_total = copy.deepcopy(plateau_joueur1.liste_bateau_restant)
plateau_joueur2.liste_bateau_total = copy.deepcopy(plateau_joueur2.liste_bateau_restant)

for i in range(2):
    fenetre1.titres[i].destroy()
    fenetre2.titres[i].destroy()
for widget in fenetre1.canva_ids:
    widget.destroy()
for widget in fenetre2.canva_ids:
    widget.destroy()
fenetre1.vider_ids()
fenetre2.vider_ids()

fenetre1.titre_information(fenetre1.fenetre,"C'est à vous de jouer",1,22,15)
fenetre2.titre_information(fenetre2.fenetre,"C'est à l'adversaire de jouer",1,22,15)

fenetre1.bloc_canva(fenetre1.fenetre, "Vos bateaux restant", '× ', plateau_joueur1.nb_bateau_restant_par_taille(), 2, 22, "bleu")
fenetre2.bloc_canva(fenetre2.fenetre, "Vos bateaux restant", '× ', plateau_joueur2.nb_bateau_restant_par_taille(), 2, 22, "bleu")
fenetre1.bloc_canva(fenetre1.fenetre, "Les bateaux adverse", '× ', plateau_joueur1.nb_bateau_restant_par_taille(), 3, 22, "rouge")
fenetre2.bloc_canva(fenetre2.fenetre, "Les bateaux adverse", '× ', plateau_joueur2.nb_bateau_restant_par_taille(), 3, 22, "rouge")

joueur = 1
joueur_perdu = None
fin_du_jeux = False
coordonnee_case_x, coordonnee_case_y = 0,0
fenetre1.canva_bind = 'gauche'
fenetre2.canva_bind = 'gauche'
while not fin_du_jeux:
    # affiche les plateaux
    #print("\n","Ton propre plateau qui sert à viser l'adversaire")
    if joueur == 1:
        #plateau_joueur2.afficher_plateau(True, False)
        #print("\n" , "Ton plateau avec tes bateaux")
        #plateau_joueur1.afficher_plateau(True, True)
        fenetre1.titres[0].configure(text="C'est à vous de jouer")
        fenetre2.titres[0].configure(text="C'est à l'adversaire de jouer")
        

    if joueur == 2:
        #plateau_joueur1.afficher_plateau(True, False)
        #print("\n" , "Ton plateau avec tes bateaux")
        #plateau_joueur2.afficher_plateau(True, True)
        fenetre1.titres[0].configure(text="C'est à l'adversaire de jouer")
        fenetre2.titres[0].configure(text="C'est à vous de jouer")

    fenetre1.afficher_plateau(plateau_joueur2.plateau, True, False, 'gauche', False)
    if not fenetre1.canva_cacher:
        fenetre1.afficher_plateau(plateau_joueur1.plateau, option_voir_cibles_adverses, True, 'droite', False)
    fenetre2.afficher_plateau(plateau_joueur1.plateau, True, False, 'gauche', False)
    if not fenetre2.canva_cacher:
        fenetre2.afficher_plateau(plateau_joueur2.plateau, option_voir_cibles_adverses, True, 'droite', False)


    #print(f"C'est au joueur du joueur {joueur} de jouer")

    # demande la case à ciblé
    bonne_position_cible = False
    while not bonne_position_cible:
        #coordonner_case_x = int(input("Dans quel numero de ligne veux tu cibler ?"))
        #coordonner_case_y = int(input("Dans quel numero de colonne veux tu cibler ? "))

        if joueur == 1:
            if 1 in liste_joueur_humain:
                fenetre1.canva_gauche.config(cursor="none")
                fenetre1.canva_gauche.bind("<Motion>", fenetre1.afficher_croix)
                fenetre1.canva_gauche.bind("<Leave>", fenetre1.cacher_croix)
                coordonnee_case = fenetre1.attendre_click_case()
                fenetre1.canva_gauche.config(cursor="arrow")
                fenetre1.canva_gauche.unbind("<Motion>")
                fenetre1.canva_gauche.unbind("<Leave>")
            else :
                coordonnee_case = plateau_joueur2.coup_IA(option_can_touch)
        else:
            if 2 in liste_joueur_humain:
                fenetre2.canva_gauche.config(cursor="none")
                fenetre2.canva_gauche.bind("<Motion>", fenetre2.afficher_croix)
                fenetre2.canva_gauche.bind("<Leave>", fenetre2.cacher_croix)
                coordonnee_case = fenetre2.attendre_click_case()
                fenetre2.canva_gauche.config(cursor="arrow")
                fenetre2.canva_gauche.unbind("<Motion>")
                fenetre2.canva_gauche.unbind("<Leave>")
            else:
                coordonnee_case = plateau_joueur1.coup_IA(option_can_touch)
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
                #print(f"Le bateau de taille {taille_bateau_restant[0]} a été touché il lui reste {taille_bateau_restant[1]} vie(s)")
                pass
            else: # si tout le bateau a été découvert
                nb_bateaux_restant = plateau_joueur2.nb_bateau_restant()
                #print(f"Le bateau de taille {taille_bateau_restant[0]} a été coulé")

                idx = taille_bateau_restant[0] - 1   
                fenetre1.canva_ids[1].itemconfig(fenetre1.canva_text_ids[1][idx], text='× '+ str(plateau_joueur2.nb_bateau_restant_par_taille()[idx]))
                fenetre2.canva_ids[0].itemconfig(fenetre2.canva_text_ids[0][idx], text='× '+ str(plateau_joueur2.nb_bateau_restant_par_taille()[idx]))

                index_bateau_touche = 0
                for index_bateau, bateau in enumerate(plateau_joueur2.liste_bateau_total):
                    for case in bateau[1]:
                        if case == [coordonnee_case_x, coordonnee_case_y]:
                            index_bateau_touche = index_bateau
                for case in plateau_joueur2.liste_bateau_total[index_bateau_touche][1]:
                    plateau_joueur2.modifier_case(case[0], case[1], 5)
                                      

                if nb_bateaux_restant != 0: # s'il reste des bateaux
                    #print(f"Il reste {nb_bateaux_restant} bateau(x) en vie")
                    pass
                else: # s'il n'y a plus de bateau restant
                    #print("Partie terminée, le joueur 1 a gagné")
                    joueur_perdu = 2
                    fin_du_jeux = True
        else: # une case vide
            plateau_joueur2.modifier_case(coordonnee_case_x, coordonnee_case_y, 1)
            #print("La case ne contient pas de bateaux")
            joueur = 2

    elif joueur == 2:
        if plateau_joueur1.cible_case(coordonnee_case_x, coordonnee_case_y) == True: # si bateau présent
            taille_bateau_restant = plateau_joueur1.enlever_case_bateau(coordonnee_case_x, coordonnee_case_y)
            plateau_joueur1.modifier_case(coordonnee_case_x, coordonnee_case_y, 3)
            if taille_bateau_restant[1] != 0: # s'il reste des parties non découvertes du bateau trouvé
                #print(f"Le bateau de taille {taille_bateau_restant[0]} a été touché il lui reste {taille_bateau_restant[1]} vie(s)")
                pass
            else: # si tout le bateau a été découvert
                nb_bateaux_restant = plateau_joueur1.nb_bateau_restant()
                #print(f"Le bateau de taille {taille_bateau_restant[0]} a été coulé")

                idx = taille_bateau_restant[0] - 1
                fenetre1.canva_ids[0].itemconfig(fenetre1.canva_text_ids[0][idx], text='× '+ str(plateau_joueur1.nb_bateau_restant_par_taille()[idx]))
                fenetre2.canva_ids[1].itemconfig(fenetre2.canva_text_ids[1][idx], text='× '+ str(plateau_joueur1.nb_bateau_restant_par_taille()[idx]))

                index_bateau_touche = 0
                for index_bateau, bateau in enumerate(plateau_joueur1.liste_bateau_total):
                    for case in bateau[1]:
                        if case == [coordonnee_case_x, coordonnee_case_y]:
                            index_bateau_touche = index_bateau

                for case in plateau_joueur1.liste_bateau_total[index_bateau_touche][1]:
                    plateau_joueur1.modifier_case(case[0], case[1], 5)
                    


                if nb_bateaux_restant != 0: # s'il reste des bateaux
                    #print(f"Il reste {nb_bateaux_restant} bateau(x) en vie")
                    pass
                else: # s'il n'y a plus de bateau restant
                    #print(f"Partie terminée, le joueur 2 a gagné")
                    joueur_perdu = 1
                    fin_du_jeux = True
        else: # une case vide
            plateau_joueur1.modifier_case(coordonnee_case_x, coordonnee_case_y, 1)
            #print("La case ne contient pas de bateaux")
            joueur = 1

fenetre1.afficher_plateau(plateau_joueur2.plateau, True, False, 'gauche', False)
fenetre1.afficher_plateau(plateau_joueur1.plateau, option_voir_cibles_adverses, True, 'droite', False)
fenetre2.afficher_plateau(plateau_joueur1.plateau, True, False, 'gauche', False)
fenetre2.afficher_plateau(plateau_joueur2.plateau, option_voir_cibles_adverses, True, 'droite', False)
vert = Image.new("RGBA", (480,480), (0, 255, 0, 120))
rouge = Image.new("RGBA", (480,480), (255, 0, 0, 120))
if joueur_perdu == 2:
    tk_vert = ImageTk.PhotoImage(vert, master=fenetre1.fenetre)
    tk_rouge = ImageTk.PhotoImage(rouge, master=fenetre1.fenetre)
    fenetre2.canva_gauche.create_image(1,1,image=tk_rouge, anchor=NW)
    fenetre1.canva_droite.create_image(1,1,image=tk_vert, anchor=NW)
    fenetre2.canva_droite.create_image(1,1,image=tk_rouge, anchor=NW)
    fenetre1.canva_gauche.create_image(1,1,image=tk_vert, anchor=NW)
if joueur_perdu == 1:
    tk_vert = ImageTk.PhotoImage(vert, master=fenetre1.fenetre)
    tk_rouge = ImageTk.PhotoImage(rouge, master=fenetre1.fenetre)
    fenetre2.canva_gauche.create_image(1,1,image=tk_vert, anchor=NW)
    fenetre1.canva_droite.create_image(1,1,image=tk_rouge, anchor=NW)
    fenetre2.canva_droite.create_image(1,1,image=tk_vert, anchor=NW)
    fenetre1.canva_gauche.create_image(1,1,image=tk_rouge, anchor=NW)

mainloop()