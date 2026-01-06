import numpy as np
import matplotlib.pyplot as plt
from nebulo.membership import TriangularMF
from nebulo.variables import FuzzyVariable
from nebulo.rules import FuzzyRule
from nebulo.system import FuzzySystem

# --- 1. Definirea Variabilelor Fuzzy ---

# Variabila de Intrare 1: Buget Lunar (x1)
buget_lunar = FuzzyVariable("Buget_Lunar")
buget_lunar.add_term("scazut", TriangularMF(0, 1000, 2000))
buget_lunar.add_term("mediu", TriangularMF(1000, 3000, 5000))
buget_lunar.add_term("ridicat", TriangularMF(3000, 5000, 5000))

# Variabila de Intrare 2: Cost Actual (x2)
cost_actual = FuzzyVariable("Cost_Actual")
cost_actual.add_term("mic", TriangularMF(0, 500, 1500))
cost_actual.add_term("moderat", TriangularMF(500, 2500, 4500))
cost_actual.add_term("mare", TriangularMF(3500, 5000, 5000))

# --- 2. Crearea Sistemului Fuzzy Sugeno (Ordin 0) ---

system_sugeno = FuzzySystem(mode="sugeno")
system_sugeno.add_variable(buget_lunar)
system_sugeno.add_variable(cost_actual)

# --- 3. Definirea și Adăugarea Regulilor (Tabele de Reguli) ---
# Consecințele sunt valori constante (0, 50, 100)

rules = [
    FuzzyRule([("Buget_Lunar", "scazut"), ("Cost_Actual", "mic")], 0),      # Scazut & Mic -> Risc Scazut
    FuzzyRule([("Buget_Lunar", "scazut"), ("Cost_Actual", "moderat")], 50), # Scazut & Moderat -> Risc Mediu
    FuzzyRule([("Buget_Lunar", "scazut"), ("Cost_Actual", "mare")], 100),    # Scazut & Mare -> Risc Ridicat

    FuzzyRule([("Buget_Lunar", "mediu"), ("Cost_Actual", "mic")], 0),       # Mediu & Mic -> Risc Scazut
    FuzzyRule([("Buget_Lunar", "mediu"), ("Cost_Actual", "moderat")], 50),  # Mediu & Moderat -> Risc Mediu
    FuzzyRule([("Buget_Lunar", "mediu"), ("Cost_Actual", "mare")], 100),     # Mediu & Mare -> Risc Ridicat

    FuzzyRule([("Buget_Lunar", "ridicat"), ("Cost_Actual", "mic")], 0),    # Ridicat & Mic -> Risc Scazut
    FuzzyRule([("Buget_Lunar", "ridicat"), ("Cost_Actual", "moderat")], 0), # Ridicat & Moderat -> Risc Scazut
    FuzzyRule([("Buget_Lunar", "ridicat"), ("Cost_Actual", "mare")], 50),   # Ridicat & Mare -> Risc Mediu
]

for rule in rules:
    system_sugeno.add_rule(rule)

# --- 4. Evaluare (Exemplu) ---
inputs_test = {"Buget_Lunar": 4000, "Cost_Actual": 3000}
risc_evaluat = system_sugeno.evaluate(inputs_test)
print(f"Pentru Buget Lunar de 4000 și Cost Actual de 3000, Risc-ul (y) este: {risc_evaluat:.2f}")

# --- 5. Vizualizarea Funcțiilor de Apartenență 2D ---

# -----------------------------------
# Grafic 1: Buget Lunar (x1)
# -----------------------------------
fig, ax = plt.subplots(figsize=(8, 4))
x_plot = np.linspace(0, 5000, 1000) # Gama de valori pentru plotare

# Parcurgeți termenii lingvistici și funcțiile lor de apartenență
for term_name, mf in buget_lunar.terms.items():
    # mf.evaluate(x_plot) returnează gradul de apartenență pentru fiecare punct din x_plot
    y_plot = [mf.evaluate(x) for x in x_plot]
    ax.plot(x_plot, y_plot, label=term_name.capitalize())

ax.set_title(r'Funcțiile de Apartenență pentru Buget Lunar ($x_1$)')
ax.set_xlabel('Buget (Unități Monetare)')
ax.set_ylabel('Grad de Apartenență $\mu(x_1)$')
ax.set_ylim(0, 1.1)
ax.legend()
ax.grid(True, linestyle='--')

# -----------------------------------
# Grafic 2: Cost Actual (x2)
# -----------------------------------
fig, ax = plt.subplots(figsize=(8, 4))
# Folosim aceeași gamă x_plot (0-5000)
for term_name, mf in cost_actual.terms.items():
    y_plot = [mf.evaluate(x) for x in x_plot]
    ax.plot(x_plot, y_plot, label=term_name.capitalize())

ax.set_title(r'Funcțiile de Apartenență pentru Cost Actual ($x_2$)')
ax.set_xlabel('Cost (Unități Monetare)')
ax.set_ylabel('Grad de Apartenență $\mu(x_2)$')
ax.set_ylim(0, 1.1)
ax.legend()
ax.grid(True, linestyle='--')

