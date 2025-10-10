import numpy as np

###################################
#DONNÉES PHYSIQUES ET GÉOMÉTRIQUES#
###################################

V = 100e-6 # L
delta_V = 1e-6 # L

L = 75e-3 # m
delta_L = 127e-6 # m

v = 1.05e-2 # m/s
delta_v = 0.03e-2 # m/s

r = 6.515e-4 # m

#######################################
# CALCUL DU DÉBIT ET DE SON INCERTITUDE
#######################################

Q = np.pi * r**2 * v
print(f"Débit: {Q:.2e} m3/s")

delta_Q = np.sqrt((v/L * delta_V)**2 + (V*v/(L**2) * delta_L)**2 + (V/L * delta_v)**2)
print(f"Incertitude sur le débit: {delta_Q:.4e} m3/s")