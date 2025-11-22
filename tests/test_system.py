import unittest
from nebulo.membership import TriangularMF
from nebulo.variables import FuzzyVariable
from nebulo.rules import FuzzyRule
from nebulo.system import FuzzySystem

class TestFuzzySystem(unittest.TestCase):

    def setUp(self):
        # Set up a fuzzy system for testing
        self.consumption = FuzzyVariable("weekly_consumption")
        self.consumption.add_term("low", TriangularMF(0, 0, 200))
        self.consumption.add_term("medium", TriangularMF(150, 400, 600))
        self.consumption.add_term("high", TriangularMF(500, 700, 1000))

        self.trend = FuzzyVariable("trend")
        self.trend.add_term("decreasing", TriangularMF(-500, -200, 0))
        self.trend.add_term("stable", TriangularMF(-50, 0, 50))
        self.trend.add_term("increasing", TriangularMF(0, 200, 500))

        self.system = FuzzySystem(mode="sugeno")
        self.system.add_variable(self.consumption)
        self.system.add_variable(self.trend)

        # Define rules
        rule1 = FuzzyRule([("weekly_consumption", "high"), ("trend", "increasing")], 100)
        rule2 = FuzzyRule([("weekly_consumption", "low"), ("trend", "decreasing")], 0)
        self.system.add_rule(rule1)
        self.system.add_rule(rule2)

    def test_sugeno_evaluation(self):
        inputs = {"weekly_consumption": 600, "trend": 150}
        output = self.system.evaluate(inputs)
        self.assertAlmostEqual(output, 100, places=1)

    def test_mamdani_evaluation(self):
        mamdani_system = FuzzySystem(mode="mamdani")
        mamdani_system.add_variable(self.consumption)
        mamdani_system.add_variable(self.trend)

        rule_m1 = FuzzyRule([("weekly_consumption", "high"), ("trend", "increasing")], "alert")
        rule_m2 = FuzzyRule([("weekly_consumption", "low"), ("trend", "decreasing")], "normal")
        mamdani_system.add_rule(rule_m1)
        mamdani_system.add_rule(rule_m2)

        inputs = {"weekly_consumption": 600, "trend": 150}
        output = mamdani_system.evaluate(inputs)
        self.assertIn("alert", output)

if __name__ == '__main__':
    unittest.main()