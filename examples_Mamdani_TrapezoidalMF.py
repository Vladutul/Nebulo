import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from nebulo.membership import TrapezoidalMF 
from nebulo.variables import FuzzyVariable
from nebulo.rules import FuzzyRule
from nebulo.system import FuzzySystem

# --- 1. Definirea Variabilelor (Trapezoidal) ---
buget_lunar = FuzzyVariable("Buget_Lunar")
buget_lunar.add_term("scazut", TrapezoidalMF(0, 0, 800, 2200))
buget_lunar.add_term("mediu", TrapezoidalMF(1200, 2500, 3500, 4800))
buget_lunar.add_term("ridicat", TrapezoidalMF(3500, 4500, 5000, 5000))

cost_actual = FuzzyVariable("Cost_Actual")
cost_actual.add_term("mic", TrapezoidalMF(0, 0, 600, 1800))
cost_actual.add_term("moderat", TrapezoidalMF(800, 2000, 3000, 4200))
cost_actual.add_term("mare", TrapezoidalMF(3200, 4200, 5000, 5000))

risc = FuzzyVariable("Risc") 
risc.add_term("scazut", TrapezoidalMF(0, 0, 20, 45))
risc.add_term("mediu", TrapezoidalMF(30, 45, 55, 75))
risc.add_term("ridicat", TrapezoidalMF(60, 85, 100, 100))

# --- 2. Crearea Sistemului ---
system_mamdani = FuzzySystem(mode="mamdani")
for var in [buget_lunar, cost_actual, risc]: system_mamdani.add_variable(var)

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
for rule in rules: system_mamdani.add_rule(rule)

# --- 3. Plot Unificat (Toate într-o singură fereastră) ---
fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Arhitectura Sistemului Fuzzy Mamdani (Trapezoidal)', fontsize=16, fontweight='bold')

# Plot Buget (Sus-Stânga)
x_buget = np.linspace(0, 5000, 1000)
for name, mf in buget_lunar.terms.items():
    axs[0, 0].plot(x_buget, [mf.evaluate(x) for x in x_buget], label=name, linewidth=2)
axs[0, 0].set_title('Intrare: Buget Lunar')
axs[0, 0].legend()
axs[0, 0].grid(True, alpha=0.3)

# Plot Cost (Sus-Dreapta)
x_cost = np.linspace(0, 5000, 1000)
for name, mf in cost_actual.terms.items():
    axs[0, 1].plot(x_cost, [mf.evaluate(x) for x in x_cost], label=name, linewidth=2)
axs[0, 1].set_title('Intrare: Cost Actual')
axs[0, 1].legend()
axs[0, 1].grid(True, alpha=0.3)

# Plot Risc (Jos-Stânga)
x_risc = np.linspace(0, 100, 1000)
for name, mf in risc.terms.items():
    axs[1, 0].plot(x_risc, [mf.evaluate(x) for x in x_risc], label=name, linewidth=2, color='tab:red' if 'ridicat' in name else None)
axs[1, 0].set_title('Ieșire: Nivel de Risc')
axs[1, 0].legend()
axs[1, 0].grid(True, alpha=0.3)

# Plot Suprafață 3D (Jos-Dreapta)
from mpl_toolkits.mplot3d import Axes3D
axs[1, 1].remove() # Ștergem axa 2D standard
ax3d = fig.add_subplot(2, 2, 4, projection='3d')
X1, X2 = np.meshgrid(np.linspace(0, 5000, 20), np.linspace(0, 5000, 20))
Z = np.array([[system_mamdani.evaluate({"Buget_Lunar": x, "Cost_Actual": y}) for x in np.linspace(0, 5000, 20)] for y in np.linspace(0, 5000, 20)])
surf = ax3d.plot_surface(X1, X2, Z, cmap='viridis', edgecolor='none')
ax3d.set_title('Suprafața de Decizie')
fig.colorbar(surf, ax=ax3d, shrink=0.5, aspect=10)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# --- 4. Tabel și Feedback (Același cod ca înainte) ---
print("\nSistemul a fost generat cu succes. Toate graficele sunt acum vizibile într-o singură fereastră.")