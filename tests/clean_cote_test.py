import unittest

from src.clean_cote import CoteCleaner


class ManuscritsTest(unittest.TestCase):
    def test_fr(self):
        input, expected = "fr. 96", "Français 96"
        pc = CoteCleaner.clean(input=input)
        actual = pc.idno
        self.assertEqual(actual, expected)
        self.assertEqual(pc.dept, "Manuscrits")

        input, expected = "fr 96", "Français 96"
        actual = CoteCleaner.clean(input=input).idno
        self.assertEqual(actual, expected)
        self.assertEqual(pc.dept, "Manuscrits")

    def test_francais(self):
        input, expected = "Paris, BNF, français 1598", "Français 1598"
        pc = CoteCleaner.clean(input=input)
        actual = pc.idno
        self.assertEqual(actual, expected)
        self.assertEqual(pc.dept, "Manuscrits")

    def test_arsenal(self):
        input, expected = "Arsenal 2985", "Ms-2985"
        pc = CoteCleaner.clean(input=input)
        actual = pc.idno
        self.assertEqual(actual, expected)
        self.assertEqual(pc.dept, "Arsenal")


if __name__ == "__main__":
    unittest.main()
