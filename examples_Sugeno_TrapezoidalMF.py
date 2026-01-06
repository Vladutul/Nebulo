import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from nebulo.membership import TrapezoidalMF
from nebulo.variables import FuzzyVariable
from nebulo.rules import FuzzyRule
from nebulo.system import FuzzySystem

# --- 1. Definirea Variabilelor (Intrări Triunghiulare, Ieșire Sugeno) ---
buget_lunar = FuzzyVariable("Buget_Lunar")
buget_lunar.add_term("scazut", TrapezoidalMF(0, 0, 1000, 2000))
buget_lunar.add_term("mediu", TrapezoidalMF(1000, 2500, 3500, 5000))
buget_lunar.add_term("ridicat", TrapezoidalMF(3000, 4500, 5000, 5000))

cost_actual = FuzzyVariable("Cost_Actual")
cost_actual.add_term("mic", TrapezoidalMF(0, 0, 500, 1500))
cost_actual.add_term("moderat", TrapezoidalMF(500, 2000, 3000, 4500))
cost_actual.add_term("mare", TrapezoidalMF(3500, 4500, 5000, 5000))

# Definim sistemul Sugeno
system_sugeno = FuzzySystem(mode="sugeno")
system_sugeno.add_variable(buget_lunar)
system_sugeno.add_variable(cost_actual)

# Reguli cu consecințe constante (0, 50, 100)
rules = [
    FuzzyRule([("Buget_Lunar", "scazut"), ("Cost_Actual", "mic")], 0),
    FuzzyRule([("Buget_Lunar", "scazut"), ("Cost_Actual", "moderat")], 50),
    FuzzyRule([("Buget_Lunar", "scazut"), ("Cost_Actual", "mare")], 100),
    FuzzyRule([("Buget_Lunar", "mediu"), ("Cost_Actual", "mic")], 0),
    FuzzyRule([("Buget_Lunar", "mediu"), ("Cost_Actual", "moderat")], 50),
    FuzzyRule([("Buget_Lunar", "mediu"), ("Cost_Actual", "mare")], 100),
    FuzzyRule([("Buget_Lunar", "ridicat"), ("Cost_Actual", "mic")], 0),
    FuzzyRule([("Buget_Lunar", "ridicat"), ("Cost_Actual", "moderat")], 0),
    FuzzyRule([("Buget_Lunar", "ridicat"), ("Cost_Actual", "mare")], 50),
]
for rule in rules:
    system_sugeno.add_rule(rule)

# --- 2. Date pentru Feedback și Suprafață ---
iteratii = 15
buget, cost = 1200, 1000
h_risc, h_cost, h_buget = [], [], []
for t in range(iteratii):
    r_eval = system_sugeno.evaluate({"Buget_Lunar": buget, "Cost_Actual": cost})
    h_risc.append(r_eval)
    h_cost.append(cost)
    h_buget.append(buget)
    cost = min(cost + 300, 5000)
    if r_eval > 40: buget = min(buget + 500, 5000)

x1_range = np.linspace(0, 5000, 25)
x2_range = np.linspace(0, 5000, 25)
X1, X2 = np.meshgrid(x1_range, x2_range)
Z = np.array([[system_sugeno.evaluate({"Buget_Lunar": x, "Cost_Actual": y}) for x in x1_range] for y in x2_range])

# --- 3. CREAREA PLOTULUI UNIFICAT (6 ZONE) ---
fig = plt.figure(figsize=(18, 10))
plt.subplots_adjust(hspace=0.4, wspace=0.3)

# Subplot 1: MF Buget
ax1 = fig.add_subplot(2, 3, 1)
x_plot = np.linspace(0, 5000, 500)
for term, mf in buget_lunar.terms.items():
    ax1.plot(x_plot, [mf.evaluate(x) for x in x_plot], label=term.capitalize())
ax1.set_title("MF: Buget Lunar ($x_1$)")
ax1.legend(); ax1.grid(True, alpha=0.3)

# Subplot 2: MF Cost
ax2 = fig.add_subplot(2, 3, 2)
for term, mf in cost_actual.terms.items():
    ax2.plot(x_plot, [mf.evaluate(x) for x in x_plot], label=term.capitalize(), linestyle='--')
ax2.set_title("MF: Cost Actual ($x_2$)")
ax2.legend(); ax2.grid(True, alpha=0.3)

# Subplot 3: Ieșire Sugeno (Nivel Risc - VALORI CONSTANTE)
ax3 = fig.add_subplot(2, 3, 3)
output_values = [0, 50, 100]
labels = ["Scăzut (0)", "Mediu (50)", "Ridicat (100)"]
# Desenăm linii verticale (Stem) pentru a arăta că ieșirea Sugeno e discretă
markerline, stemlines, baseline = ax3.stem(output_values, [1, 1, 1], linefmt='r--', markerfmt='ro')
plt.setp(markerline, markersize=10)
ax3.set_xticks(output_values)
ax3.set_xticklabels(labels)
ax3.set_ylim(0, 1.2)
ax3.set_title("Ieșire Sugeno: Nivel Risc ($y$)")
ax3.grid(True, axis='x', alpha=0.5)

# Subplot 4: Suprafața de Decizie 3D
ax4 = fig.add_subplot(2, 3, (4, 5), projection='3d')
surf = ax4.plot_surface(X1, X2, Z, cmap='viridis', edgecolor='none')
ax4.set_title('Suprafața de Decizie Sugeno')
ax4.set_xlabel('Buget')
ax4.set_ylabel('Cost')
fig.colorbar(surf, ax=ax4, shrink=0.5, aspect=10)

# Subplot 5: Evoluție Feedback
ax5 = fig.add_subplot(2, 3, 6)
ax5.plot(h_risc, 'r-o', linewidth=2, label='Risc (y)')
ax5.plot(np.array(h_cost)/50, 'b--', alpha=0.7, label='Cost/50')
ax5.plot(np.array(h_buget)/50, 'g:', alpha=0.7, label='Buget/50')
ax5.set_title("Evoluție Feedback")
ax5.set_xlabel("Iterație")
ax5.legend(); ax5.grid(True, linestyle='--')

plt.suptitle("Dashboard Sistem Fuzzy Sugeno - Analiză Risc Bugetar", fontsize=18, fontweight='bold')
plt.show()