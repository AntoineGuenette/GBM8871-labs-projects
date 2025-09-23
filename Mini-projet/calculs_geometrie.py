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
w_1 = 500e-6
w_2 = 500e-6
w_3 = 500e-6
w_4 = 500e-6

# Choix d'une longueur de base pour L_3 (en mètres)
L_3 = 0.01 # Ce sera la longueur de canal la plus courte

###################################
# Calcul des résistances du montage
###################################

R_t = 8 * eta * L_t / (np.pi * r_t**4)
R_c = 8 * eta * L_c / (np.pi * r_c**4)

R_in = R_t
R_out = R_t + R_c

# print(f"\nRésistance d'entrée : {R_in:.2e}")
# print(f"Résistance de sortie : {R_out:.2e}")

###################################
# Calcul des résistances du routeur
###################################

# On calcule R_3 avec L_3 choisi
def calc_R_rect(L, w, h, eta):
    R_rect = (12 * eta * L) / (h**3 * w)
    for n_i in range(1, 10, 2):
        terme_somme = (192 * h) / (np.pi**5 * n_i**5 * w) * np.tanh(n_i * np.pi * w / (2 * h))
        R_rect -= terme_somme
    return R_rect

R_3 = calc_R_rect(L_3, w_3, h, eta)

# Calcul de L_1 pour respecter la première relation
R_1 = 3 * R_3 + 2 * (8 * eta * L_t / (np.pi * r_t**4) + 8 * eta * L_c / (np.pi * r_c**4))
# Inversion de calc_R_rect pour L_1
L_1 = (R_1 * h**3 * w_1) / (12 * eta)

# Calcul de L_2 pour respecter la deuxième relation
# R_4 = R_2 + 3/4*R_3 - 1/4*R_out
# Donc R_2 = R_4 - 3/4*R_3 + 1/4*R_out
# On choisit L_4 = L_1 (pour garder les canaux symétriques)
L_4 = L_1
R_4 = calc_R_rect(L_4, w_4, h, eta)
R_out = 8 * eta * L_t / (np.pi * r_t**4) + 8 * eta * L_c / (np.pi * r_c**4)
R_2 = R_4 - 3/4 * R_3 + 1/4 * R_out
L_2 = (R_2 * h**3 * w_2) / (12 * eta)

#########################
# Affichage des résultats
#########################

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
