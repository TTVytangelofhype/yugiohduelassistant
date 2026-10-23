import unittest
from engine import battle_damage, deck_statistics, checklist

class EngineTests(unittest.TestCase):
    def test_attack_damage(self):
        self.assertEqual(battle_damage(3000,2500)["opponent"],500)
    def test_defense_damage(self):
        self.assertEqual(battle_damage(1500,2500,"Defense")["you"],1000)
    def test_deck_counts(self):
        self.assertEqual(deck_statistics({"main":{"A":3},"extra":{"B":1}})["main"],3)
    def test_checklist(self):
        self.assertIn("Opponent",checklist("A","B","","","C","Battle"))
if __name__ == "__main__":
    unittest.main()
