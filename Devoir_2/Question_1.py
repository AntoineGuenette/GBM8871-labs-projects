import numpy as np
import matplotlib.pyplot as plt

###################################
# DONNÉES PHYSIQUES ET GÉOMÉTRIQUES
###################################

# Définitions des constantes
kB = 1.380649e-23 # (J/K)
T = 298.15 # (K)
rho_or = 19300 # (kg/m3)
rho_eau = 1000 # (kg/m3)
g = 9.81 # (m/s2)
H = 0.10 # (m)

#################
# SOUS-QUESTION C
#################

# Génération des diamètres des particules
d = np.logspace(-9, -6, 200) # m

# Calcul du nombre de Péclet
Pe = (np.pi * d**3 * (rho_or - rho_eau) * g * H) / (6 * kB * T)

# Figure pour la sous-question C
plt.figure(figsize=(8, 5))
plt.plot(d * 1e9, Pe)
plt.xlabel("Diamètre, d, des particules d'or (nm)")
plt.ylabel("Nombre de Péclet (Pe)")
plt.title("Nombre de Péclet en fonction du diamètre des nanoparticules d'or")
plt.grid(True)
plt.tight_layout()
plt.show()

#################
# SOUS-QUESTION E
#################

# Calcul du h_50
h50 = -(H / Pe) * np.log(0.5 * (1 + np.exp(-Pe)))

# Figure pour la sous-question E
plt.figure(figsize=(8, 5))
plt.plot(d * 1e9, h50 * 100)
plt.yscale("log")
plt.xlabel("Diamètre d (nm)")
plt.ylabel("Hauteur h_50 (cm)")
plt.title("Hauteur d’équilibre h_50 en fonction du diamètre des nanoparticules d’or")
plt.grid(True, which="both")
plt.tight_layout()
plt.show()