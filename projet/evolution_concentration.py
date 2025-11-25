import pandas as pd
import matplotlib.pyplot as plt

# Charger le fichier CSV (adapter le chemin si nécessaire)
fichier = '/Users/Shared/COMSOL/GBM8871/Figures projet/Changement de milieu/concentrations.csv'

# Lecture en ignorant les lignes de commentaires
df = pd.read_csv(
    fichier,
    comment='%',
)

df.columns = [
    "time_s",
    "c0_puits_1_pct",
    "c0_puits_2_pct",
    "c0_puits_3_pct",
    "c0_systeme_pct"
]

# Créer une nouvelle ligne pour t=0s avec les valeurs initiales
nouvelle_ligne = pd.DataFrame({
    "time_s": [0],
    "c0_puits_1_pct": [10],
    "c0_puits_2_pct": [10],
    "c0_puits_3_pct": [10],
    "c0_systeme_pct": [10.5]
})

# Ajouter la nouvelle ligne au début et réinitialiser l'index
df = pd.concat([nouvelle_ligne, df], ignore_index=True)

# Sauvegarder le CSV modifié
df.to_csv("concentrations_modifie.csv", index=False)

# Tracer le graphique
plt.figure(figsize=(8, 5))

plt.plot(df["time_s"], df["c0_puits_1_pct"], label="Puits 1", color="tab:blue")
plt.plot(df["time_s"], df["c0_puits_2_pct"], label="Puits 2", color="tab:pink")
plt.plot(df["time_s"], df["c0_puits_3_pct"], label="Puits 3", color="tab:green")
plt.plot(df["time_s"], df["c0_systeme_pct"], label="Système", color="tab:purple")

# Ligne horizontale à 95.5 %
plt.axhline(y=95.5, color="red", linestyle="--", linewidth=2, label="Seuil de changement acceptable")

# Lignes verticales à 0, 130, 260, 390 s
for x in [0, 130, 260, 390]:
    plt.axvline(x=x, color="gray", linestyle=":", linewidth=2)

plt.xlabel("Temps (s)")
plt.ylabel("Fraction de C₀ (%)")
plt.title("Évolution de la fraction de C₀ dans chaque puits et le système")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()
