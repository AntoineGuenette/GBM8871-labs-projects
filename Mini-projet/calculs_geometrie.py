import numpy as np

###################################
#DONNÉES PHYSIQUES ET GÉOMÉTRIQUES#
###################################

# Paramètre physique de l'eau à 20°C
eta = 8.94e-4

# Paramètres géométriques des canaux rectangulaires
h = 250e-6

# Paramètres géométriques des tubes
L_t = 0.2
r_t = 7.5e-4

# Paramètres géométriques des capillaires
L_c = 0.127
r_c = 6.515e-4

# Débits
Q_1 = (100/60) * 1e-9
Q_3 = 3*Q_1
Q_4 = 4*Q_1
Q_0 = Q_1 + Q_3 + Q_4

###################################
# DONNÉES À CHOISIR
###################################

# Choix des largeurs (en mètres)
w = 500e-6
w_0 = 4 * w
w_1 = w
w_2 = 4 * w
w_3 = 3 * w
w_4 = 4 * w

# Choix de la longueur de l'entrée du routeur (en mètres)
L_0 = 0.002

#####################################
# FONCTIONS DE CALCUL DES RÉSISTANCES
#####################################

def calc_R_cyl(L, r, eta):
    R_cyl = (8 * eta * L) / (np.pi * r**4)
    return R_cyl

def calc_R_rect(L, w, h, eta):
    R_rect = (12 * eta * L) / (h**3 * w)
    for n_i in range(1, 10, 2):
        terme_somme = (192 * h) / (np.pi**5 * n_i**5 * w) * np.tanh(n_i * np.pi * w / (2 * h))
        R_rect -= terme_somme
    return R_rect

def calc_L(R, w, h, eta):
    L = (R * h**3 * w) / (12 * eta)
    # Les termes de la somme sont négligés pour l'inversion
    return L

###################################
# Calcul des résistances du montage
###################################

R_t = calc_R_cyl(L_t, r_t, eta)
R_c = calc_R_cyl(L_c, r_c, eta)
R_0 = calc_R_rect(L_0, w_0, h, eta)

R_in = R_t + R_0
R_out = R_t + R_c

###################################
# Calcul des résistances du routeur
###################################

# On veut que les canaux aient une longueur 10x plus grande que leur largeur
# pour minimiser les effets de coins
L_3 = 10 * w_3

# On calcule R_3 avec L_3 choisi
R_3 = calc_R_rect(L_3, w_3, h, eta)

# Relations à respecter :
# R_1 = 3*R_3 + 2*R_out
# R_4 = R_2 + 3/4*R_3 - 1/4*R_out

# Calcul de L_1 pour respecter la première relation
R_1 = 3 * R_3 + 2 * R_out
# Inversion de calc_R_rect pour L_1
# (Les termnes de la somme sont négligés pour l'inversion)
L_1 = calc_L(R_1, w_1, h, eta)

# Calcul de L_4 pour respecter la deuxième relation
# On choisit L_2 = L_3
L_2 = L_3
# On calcule R_2 avec L_2 choisi
R_2 = calc_R_rect(L_2, w_2, h, eta)
# On calcule L_4 pour respecter la deuxième relation
R_4 = R_2 + 3/4 * R_3 - 1/4 * R_out
# Inversion de calc_R_rect pour L_4
L_4 = calc_L(R_4, w_4, h, eta)

#########################
# Affichage des résultats
#########################

print(f"\nRésistance d'entrée : {R_in:.2e}")
print(f"Résistance de sortie : {R_out:.2e}")

print(f"\nRésistance 1 : {R_1:.2e}")
print(f"Résistance 2 : {R_2:.2e}")
print(f"Résistance 3 : {R_3:.2e}")
print(f"Résistance 4 : {R_4:.2e}")

print(f"\nRelation R_1 = 3*R_3 + 2*R_out :")
print(f"valeur de gauche : {R_1:.2e}")
print(f"valeur de droite : {3*R_3 + 2*R_out:.2e}")

print(f"\nRelation R_4 = R_2 + 3/4*R_3 - 1/4*R_out :")
print(f"valeur de gauche : {R_4:.2e}")
print(f"valeur de droite : {R_2 + 3/4 * R_3 - 1/4 * R_out:.2e}")

print(f"\nLongueur 1 : {L_1*1e3:.2f} mm")
print(f"Longueur 2 : {L_2*1e3:.2f} mm")
print(f"Longueur 3 : {L_3*1e3:.2f} mm")
print(f"Longueur 4 : {L_4*1e3:.2f} mm\n")
