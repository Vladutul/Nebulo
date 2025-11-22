# Example of using Nebulo - directly runnable

from nebulo.membership import TriangularMF
from nebulo.variables import FuzzyVariable
from nebulo.rules import FuzzyRule
from nebulo.system import FuzzySystem
from nebulo.utils import compute_weekly_trend

# -----------------------------
# Define fuzzy variables

# Weekly Consumption
consumption = FuzzyVariable("weekly_consumption")
consumption.add_term("low", TriangularMF(0, 0, 200))
consumption.add_term("medium", TriangularMF(150, 400, 600))
consumption.add_term("high", TriangularMF(500, 700, 1000))

# Weekly Trend
trend = FuzzyVariable("trend")
trend.add_term("decreasing", TriangularMF(-500, -200, 0))
trend.add_term("stable", TriangularMF(-50, 0, 50))
trend.add_term("increasing", TriangularMF(0, 200, 500))

# -----------------------------
# Sugeno System

system_sugeno = FuzzySystem(mode="sugeno")
system_sugeno.add_variable(consumption)
system_sugeno.add_variable(trend)

# Sugeno Rules
rule1 = FuzzyRule([("weekly_consumption","high"),("trend","increasing")], 100)  # alert max
rule2 = FuzzyRule([("weekly_consumption","low"),("trend","decreasing")], 0)     # normal
system_sugeno.add_rule(rule1)
system_sugeno.add_rule(rule2)

# Evaluate Sugeno
inputs = {"weekly_consumption": 600, "trend": 150}
print("Sugeno output:", system_sugeno.evaluate(inputs))

# -----------------------------
# Mamdani System

system_mamdani = FuzzySystem(mode="mamdani")
system_mamdani.add_variable(consumption)
system_mamdani.add_variable(trend)

# Mamdani Rules
rule_m1 = FuzzyRule([("weekly_consumption","high"),("trend","increasing")], "alert")
rule_m2 = FuzzyRule([("weekly_consumption","low"),("trend","decreasing")], "normal")
system_mamdani.add_rule(rule_m1)
system_mamdani.add_rule(rule_m2)

# Evaluate Mamdani
print("Mamdani output:", system_mamdani.evaluate(inputs))

# -----------------------------
# Weekly Trend Example
previous_week = 400
current_week = 600
trend_value = compute_weekly_trend(current_week, previous_week)
print("Weekly trend:", trend_value)