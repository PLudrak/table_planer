import unittest
from guest_manager import Guest, Table


class TestGuest(unittest.TestCase):

    def test_single_guest_with_surname(self):
        g = Guest("Anna Kowalska")
        self.assertFalse(g.pair)
        self.assertEqual(g.persons, [{"name": "Anna", "surname": "Kowalska"}])
        self.assertTrue(g.one_family)
        self.assertEqual(g.family_name, "Kowalska")
        self.assertEqual(g.display_name, "Anna K.")

    def test_single_guest_without_surname(self):
        g = Guest("Anna")
        self.assertFalse(g.pair)
        self.assertEqual(g.persons, [{"name": "Anna", "surname": None}])
        self.assertFalse(g.one_family)
        self.assertEqual(g.display_name, "Anna")

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
        self.assertEqual(g.display_name, "Anna i Piotr N.")

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
        self.assertEqual(g.display_name, "Anna K. i Piotr N.")

    def test_pair_without_surnames(self):
        g = Guest("Anna i Piotr")
        self.assertTrue(g.pair)
        self.assertEqual(
            g.persons,
            [{"name": "Anna", "surname": None}, {"name": "Piotr", "surname": None}],
        )
        self.assertFalse(g.one_family)
        self.assertEqual(g.display_name, "Anna i Piotr")

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

    def test_pair_with_acompanying(self):
        g = Guest("Anna Kowalska i osoba towarzysząca")
        self.assertTrue(g.pair)
        self.assertEqual(
            g.persons,
            [
                {"name": "Anna", "surname": "Kowalska"},
                {"name": "Osoba towarzysząca", "surname": None},
            ],
        )
        self.assertTrue(g.one_family)
        self.assertEqual(g.family_name, "Kowalska")
        self.assertEqual(g.display_name, "Anna K.+1")


class TableTest(unittest.TestCase):
    def test_create_default_table(self):
        t = Table()
        self.assertEqual(t.type, "square")

    def test_create_round_table(self):
        t = Table("round")
        self.assertEqual(t.max_seats, 12)

    def test_create_square_table(self):
        t = Table("square")
        self.assertEqual(t.max_seats, 60)

    def test_add_pair_to_round_table(self):
        t = Table("round")
        g = Guest("Anna i Jan Kowalski")
        t.add_guest(g)
        self.assertEqual(t.occupied_seats, 2)
        self.assertEqual(t.free_seats, 10)

    def test_add_single_to_round_table(self):
        t = Table("round")
        g = Guest("Jan Kowalski")
        t.add_guest(g)
        self.assertEqual(t.occupied_seats, 1)
        self.assertEqual(t.free_seats, 11)

    def test_add_pair_to_almost_full_table(self):
        t = Table("round")
        g = Guest("Anna i Jan Kowalski")
        t.occupied_seats = 11
        t.add_guest(g)
        self.assertEqual(t.occupied_seats, 11)
        self.assertNotIn(g, t.guests)

    def test_add_single_to_almost_full_table(self):
        t = Table("round")
        g = Guest("Jan Kowalski")
        t.occupied_seats = 11
        t.add_guest(g)
        self.assertEqual(t.occupied_seats, 12)
        self.assertIn(g, t.guests)


if __name__ == "__main__":
    unittest.main()
