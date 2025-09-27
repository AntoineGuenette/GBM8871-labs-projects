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

def simulation_t_chute(d: float, rho_part: float, rho_air: float, h: float, dt : int) -> float:
    
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

        # Pour des valeurs très petites de Re (Re << 1 donc Re < 0.1)
        if Re <= 1e-1:
            # Traînée de Stokes
            F_frot = -6 * np.pi * eta_air * r * v
        else:
            # Calcul du coefficient de frottement
            C = calcul_C(Re)
            # Traînée quadratique
            F_frot = -np.sign(v) * 1/2 * C * rho_air * A * v**2

        # Calcul du pas de vitesse
        dv = (F_frot/m - g) * dt

        # print("t:", t, "y:", y, "dv:", dv)

        # Lorsque la vitesse terminale est atteinte (donc lorsque dv proche de 0),
        # On peut calculer directement le temps restant pour la chute
        if abs(dv) < 1e-9 :
            v_terminal = v
            print(f"Vitesse terminale ({v_terminal*1e6:.2f} µm/s) atteinte par la particule de diamètre {d*1e6} µm après {t*1e6:.2f} µs!")
            if v_terminal == 0:
                break
            t += y / abs(v_terminal)
            return t

        v += dv
        y += v * dt
        t += dt
    
    return t - dt

print("\nPARTIE 1:")

t_part_1 = simulation_t_chute(d_part_1, rho_part, rho_air, h_bouche, dt=1e-6)
print(f"Temps de chute pour une particule de diamètre {d_part_1*1e6} µm : {t_part_1/3600:.2f} h")

t_part_2 = simulation_t_chute(d_part_2, rho_part, rho_air, h_bouche, dt=1e-6)
print(f"Temps de chute pour une particule de diamètre {d_part_2*1e6} µm : {t_part_2:.2f} s")

###############################################################
# PARTIE 2 : Distance horizontale de pénétration des particules
###############################################################

def simulation_dist_penetration(d: float, rho_part: float, rho_air: float, v_max: float, dt: int) -> float:
    
    # Calculs préliminaires
    r = d / 2 # Rayon de la particule (m)
    A = np.pi * r**2 # Section transversale de la particule (m^2)
    V = 4/3 * np.pi * r**3 # Volume de la particule (m^3)
    m = rho_part * V # Masse de la particule (kg)

    # Initialisation des variables
    t = 0 # Temps de chute (s)
    v = v_max # Vitesse (m.s^-1)
    x = 0 # Position (m)
    dv = 0

    # La vitesse ne sera jamais réellement nulle, donc on considère la distance de pénétration
    # comme étant la distance que la particule a parcouru lorsque sa vitesse est réduite de 99%
    while v >= 0.01*v_max:
        
        # Calcul du nombre de Reynolds
        Re = calcul_Re(rho_air, v, d, eta_air)

        # Pour des valeurs très petites de Re (Re << 1 donc Re < 0.1)
        if Re <= 1e-1:
            # Traînée de Stokes
            F_frot = - 6 * np.pi * eta_air * r * v
        else:
            # Calcul du coefficient de frottement
            C = calcul_C(Re)
            # Traînée quadratique
            F_frot = - np.sign(v) * 1/2 * C * rho_air * A * v**2

        # Calcul du pas de vitesse
        dv = F_frot/m * dt

        # Mise à jour des variables
        v += dv
        x += v * dt
        t += dt
    
    return x - v * dt

print("\nPARTIE 2:")

dist_penetration_part_1 = simulation_dist_penetration(d_part_1, rho_part, rho_air, v_max_x, dt=1e-8)
print(f"Distance de pénétration pour une particule de diamètre {d_part_1*1e6} µm : {dist_penetration_part_1*1e6:.2f} µm")

dist_penetration_part_2 = simulation_dist_penetration(d_part_2, rho_part, rho_air, v_max_x, dt=1e-6)
print(f"Distance de pénétration pour une particule de diamètre {d_part_2*1e6} µm : {dist_penetration_part_2:.2f} m")

##############################
# PARTIE 3 : DIAMÈTRE CRITIQUE
##############################

def diametre_critique(rho_part, rho_air, v_max_x, penetration_cible, dt=1e-6, tol=1e-6, max_iter=100):
    d_min = 500e-6
    d_max = 600e-6
    for i in range(max_iter):
        d_mid = 0.5 * (d_min + d_max)
        print(f"Simulation {i+1} en cours")
        dist = simulation_dist_penetration(d_mid, rho_part, rho_air, v_max_x, dt)
        
        if abs(dist - penetration_cible) < tol:
            return d_mid
        if dist < penetration_cible:
            d_min = d_mid
        else:
            d_max = d_mid
        print(f"Estimation {i+1} : {d_mid*1e6:.2f} µm avec un écart de {100*abs(dist-penetration_cible)/dist:.4f} %")
    return d_mid  # Retourne la meilleure estimation après max_iter

print("\nPARTIE 3:")
d_critique = diametre_critique(rho_part, rho_air, v_max_x, 2.0, dt=1e-6)
print(f"Diamètre critique pour une distance de pénétration de 2m : {d_critique*1e6:.2f} µm\n")
