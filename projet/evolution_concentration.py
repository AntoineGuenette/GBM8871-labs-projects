import pandas as pd
import matplotlib.pyplot as plt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
path_fichier = os.path.join(script_dir, "data", "concentrations.csv")

# Charger le CSV original
df = pd.read_csv(
    path_fichier,
    comment='%',
)

# Utilisation de noms de colonnes plus simples
df.columns = [
    "time_s",
    "c0_puits_1_pct",
    "c0_puits_2_pct",
    "c0_puits_3_pct",
    "c0_systeme_pct"
]

# Ajouter les valeur initiales au données existantes
nouvelle_ligne = pd.DataFrame({
    "time_s": [0],
    "c0_puits_1_pct": [10],
    "c0_puits_2_pct": [10],
    "c0_puits_3_pct": [10],
    "c0_systeme_pct": [10.5]
})
df = pd.concat([nouvelle_ligne, df], ignore_index=True)

# Sauvegarder le CSV modifié
path_fichier_modifie = os.path.join(script_dir, "data", "concentrations_modifie.csv")
df.to_csv(path_fichier_modifie, index=False)

# Tracer le graphique
plt.figure(figsize=(8, 5))

# Évolutions de concentration
plt.plot(df["time_s"], df["c0_puits_1_pct"], label="Puits 1", color="tab:blue")
plt.plot(df["time_s"], df["c0_puits_2_pct"], label="Puits 2", color="tab:pink")
plt.plot(df["time_s"], df["c0_puits_3_pct"], label="Puits 3", color="tab:green")
plt.plot(df["time_s"], df["c0_systeme_pct"], label="Système", color="tab:purple")

# Ligne de seuil de changement acceptable
plt.axhline(y=95.5, color="red", linestyle="--", linewidth=2, label="Seuil de changement acceptable")

# Lignes délimitant les changements de milieu
for x in [0, 130, 260, 390]:
    plt.axvline(x=x, color="gray", linestyle=":", linewidth=2)

plt.xlabel("Temps (s)")
plt.ylabel("Fraction de C₀ (%)")
plt.title("Évolution de la fraction de C₀ dans chaque puits et le système")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()
