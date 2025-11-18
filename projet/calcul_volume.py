import numpy as np

# Dimensions géométriques
h_puce = 2.75e-3

d_inlet = 2.9e-3
d_raman = 2e-3
d_outlet = 1.5e-3

L_puits = 700e-6
W_puits = 700e-6
h_puits = 630e-6

W_canal = 700e-6
h_canal = 700e-6

dist_x = 3e-3
dist_y = 6e-3

# Calculs associés
dist_inout = 2* dist_x + 2.5*dist_y + (2*np.pi*W_canal)
dist_puits = dist_x + dist_y + 0.5*(2*np.pi*W_canal)
dist_tot = 2*(dist_inout + dist_puits)
print(f"\nDistance entrée-puits et sortie-puits : {dist_inout*1000:.2f} mm")
print(f"Distance entre puits : {dist_puits*1000:.2f} mm")
print(f"Longueur totale du canal : {dist_tot*1000:.2f} mm")

r_inlet = d_inlet / 2
r_raman = d_raman / 2
r_outlet = d_outlet / 2

A_inlet = np.pi * r_inlet**2
A_raman = np.pi * r_raman**2
A_outlet = np.pi * r_outlet**2

# Caclul du volume total
V_puits = L_puits * W_puits * h_puits
V_raman = A_raman * h_puce
V_inlet = A_inlet * h_canal
V_outlet = A_outlet * h_canal
print(f"\nVolume d'un puits : {V_puits*1e9:.2f} uL")
print(f"Volume de raman : {V_raman*1e9:.2f} uL")
print(f"Volume d'entrée : {V_inlet*1e9:.2f} uL")
print(f"Volume de sortie : {V_outlet*1e9:.2f} uL")

V_canal = W_canal * h_canal * (dist_tot - r_inlet - r_outlet)

V_tot = 3 * V_puits + V_inlet + V_outlet + V_canal # + 3 * V_raman
print(f"\nVolume total : {V_tot*1e9:.2f} uL")
print(f"Première approximation de V_max : {V_tot*1.2*1e9:.2f} uL")



