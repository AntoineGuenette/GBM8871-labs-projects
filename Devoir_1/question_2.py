import numpy as np

###################################
# DONNÉES PHYSIQUES ET GÉOMÉTRIQUES
###################################

# Viscosité du PBS (approximée à celle de l'eau à 20˚C) (kg.m^-1.s^-1)
eta = 1e-3

# Largeur et hauteur des canaux d'entrées, intermédiaires et de sortie, en plus des serpentins (m)
w = 50e-6
h = 50e-6

# Longueur des canaux d'entrées (m)
Le  = 2000e-6

# Longueur des sections du diffuseur
Ld1 = 3000e-6
Ld2 = 1000e-6
Ld3 = 3000e-6

# Largeur des sections du diffuseur
wd1 = 600e-6
wd2 = 450e-6
wd3 = 300e-6

#################################
# CALCUL DES LONGUEURS DES CANAUX
#################################

# Longueur des serpentins (m)
Ls = 50 * 2 + 225 * 2 + 500 * 7 + np.pi/2 * 1/2 * (150 + 50) * 9
Ls = Ls / 1000000

# Longueur des canaux intermédiaires reliant les serpentins (m)
Li = 400 + np.pi/4 * 1/2 * (150 + 50)
Li = Li / 1000000

# Longueur des canaux de sortie (m)
L1 = 300 + 1650 + 430 + np.pi/2 * 1/2 * (150 + 50)
L1 = L1 / 1000000
L2 = 200 + 960 + 530 + np.pi/2 * 1/2 * (150 + 50)
L2 = L2 / 1000000
L3 = 100 + 270 + 630 + np.pi/2 * 1/2 * (150 + 50)
L3 = L3 / 1000000

##################################################
# FONCTIONS DE CALCUL DES RÉSISTANCES HYDRAULIQUES
##################################################

def calcul_resistance_rayonhydro(L, h=h, w=w):
    """Question A"""
    RH = h * w / (h + w)
    return 8 * eta * L / (RH**2 * h * w)

def calcul_resistance_solutionStokes(L, h=h, w=w):
    """Question B"""
    R_rect = (12 * eta * L) / (h**3 * w)
    somme = 1
    for n_i in range(1, 10, 2):
        terme_somme = (192 * h) / (np.pi**5 * n_i**5 * w) * np.tanh(n_i * np.pi * w / (2 * h))
        somme -= terme_somme
    return R_rect / somme

def calcul_resistance_plaquesParalleles(L, h=h, w=w):
    """Question C"""
    return 12 * eta * L / (h**3 * w)

def calcul_resistance_solutionStokes_premierTerme(L, h=h, w=w):
    """Question D"""
    return 12 * eta * L / (h**3 * w * (1 - 0.63 * h/w))

def afficher_resultats(methode, nom=None):
    if nom is None:
        nom = methode.__name__

    print(f"méthode: {nom} :")
    Rs = methode(Ls)
    Ri = methode(Li)
    Re = methode(Le)
    R1 = methode(L1)
    R2 = methode(L2)
    R3 = methode(L3)
    Rd1 = methode(Ld1, h=50e-6, w=wd1)
    Rd2 = methode(Ld2, h=50e-6, w=wd2)
    Rd3 = methode(Ld3, h=50e-6, w=wd3)

    print(f'Rs = {Rs:.3g}')
    print(f'Ri = {Ri:.3g}')
    print(f'Re = {Re:.3g}')
    print(f'R1 = {R1:.3g}')
    print(f'R2 = {R2:.3g}')
    print(f'R3 = {R3:.3g}')

    Rtot = (
        Re / 2
        + Rs * (1/4 + 1/5 + 1/3)
        + 1/(2/(Rs+R1) + 2/(Rs+R2) + 2/(Rs+R3))
        + Rd1 + Rd2 + Rd3
    )
    print(f'Rtot = {Rtot:.3g}\n')


#########################
# AFFICHAGE DES RÉSULTATS
#########################

if __name__ == "__main__" :

    print("CALCUL DES LONGUEURS DES CANAUX")
    print(f'Ls = {Ls*1e6:.2f} um')
    print(f'Li = {Li*1e6:.2f} um')
    print(f'Ratio Ls/Li = {Ls/Li:.2f} >> 1')
    print(f'L1 = {L1*1e6:.2f} um')
    print(f'L2 = {L2*1e6:.2f} um')
    print(f'L3 = {L3*1e6:.2f} um\n')

    calcul_resistance = [
    calcul_resistance_rayonhydro,
    calcul_resistance_solutionStokes,
    calcul_resistance_plaquesParalleles,
    calcul_resistance_solutionStokes_premierTerme
    ]

    for methode in calcul_resistance:
        afficher_resultats(methode)
