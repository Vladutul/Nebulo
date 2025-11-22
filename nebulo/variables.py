from .membership import MembershipFunction

class FuzzyVariable:
    def __init__(self, name):
        self.name = name
        self.terms = {}  # {"low": MF, "medium": MF, ...}
        
    def add_term(self, term_name, mf: MembershipFunction):
        self.terms[term_name] = mf
        
    def fuzzify(self, value):
        return {term: mf.evaluate(value) for term, mf in self.terms.items()}