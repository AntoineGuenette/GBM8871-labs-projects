import numpy as np

h = 500e-6
w = 500e-6
gamma = 72.9e-3
theta_deg = 60
theta = np.deg2rad(theta_deg)
eta = 8.94e-4
t = 10

L = np.sqrt((1/h + 1/w) * np.cos(theta) * gamma * h**2/(12*eta) * (1-0.63*(h/w)) * t)
print(f"Longueur : {L*1000:.2f} mm")