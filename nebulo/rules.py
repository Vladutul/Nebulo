class FuzzyRule:
    """Generic rule, can be Sugeno or Mamdani"""
    def __init__(self, conditions, output):
        """
        conditions: list of (var_name, term_name)
        output: numeric (Sugeno) or fuzzy term name (Mamdani)
        """
        self.conditions = conditions
        self.output = output  # constant/function (Sugeno) or fuzzy label (Mamdani)

    def activation(self, fuzzified_inputs):
        degrees = [fuzzified_inputs[var][term] for var, term in self.conditions]
        return min(degrees)  # AND logic, can be extended to OR/product

    def eval_output(self, inputs=None):
        if callable(self.output):  # Sugeno
            return self.output(inputs)
        return self.output  # Mamdani