import matplotlib.pyplot as plt

# Valeurs et incertitudes
values = {
    "Analogie électrique": (109.989, 8.603),   # valeur, incertitude
    "Modélisation COMSOL": (115, 1),
    "Valeur expérimentale": (116, 0.8)
}

# Préparation
labels = list(values.keys())
means = [values[k][0] for k in labels]
errors = [values[k][1] for k in labels]

fig, ax = plt.subplots(figsize=(8, 4))

# Affichage des barres ± incertitudes
ax.errorbar(
    means,                         # valeurs
    labels,                        # positions verticales
    xerr=errors,                   # barres d'incertitude
    fmt='o',                       # point central
    capsize=8                      # petite barre au bout
)

# Style
ax.set_xlabel("Volume [uL]")
ax.set_title("Diagramme de chevauchement")

# Affichage de la plage min-max en arrière-plan
for i, label in enumerate(labels):
    x_min = means[i] - errors[i]
    x_max = means[i] + errors[i]
    ax.hlines(label, x_min, x_max, linewidth=6, alpha=0.2)

plt.tight_layout()
plt.show()