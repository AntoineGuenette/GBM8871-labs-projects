import numpy as np

###################################
#DONNÉES PHYSIQUES ET GÉOMÉTRIQUES#
###################################

# Paramètre physique de l'eau à 20°C
eta = 8.94e-4
rho = 1000

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
L_0 = 0.004
L_3 = 10 * w_3
L_4 = 10 * w_4

#####################################
# FONCTIONS DE CALCUL DES RÉSISTANCES
#####################################

def calc_R_cyl(L, r, eta):
    R_cyl = (8 * eta * L) / (np.pi * r**4)
    return R_cyl

def calc_R_rect(L, w, h, eta):
    R_rect = (12 * eta * L) / (h**3 * w)
    somme = 1
    for n_i in range(1, 10, 2):
        terme_somme = (192 * h) / (np.pi**5 * n_i**5 * w) * np.tanh(n_i * np.pi * w / (2 * h))
        somme -= terme_somme
    return R_rect / somme

def calc_L(R, w, h, eta):
    L = (R * h**3 * w) / (12 * eta)
    somme = 1
    for n_i in range(1, 10, 2):
        terme_somme = (192 * h) / (np.pi**5 * n_i**5 * w) * np.tanh(n_i * np.pi * w / (2 * h))
        somme -= terme_somme
    return L * somme

##########################################################
# Fontions de calcul des vitesses et du nombre de Reynolds
##########################################################

def calc_v(Q, w, h):
    A = w * h
    v = Q / A
    return v

def calc_Re(v, h, L, eta, rho):
    Re = (rho * v * h**2) / (eta * L)
    return Re

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

# Calcul de L_2 pour respecter la deuxième relation, en utilisant L_4 choisi
R_4 = calc_R_rect(L_4, w_4, h, eta)
# On calcule R_2 pour respecter la deuxième relation
R_2 = R_4 - 3/4 * R_3 + 1/4 * R_out
# Inversion de calc_R_rect pour L_2
L_2 = calc_L(R_2, w_2, h, eta)

############################################
# Caclul des vitesses et nombres de Reynolds
############################################

v_in = calc_v(Q_0, w_0, h)
v_out = v_in * (w_0 / (w_1 + w_3 + w_4))

Re_in = calc_Re(v_in, h, L_0, eta, rho)
Re_out_1 = calc_Re(v_out, h, L_1, eta, rho)
Re_out_3 = calc_Re(v_out, h, L_3, eta, rho)
Re_out_4 = calc_Re(v_out, h, L_4, eta, rho)

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
print(f"Longueur 4 : {L_4*1e3:.2f} mm")

print(f"\nVitesse entrée : {v_in:.2e} m/s")
print(f"Vitesse sortie : {v_out:.2e} m/s")

print(f"\nNombre de Reynolds entrée : {Re_in:.2e}")
print(f"Nombre de Reynolds sortie 1 : {Re_out_1:.2e}")
print(f"Nombre de Reynolds sortie 3 : {Re_out_3:.2e}")
print(f"Nombre de Reynolds sortie 4 : {Re_out_4:.2e}\n")
