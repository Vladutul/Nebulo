import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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

# --- DIFERENȚA MAMDANI: Variabila de Ieșire (y) ---
# În Mamdani, ieșirea are funcții de apartenență, nu doar numere fixe.
risc = FuzzyVariable("Risc") 
risc.add_term("scazut", TriangularMF(0, 0, 40))
risc.add_term("mediu", TriangularMF(30, 50, 70))
risc.add_term("ridicat", TriangularMF(60, 100, 100))

# --- 2. Crearea Sistemului Fuzzy Mamdani ---

system_mamdani = FuzzySystem(mode="mamdani")
system_mamdani.add_variable(buget_lunar)
system_mamdani.add_variable(cost_actual)
system_mamdani.add_variable(risc) # Adăugăm variabila redenumită

# --- 3. Definirea și Adăugarea Regulilor ---
# Consecințele sunt acum termenii lingvistici definiți în Risc

rules = [
    FuzzyRule([("Buget_Lunar", "scazut"), ("Cost_Actual", "mic")], ("Risc", "scazut")),
    FuzzyRule([("Buget_Lunar", "scazut"), ("Cost_Actual", "moderat")], ("Risc", "mediu")),
    FuzzyRule([("Buget_Lunar", "scazut"), ("Cost_Actual", "mare")], ("Risc", "ridicat")),

    FuzzyRule([("Buget_Lunar", "mediu"), ("Cost_Actual", "mic")], ("Risc", "scazut")),
    FuzzyRule([("Buget_Lunar", "mediu"), ("Cost_Actual", "moderat")], ("Risc", "mediu")),
    FuzzyRule([("Buget_Lunar", "mediu"), ("Cost_Actual", "mare")], ("Risc", "ridicat")),

    FuzzyRule([("Buget_Lunar", "ridicat"), ("Cost_Actual", "mic")], ("Risc", "scazut")),
    FuzzyRule([("Buget_Lunar", "ridicat"), ("Cost_Actual", "moderat")], ("Risc", "scazut")),
    FuzzyRule([("Buget_Lunar", "ridicat"), ("Cost_Actual", "mare")], ("Risc", "mediu")),
]

for rule in rules:
    system_mamdani.add_rule(rule)

# --- 4. Evaluare ---
inputs_test = {"Buget_Lunar": 4000, "Cost_Actual": 3000}
risc_evaluat = system_mamdani.evaluate(inputs_test)
print(f"MAMDANI: Pentru Buget 4000 și Cost 3000, Risc-ul este: {risc_evaluat:.2f}")

# --- 5. Vizualizarea Funcțiilor de Apartenență (Inclusiv Ieșirea) ---

def plot_mf(variable, title, xlabel):
    fig, ax = plt.subplots(figsize=(8, 3))
    x_plot = np.linspace(0, 5000 if "Risc" not in title else 100, 1000)
    for term_name, mf in variable.terms.items():
        y_plot = [mf.evaluate(x) for x in x_plot]
        ax.plot(x_plot, y_plot, label=term_name.capitalize())
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Grad de Apartenență')
    ax.legend()
    ax.grid(True, linestyle='--')
    plt.show()

plot_mf(buget_lunar, "Buget Lunar (x1)", "Buget")
plot_mf(cost_actual, "Cost Actual (x2)", "Cost")
plot_mf(risc, "Nivel de Risc (Ieșire Mamdani)", "Procent Risc")

# --- 6. Reprezentarea Suprafaței de Decizie ---

x1_range = np.linspace(0, 5000, 20)
x2_range = np.linspace(0, 5000, 20)
X1, X2 = np.meshgrid(x1_range, x2_range)
Z = np.zeros_like(X1)

for i in range(X1.shape[0]):
    for j in range(X1.shape[1]):
        Z[i, j] = system_mamdani.evaluate({"Buget_Lunar": X1[i, j], "Cost_Actual": X2[i, j]})

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X1, X2, Z, cmap='plasma', edgecolor='none')
ax.set_title('Suprafața de Decizie Mamdani')
fig.colorbar(surf, label='Nivel Risc')
plt.show()

# --- 7. Tabel 20 Rulări ---
date_tabel = []
for i in range(20):
    x1, x2 = np.random.uniform(0, 5000), np.random.uniform(0, 5000)
    y = system_mamdani.evaluate({"Buget_Lunar": x1, "Cost_Actual": x2})
    date_tabel.append({"Rulare": i+1, "x1": round(x1, 2), "x2": round(x2, 2), "y (Risc)": round(y, 2)})

print("\n--- Tabel Rulări Mamdani ---")
print(pd.DataFrame(date_tabel).to_string(index=False))

# --- 8. Buclă de Reacție (Feedback) ---
iteratii = 15
buget, cost = 1200, 1000
h_risc, h_cost, h_buget = [], [], []

for t in range(iteratii):
    risc = system_mamdani.evaluate({"Buget_Lunar": buget, "Cost_Actual": cost})
    h_risc.append(risc)
    h_cost.append(cost)
    h_buget.append(buget)
    
    cost = min(cost + 300, 5000)
    if risc > 45: # Prag de reacție
        buget = min(buget + 500, 5000)
    elif risc < 15:
        buget = max(buget - 200, 500)

plt.figure(figsize=(10, 5))
plt.plot(h_risc, 'r-o', label='Risc (y)')
plt.plot(np.array(h_cost)/50, 'b--', label='Cost (x2) / 50') # Scalat pt vizibilitate
plt.plot(np.array(h_buget)/50, 'g--', label='Buget (x1) / 50')
plt.title("Evoluție Feedback - Sistem Mamdani")
plt.legend()
plt.grid(True)
plt.show()