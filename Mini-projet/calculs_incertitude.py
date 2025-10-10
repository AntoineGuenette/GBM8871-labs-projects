import numpy as np

###################################
#DONNÉES PHYSIQUES ET GÉOMÉTRIQUES#
###################################

V = 100e-9 # m3
delta_V = 0.01 * V # m3

L = 75e-3 # m
delta_L = 127e-6 # m

v = 1.01e-2 # m/s
delta_v = 0.04e-2 # m/s

r = 6.515e-4 # m

w_4 = 2e-3 # m
h = 250e-6 #m

#######################################
# CALCUL DU DÉBIT ET DE SON INCERTITUDE
#######################################

Q = np.pi * r**2 * v
print(f"Débit: {Q:.3e} m3/s")

delta_Q = np.sqrt((v/L * delta_V)**2 + (V*v/(L**2) * delta_L)**2 + (V/L * delta_v)**2)
print(f"Incertitude sur le débit: {delta_Q:.3e} m3/s")

######################################
# CALCUL DE LA VITESSE DANS LE ROUTEUR
######################################

v_routeur = Q / (w_4 * h)
print(f"Vitesse: {v_routeur:.4e} m/s")