# Reafisăm plot-ul
plt.show()

# --- 6. Reprezentarea Suprafaței de Decizie (Matplotlib) ---

# Crearea grilei de puncte pentru Buget și Cost
x1_range = np.linspace(0, 5000, 30)  # Buget Lunar
x2_range = np.linspace(0, 5000, 30)  # Cost Actual
X1, X2 = np.meshgrid(x1_range, x2_range)
Z = np.zeros_like(X1)

# Calcularea ieșirii pentru fiecare punct din grilă
for i in range(X1.shape[0]):
    for j in range(X1.shape[1]):
        inputs = {"Buget_Lunar": X1[i, j], "Cost_Actual": X2[i, j]}
        Z[i, j] = system_sugeno.evaluate(inputs)

# Reprezentarea 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plotează suprafața
surf = ax.plot_surface(X1, X2, Z, cmap='viridis', edgecolor='none')

ax.set_xlabel('Buget Lunar (x1)')
ax.set_ylabel('Cost Actual (x2)')
ax.set_zlabel('Nivel de Risc (y)')
ax.set_title('Suprafața de Decizie a Sistemului Fuzzy Sugeno')
fig.colorbar(surf, shrink=0.5, aspect=5, label='Nivel de Risc (0-100)')

plt.show()

print("\n--- Analiză Suplimentară ---")
# Voi efectua o rulare (testare) mai detaliată
buget_scazut_cost_mare = system_sugeno.evaluate({"Buget_Lunar": 1000, "Cost_Actual": 4500})
print(f"Risc pentru Buget 1000 (Scăzut) și Cost 4500 (Mare): {buget_scazut_cost_mare:.2f} (Aproape 100)")

buget_ridicat_cost_mic = system_sugeno.evaluate({"Buget_Lunar": 4500, "Cost_Actual": 500})
print(f"Risc pentru Buget 4500 (Ridicat) și Cost 500 (Mic): {buget_ridicat_cost_mic:.2f} (Aproape 0)")

# --- 7. Tabel cu 20 de rulări (Conform cerinței 3 din imagine) ---
import pandas as pd 

print("\n--- Tabel 20 Rulări (Date pentru documentație) ---")

date_tabel = []
for i in range(20):
    # Generăm valori aleatorii pentru a testa spectrul sistemului
    x1_val = np.random.uniform(500, 5000)
    x2_val = np.random.uniform(500, 5000)
    
    y_val = system_sugeno.evaluate({"Buget_Lunar": x1_val, "Cost_Actual": x2_val})
    
    date_tabel.append({
        "Rulare": i + 1,
        "x1 (Buget)": round(x1_val, 2),
        "x2 (Cost)": round(x2_val, 2),
        "y (Risc)": round(y_val, 2)
    })

df = pd.DataFrame(date_tabel)
print(df.to_string(index=False))
# df.to_csv("date_sistem_fuzzy.csv", index=False) # Opțional: salvează în Excel/CSV

# --- 8. Sistem cu Buclă de Reacție (Feedback Loop) și Auto-Ajustare ---
iteratii = 20
buget_curent = 1200   # x1 inițial (Scăzut)
cost_curent = 1000    # x2 inițial (Mic)

istoric_cost = []
istoric_risc = []
istoric_buget = []

for t in range(iteratii):
    # 1. Evaluăm riscul la pasul curent
    risc = system_sugeno.evaluate({"Buget_Lunar": buget_curent, "Cost_Actual": cost_curent})
    
    # Salvează datele
    istoric_risc.append(risc)
    istoric_cost.append(cost_curent)
    istoric_buget.append(buget_curent)
    
    # 2. Logica de feedback (Reacția sistemului)
    # Costul crește constant cu 200 unități (inflație/consum)
    cost_curent = min(cost_curent + 250, 5000)
    
    # REACȚIE: Dacă riscul detectat este mare (> 40), mărim bugetul pentru a compensa
    if risc > 40:
        buget_curent = min(buget_curent + 400, 5000)
    # Dacă riscul este foarte mic, putem reduce bugetul (optimizare)
    elif risc < 10:
        buget_curent = max(buget_curent - 100, 500)

# --- 9. Graficul Evoluției în Timp (Sistem cu buclă de reacție) ---
plt.figure(figsize=(12, 6))
plt.plot(istoric_risc, 'r-o', linewidth=2, label='Ieșire: Nivel Risc (y)')
plt.plot(istoric_cost, 'b-s', alpha=0.6, label='Intrare 1: Evoluție Cost (x2)')
plt.plot(istoric_buget, 'g-^', alpha=0.6, label='Intrare 2: Ajustare Buget (x1)')

plt.title("Analiza Sistemului în Buclă Închisă (Feedback Control)")
plt.xlabel("Iterații (Timp)")
plt.ylabel("Valoare / Procent Risc")
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)
plt.show()