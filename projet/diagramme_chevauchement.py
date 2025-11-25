import matplotlib.pyplot as plt

# Valeurs et incertitudes
values = {
    "Valeur théorique": (110.441, 8.639),
    "Valeur simulée": (115, 0.5),
    "Valeur expérimentale": (116, 0.8)
}

# Création du diagramme de chevauchement
labels = list(values.keys())
means = [values[k][0] for k in labels]
errors = [values[k][1] for k in labels]

fig, ax = plt.subplots(figsize=(8, 4))
ax.errorbar(
    means,
    labels,
    xerr=errors,
    fmt='o',
    capsize=8
)

ax.set_xlabel("Volume de débordement [uL]")
ax.set_title("Diagramme de chevauchement")

for i, label in enumerate(labels):
    x_min = means[i] - errors[i]
    x_max = means[i] + errors[i]
    ax.hlines(label, x_min, x_max, linewidth=6, alpha=0.2)

plt.tight_layout()
plt.show()