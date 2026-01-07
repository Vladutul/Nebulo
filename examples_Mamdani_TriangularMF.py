import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from nebulo.membership import TriangularMF  # Folosim TriangularMF
from nebulo.variables import FuzzyVariable
from nebulo.rules import FuzzyRule
from nebulo.system import FuzzySystem

# --- 1. Definirea Variabilelor și Sistemului (Identic ca denumiri, format Triangular) ---
buget_lunar = FuzzyVariable("Buget_Lunar")
# Parametri TriangularMF: (start, peak, end)
buget_lunar.add_term("scazut", TriangularMF(0, 0, 2500))
buget_lunar.add_term("mediu", TriangularMF(1000, 2500, 5000))
buget_lunar.add_term("ridicat", TriangularMF(3000, 5000, 5000))

cost_actual = FuzzyVariable("Cost_Actual")
cost_actual.add_term("mic", TriangularMF(0, 0, 2000))
cost_actual.add_term("moderat", TriangularMF(1000, 2000, 4500))
cost_actual.add_term("mare", TriangularMF(3500, 5000, 5000))

risc_var = FuzzyVariable("Risc") 
risc_var.add_term("scazut", TriangularMF(0, 0, 45))
risc_var.add_term("mediu", TriangularMF(30, 50, 70))
risc_var.add_term("ridicat", TriangularMF(60, 100, 100))

system_mamdani = FuzzySystem(mode="mamdani")
system_mamdani.add_variable(buget_lunar)
system_mamdani.add_variable(cost_actual)
system_mamdani.add_variable(risc_var)

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

# --- 2. Pregătirea Datelor pentru Ploturi (Păstrat neschimbat) ---
iteratii = 15
buget, cost = 1200, 1000
h_risc, h_cost, h_buget = [], [], []
for t in range(iteratii):
    r_eval = system_mamdani.evaluate({"Buget_Lunar": buget, "Cost_Actual": cost})
    h_risc.append(r_eval)
    h_cost.append(cost)
    h_buget.append(buget)
    cost = min(cost + 300, 5000)
    if r_eval > 45: buget = min(buget + 500, 5000)
    elif r_eval < 15: buget = max(buget - 200, 500)

x1_range = np.linspace(0, 5000, 20)
x2_range = np.linspace(0, 5000, 20)
X1, X2 = np.meshgrid(x1_range, x2_range)
Z = np.array([[system_mamdani.evaluate({"Buget_Lunar": x, "Cost_Actual": y}) for x in x1_range] for y in x2_range])

# --- 3. Crearea Plotului Unificat (Identic cu Template-ul) ---
fig = plt.figure(figsize=(16, 10))
plt.subplots_adjust(hspace=0.4, wspace=0.3)

ax1 = fig.add_subplot(2, 3, 1)
x_plot = np.linspace(0, 5000, 500)
for term, mf in buget_lunar.terms.items():
    ax1.plot(x_plot, [mf.evaluate(x) for x in x_plot], label=term.capitalize())
ax1.set_title("MF: Buget Lunar (x1)")
ax1.set_xlabel("x1 (Buget)")
ax1.legend()

ax2 = fig.add_subplot(2, 3, 2)
for term, mf in cost_actual.terms.items():
    ax2.plot(x_plot, [mf.evaluate(x) for x in x_plot], label=term.capitalize())
ax2.set_title("MF: Cost Actual (x2)")
ax2.set_xlabel("x2 (Cost)")
ax2.legend()

ax3 = fig.add_subplot(2, 3, 3)
x_plot_risc = np.linspace(0, 100, 500)
for term, mf in risc_var.terms.items():
    ax3.plot(x_plot_risc, [mf.evaluate(x) for x in x_plot_risc], label=term.capitalize())
ax3.set_title("MF: Nivel Risc (y)")
ax3.set_xlabel("y (Risc)")
ax3.legend()

ax4 = fig.add_subplot(2, 3, (4, 5), projection='3d')
surf = ax4.plot_surface(X1, X2, Z, cmap='plasma', edgecolor='none')
ax4.set_title('Suprafața de Decizie Mamdani')
ax4.set_xlabel('x1 (Buget)')
ax4.set_ylabel('x2 (Cost)')
ax4.set_zlabel('y (Risc)')
fig.colorbar(surf, ax=ax4, shrink=0.5, aspect=10, label='y (Risc)')

ax5 = fig.add_subplot(2, 3, 6)
ax5.plot(h_risc, 'r-o', label='Risc (y)')
ax5.plot(np.array(h_cost)/50, 'b--', label='Cost/50 (x2)')
ax5.plot(np.array(h_buget)/50, 'g--', label='Buget/50 (x1)')
ax5.set_title("Evoluție Feedback")
ax5.set_xlabel("Iterație")
ax5.legend()
ax5.grid(True, linestyle='--')

plt.suptitle("Analiza Sistemului Fuzzy Mamdani (Triunghiular)", fontsize=16)
plt.show()