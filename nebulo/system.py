from .variables import FuzzyVariable
from .rules import FuzzyRule

class FuzzySystem:
    def __init__(self, mode="sugeno"):
        """
        mode: 'sugeno' or 'mamdani'
        """
        self.variables = {}
        self.rules = []
        self.mode = mode

    def add_variable(self, variable: FuzzyVariable):
        self.variables[variable.name] = variable

    def add_rule(self, rule: FuzzyRule):
        self.rules.append(rule)

    def evaluate(self, inputs: dict):
            fuzzified = {var: self.variables[var].fuzzify(inputs[var]) for var in inputs}

            if self.mode == "sugeno":
                weighted_sum = 0
                weight_total = 0
                for r in self.rules:
                    w = r.activation(fuzzified)
                    z = r.eval_output(inputs)
                    weighted_sum += w * z
                    weight_total += w
                return weighted_sum / weight_total if weight_total != 0 else 0
            else:  # Mamdani
                output_degrees = {}
                for r in self.rules:
                    w = r.activation(fuzzified)
                    # Presupunem că eval_output returnează (variabila, eticheta)
                    _, label = r.eval_output() 
                    output_degrees[label] = max(output_degrees.get(label, 0), w)
                
                # Defuzzificare prin Centrul Mediilor (Centroid approximation)
                numerator = 0
                denominator = 0
                # Identificăm variabila de ieșire (Risc)
                out_var = [v for v in self.variables.values() if v.name.startswith("Risc")][0]
                
                for label, activation in output_degrees.items():
                    if activation > 0:
                        # Folosim parametrul 'b' (vârful triunghiului) ca reprezentant
                        center = out_var.terms[label].b 
                        numerator += activation * center
                        denominator += activation
                
                return numerator / denominator if denominator != 0 else 0