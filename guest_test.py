import unittest
from guest_manager import Guest


class TestGuest(unittest.TestCase):

    def test_single_guest_with_surname(self):
        g = Guest("Anna Kowalska")
        self.assertFalse(g.pair)
        self.assertEqual(g.persons, [{"name": "Anna", "surname": "Kowalska"}])
        self.assertTrue(g.one_family)
        self.assertEqual(g.family_name, "Kowalska")

    def test_single_guest_without_surname(self):
        g = Guest("Anna")
        self.assertFalse(g.pair)
        self.assertEqual(g.persons, [{"name": "Anna", "surname": None}])
        self.assertFalse(g.one_family)

    def test_pair_same_surname(self):
        g = Guest("Anna Nowak i Piotr Nowak")
        self.assertTrue(g.pair)
        self.assertEqual(
            g.persons,
            [
                {"name": "Anna", "surname": "Nowak"},
                {"name": "Piotr", "surname": "Nowak"},
            ],
        )
        self.assertTrue(g.one_family)
        self.assertEqual(g.family_name, "Nowak")

    def test_pair_different_surnames(self):
        g = Guest("Anna Kowalska i Piotr Nowak")
        self.assertTrue(g.pair)
        self.assertEqual(
            g.persons,
            [
                {"name": "Anna", "surname": "Kowalska"},
                {"name": "Piotr", "surname": "Nowak"},
            ],
        )
        self.assertFalse(g.one_family)
        self.assertEqual(g.family_name, "Kowalska, Nowak")

    def test_pair_without_surnames(self):
        g = Guest("Anna i Piotr")
        self.assertTrue(g.pair)
        self.assertEqual(
            g.persons,
            [{"name": "Anna", "surname": None}, {"name": "Piotr", "surname": None}],
        )
        self.assertFalse(g.one_family)

    def test_whitespace_handling(self):
        g = Guest("  Anna Kowalska   i   Piotr Nowak  ")
        self.assertEqual(
            g.persons,
            [
                {"name": "Anna", "surname": "Kowalska"},
                {"name": "Piotr", "surname": "Nowak"},
            ],
        )
        self.assertEqual(g.family_name, "Kowalska, Nowak")


if __name__ == "__main__":
    unittest.main()
