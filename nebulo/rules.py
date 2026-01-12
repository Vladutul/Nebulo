class FuzzyRule:
    """Generic rule, can be Sugeno or Mamdani"""
    def __init__(self, conditions, output):
        """
        conditions: list of (var_name, term_name)
        output: numeric (Sugeno) or fuzzy term name (Mamdani)
        """
        self.conditions = conditions
        self.output = output

    def activation(self, fuzzified_inputs):
        degrees = [fuzzified_inputs[var][term] for var, term in self.conditions]
        return min(degrees)

    def eval_output(self, inputs=None):
        if callable(self.output):
            return self.output(inputs)
        return self.output