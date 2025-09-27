import numpy as np

###################################
# DONNÉES PHYSIQUES ET GÉOMÉTRIQUES
###################################

# (L'ensemble des références utilisées pour les données est disponible dans le rapport)

rho_part = 1007 # Masse volumique des particules (kg.m^-3)
rho_air = 1.293 # Masse volumique de l'air (kg.m^-3)
eta_air = 1.9e-5 # Viscosité dynamique de l'air (kg.m^-1.s^-1)

d_part_1 = 0.5e-6 # Diamètre d'un noyau de gouttelette (m)
d_part_2 = 500e-6 # Diamètre d'un postillon (m)

h_bouche = 1.50 # Hauteur de la bouche (m)
L = 2.00 # Distance considérée pour la règle de distanciation (m)

v_max_x = 15.90 # Vitesse horizontale maximale d'expulsion de l'air lors d'un éternuemen (m.s^-1)
g = 9.81 # Accélération gravitationnelle (m.s^-2)

##############################################################
# CALCUL DU NOMBRE DE REYNOLDS ET DU COEFFICIENT DE FROTTEMENT
##############################################################

def calcul_Re(rho: float, v: float, d: float, eta: float) -> float:
    Re = (rho * np.abs(v) * d) / eta
    return Re

def calcul_C(Re: float) -> float:
    C = 24 / Re + 4 / np.sqrt(Re) + 0.4
    return C

##################################################
# PARTIE 1 : CHUTE LIBRE DES PARTICULES DANS L'AIR
##################################################

def simulation_t_chute(d: float, rho_part: float, rho_air: float, h: float, dt=1e-3) -> float:
    
    # Calculs préliminaires
    r = d / 2 # Rayon de la particule (m)
    A = np.pi * r**2 # Section transversale de la particule (m^2)
    V = 4/3 * np.pi * r**3 # Volume de la particule (m^3)
    m = rho_part * V # Masse de la particule (kg)

    # Initialisation des variables
    t = 0 # Temps de chute (s)
    v = 0 # Vitesse (m.s^-1)
    y = h # Position (m)

    while y>=0:
        
        # Calcul du nombre de Reynolds
        Re = calcul_Re(rho_air, v, d, eta_air)

        if Re <= 1e-3:
            # Traînée de Stokes
            F_frot = -6 * np.pi * eta_air * r * v
        else:
            # Calcul du coefficient de frottement
            C = calcul_C(Re)
            # Traînée quadratique
            F_frot = -np.sign(v) * 1/2 * C * rho_air * A * v**2

        # Calcul du pas de vitesse
        dv = (F_frot/m - g) * dt

        # Mise à jour des variables
        v += dv
        y += v * dt
        t += dt
    
    return t - dt

t_part_1 = simulation_t_chute(d_part_1, rho_part, rho_air, h_bouche, dt=1e-5)
t_part_2 = simulation_t_chute(d_part_2, rho_part, rho_air, h_bouche, dt=1e-5)

print("\nQUESTION C:")
print(f"Temps de chute pour une particule de diamètre {d_part_1*1e6} µm : {t_part_1:.8f} s")
print(f"Temps de chute pour une particule de diamètre {d_part_2*1e6} µm : {t_part_2:.8f} s\n")

###############################################################
# PARTIE 2 : Distance horizontale de pénétration des particules
###############################################################

def simulation_dist_penetration(d: float, rho_part: float, rho_air: float, v_max: float, dt=1e-3) -> float:
    
    # Calculs préliminaires
    r = d / 2 # Rayon de la particule (m)
    A = np.pi * r**2 # Section transversale de la particule (m^2)
    V = 4/3 * np.pi * r**3 # Volume de la particule (m^3)
    m = rho_part * V # Masse de la particule (kg)

    # Initialisation des variables
    t = 0 # Temps de chute (s)
    v = v_max # Vitesse (m.s^-1)
    x = 0 # Position (m)

    while v >= 0.01*v_max:
        
        # Calcul du nombre de Reynolds
        Re = calcul_Re(rho_air, v, d, eta_air)

        if Re <= 1e-3:
            # Traînée de Stokes
            F_frot = 6 * np.pi * eta_air * r * v
        else:
            # Calcul du coefficient de frottement
            C = calcul_C(Re)
            # Traînée quadratique
            F_frot = np.sign(v) * 1/2 * C * rho_air * A * v**2

        # Calcul du pas de vitesse
        dv = -F_frot/m * dt

        # Mise à jour des variables
        v += dv
        x += v * dt
        t += dt

        print(dv, v, x, t, Re, F_frot)
    
    return x - v * dt

dist_penetration_part_1 = simulation_dist_penetration(d_part_1, rho_part, rho_air, v_max_x, 1e-1)
dist_penetration_part_2 = simulation_dist_penetration(d_part_2, rho_part, rho_air, v_max_x, 1e-1)

print("\nQUESTION D:")
print(f"Distance de pénétration pour une particule de diamètre {d_part_1*1e6} µm : {dist_penetration_part_1:.8f} m")
print(f"Distance de pénétration pour une particule de diamètre {d_part_2*1e6} µm : {dist_penetration_part_2:.8f} m\n")

##############################
# PARTIE 3 : DIAMÈTRE CRITIQUE
##############################

# TODO
