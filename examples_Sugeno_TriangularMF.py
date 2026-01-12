import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from nebulo.membership import TriangularMF
from nebulo.variables import FuzzyVariable
from nebulo.rules import FuzzyRule
from nebulo.system import FuzzySystem

# --- 1. Definirea Variabilelor (Triunghiulare - Configurație Densă) ---
buget_lunar = FuzzyVariable("Buget_Lunar")
buget_lunar.add_term("v_scazut", TriangularMF(0, 0, 1000))
buget_lunar.add_term("scazut", TriangularMF(500, 1250, 2000))
buget_lunar.add_term("mediu", TriangularMF(1500, 2500, 3500))
buget_lunar.add_term("ridicat", TriangularMF(3000, 3750, 4500))
buget_lunar.add_term("v_ridicat", TriangularMF(4000, 5000, 5000))

cost_actual = FuzzyVariable("Cost_Actual")
cost_actual.add_term("v_mic", TriangularMF(0, 0, 1000))
cost_actual.add_term("mic", TriangularMF(500, 1250, 2000))
cost_actual.add_term("moderat", TriangularMF(1500, 2500, 3500))
cost_actual.add_term("mare", TriangularMF(3000, 3750, 4500))
cost_actual.add_term("critic", TriangularMF(4000, 5000, 5000))

system_sugeno = FuzzySystem(mode="sugeno")
system_sugeno.add_variable(buget_lunar)
system_sugeno.add_variable(cost_actual)

matrice_risc = [
    [30, 60, 85, 95, 100], # Buget: v_scazut -> risc mare chiar și la cost mic
    [10, 40, 70, 90, 100], # Buget: scazut
    [0,  20, 50, 80, 95],  # Buget: mediu
    [0,  10, 30, 60, 85],  # Buget: ridicat
    [0,  0,  15, 40, 70]   # Buget: v_ridicat -> risc mic chiar și la cost mare
]

buget_terms = ["v_scazut", "scazut", "mediu", "ridicat", "v_ridicat"]
cost_terms = ["v_mic", "mic", "moderat", "mare", "critic"]

rules = []
for i, b_t in enumerate(buget_terms):
    for j, c_t in enumerate(cost_terms):
        # Extragem valoarea din matricea de mai sus
        scor_risc = matrice_risc[i][j]
        rules.append(FuzzyRule([(buget_lunar.name, b_t), (cost_actual.name, c_t)], scor_risc))

# Curățăm regulile vechi și le adăugăm pe cele noi
system_sugeno.rules = [] # Resetare reguli pentru a evita duplicatele
for rule in rules:
    system_sugeno.add_rule(rule)

# --- 2. Simulare Feedback și Calcul Suprafață ---
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

x1_range = np.linspace(0, 5000, 30)
x2_range = np.linspace(0, 5000, 30)
X1, X2 = np.meshgrid(x1_range, x2_range)
Z = np.array([[system_sugeno.evaluate({"Buget_Lunar": x, "Cost_Actual": y}) for x in x1_range] for y in x2_range])

# --- 3. Vizualizare ---
fig = plt.figure(figsize=(18, 10))
plt.subplots_adjust(hspace=0.4, wspace=0.3)

# MF Ploturi (x1, x2) conform template
for i, (var, label) in enumerate([(buget_lunar, "x1: Buget"), (cost_actual, "x2: Cost")]):
    ax = fig.add_subplot(2, 3, i+1)
    x_p = np.linspace(0, 5000, 500)
    for term, mf in var.terms.items():
        ax.plot(x_p, [mf.evaluate(x) for x in x_p], label=term.capitalize())
    ax.set_title(f"Intrare {label}")
    ax.legend()

# Subplot 3: Singleton-urile Sugeno
ax3 = fig.add_subplot(2, 3, 3)
ax3.stem([0, 50, 100], [1, 1, 1], linefmt='r--', markerfmt='ro', basefmt=" ")
ax3.set_xticks([0, 50, 100])
ax3.set_xticklabels(["Scăzut (0)", "Mediu (50)", "Ridicat (100)"])
ax3.set_title("Ieșire Sugeno ($y$)")
ax3.set_ylim(0, 1.2)

# Subplot 3D: Suprafața f(x1, x2)
ax4 = fig.add_subplot(2, 3, (4, 5), projection='3d')
surf = ax4.plot_surface(X1, X2, Z, cmap='viridis', edgecolor='none', alpha=0.9)
ax4.set_title('Suprafața de Decizie Sugeno')
ax4.set_xlabel('x1: Buget')
ax4.set_ylabel('x2: Cost')
ax4.set_zlabel('y: Risc')
ax4.view_init(elev=30, azim=220) 
fig.colorbar(surf, ax=ax4, shrink=0.5, label='Nivel Risc')

# Subplot Evoluție
ax5 = fig.add_subplot(2, 3, 6)
ax5.plot(h_risc, 'r-o', linewidth=2, label='Risc (y)')
ax5.plot(np.array(h_buget)/50, 'g--', label='x1: Buget/50')
ax5.plot(np.array(h_cost)/50, 'b:', label='x2: Cost/50')
ax5.set_title("Evoluție Feedback")
ax5.set_xlabel("Iterație")
ax5.legend()
ax5.grid(True, alpha=0.3)

plt.suptitle("Analiza Sistemului Fuzzy Sugeno (Triunghiular)", fontsize=18, fontweight='bold')
plt.show()