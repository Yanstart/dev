import unittest
from fraction import Fraction, ZeroDenominatorError, NegativeDenominatorError

class TestFraction(unittest.TestCase):
    def setUp(self):
        """Initialisation des fractions utilisées dans plusieurs tests"""
        self.f1 = Fraction(1, 2)  # fraction 1/2
        self.f2 = Fraction(2, 3)  # fraction 2/3
        self.f3 = Fraction(-1, 2)  # fraction négative
        self.f4 = Fraction(2, 4)  # fraction non réduite
        self.f5 = Fraction(0, 1)  # fraction nulle
        self.f6 = Fraction(5, 1)  # fraction entière

        # Tests de base
        self.assertTrue(self.f1.is_unit())  # 1/2 est une fraction unitaire
        self.assertFalse(self.f2.is_unit())  # 2/3 n'est pas une fraction unitaire

        # Test avec des fractions unitaires
        self.assertTrue(Fraction(1, 5).is_unit())  # 1/5 est une fraction unitaire
        self.assertTrue(Fraction(-1, 5).is_unit())  # -1/5 est une fraction unitaire

        # Test avec d'autres cas
        self.assertFalse(Fraction(2, 1).is_unit())  # 2 n'est pas une fraction unitaire
        self.assertFalse(Fraction(0, 1).is_unit())  # 0 n'est pas une fraction unitaire

    def test_init(self):
        """Test du constructeur et de la réduction des fractions"""
        # Test constructeur basique
        f = Fraction(1, 2)
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)

        # Test réduction automatique
        f = Fraction(2, 4)
        self.assertEqual(str(f), "1/2")

        # Test conversion des fractions négatives
        f = Fraction(1, -2)
        self.assertEqual(str(f), "-1/2")
        f = Fraction(-1, -2)
        self.assertEqual(str(f), "1/2")

        # Test constructeur avec numérateur seul
        f = Fraction(3)
        self.assertEqual(str(f), "3")

        # Test des exceptions
        with self.assertRaises(ZeroDenominatorError):
            Fraction(1, 0)

    def test_str(self):
        """Test de la représentation en chaîne"""
        self.assertEqual(str(self.f1), "1/2")
        self.assertEqual(str(self.f6), "5")  # cas entier
        self.assertEqual(str(self.f5), "0")  # cas zéro
        self.assertEqual(str(self.f3), "-1/2")  # cas négatif

    def test_as_mixed_number(self):
        """Test de la représentation en nombre mixte"""
        f = Fraction(5, 2)
        self.assertEqual(f.as_mixed_number(), "2 + 1/2")
        self.assertEqual(self.f1.as_mixed_number(), "1/2")  # Pas de partie entière
        self.assertEqual(self.f6.as_mixed_number(), "5")    # Entier pur
        self.assertEqual(self.f5.as_mixed_number(), "0")    # Zéro
        f = Fraction(-7, 2)
        self.assertEqual(f.as_mixed_number(), "-3 + 1/2")   # Cas négatif

    def test_add(self):
        """Test de l'addition"""
        # Addition de fractions
        result = self.f1 + self.f2
        self.assertEqual(str(result), "7/6")

        # Addition avec un entier
        result = self.f1 + 1
        self.assertEqual(str(result), "3/2")

        # Addition avec zéro
        result = self.f1 + self.f5
        self.assertEqual(str(result), "1/2")

    def test_sub(self):
        """Test de la soustraction"""
        # Soustraction de fractions
        result = self.f2 - self.f1
        self.assertEqual(str(result), "1/6")

        # Soustraction avec un entier
        result = self.f1 - 1
        self.assertEqual(str(result), "-1/2")

        # Soustraction donnant zéro
        result = self.f1 - self.f1
        self.assertEqual(str(result), "0")

    def test_mul(self):
        """Test de la multiplication"""
        # Multiplication de fractions
        result = self.f1 * self.f2
        self.assertEqual(str(result), "1/3")

        # Multiplication par un entier
        result = self.f1 * 2
        self.assertEqual(str(result), "1")

        # Multiplication par zéro
        result = self.f1 * self.f5
        self.assertEqual(str(result), "0")

    def test_truediv(self):
        """Test de la division"""
        # Division de fractions
        result = self.f1 / self.f2
        self.assertEqual(str(result), "3/4")

        # Division par un entier
        result = self.f1 / 2
        self.assertEqual(str(result), "1/4")

        # Test des exceptions
        with self.assertRaises(ZeroDenominatorError):
            self.f1 / 0
        with self.assertRaises(ZeroDenominatorError):
            self.f1 / self.f5

    def test_pow(self):
        """Test de l'élévation à la puissance"""
        # Puissance 0
        result = self.f1 ** 0
        self.assertEqual(str(result), "1")

        # Puissance 1
        result = self.f1 ** 1
        self.assertEqual(str(result), "1/2")

        # Puissance 2
        result = self.f1 ** 2
        self.assertEqual(str(result), "1/4")

        # Test des exceptions
        with self.assertRaises(ValueError):
            self.f1 ** (-1)
        with self.assertRaises(ValueError):
            self.f1 ** 1.5

    def test_eq(self):
        """Test de l'égalité"""
        # Égalité de fractions identiques
        self.assertTrue(self.f1 == Fraction(1, 2))

        # Égalité de fractions équivalentes
        self.assertTrue(self.f1 == self.f4)

        # Égalité avec un entier
        self.assertTrue(self.f6 == 5)

        # Inégalité
        self.assertFalse(self.f1 == self.f2)

    def test_float(self):
        """Test de la conversion en float"""
        self.assertEqual(float(self.f1), 0.5)
        self.assertEqual(float(self.f5), 0.0)
        self.assertEqual(float(self.f6), 5.0)
        self.assertEqual(float(self.f3), -0.5)

    def test_is_zero(self):
        """Test de la méthode is_zero"""
        self.assertTrue(self.f5.is_zero())
        self.assertFalse(self.f1.is_zero())
        self.assertFalse(self.f3.is_zero())

    def test_is_integer(self):
        """Test de la méthode is_integer"""
        self.assertTrue(self.f6.is_integer())
        self.assertFalse(self.f1.is_integer())
        self.assertTrue(Fraction(0).is_integer())

    def test_is_proper(self):
        """Test de la méthode is_proper"""
        self.assertTrue(self.f1.is_proper())
        self.assertFalse(self.f6.is_proper())
        self.assertTrue(self.f3.is_proper())  # fraction négative
        self.assertTrue(self.f5.is_proper())  # zéro

    def test_is_unit(self):
        """Test de la méthode is_unit"""
        self.assertTrue(self.f1.is_unit())  # 1/2 est une fraction unitaire
        self.assertTrue(Fraction(1, 5).is_unit())
        self.assertTrue(Fraction(-1, 5).is_unit())  # cas négatif
        self.assertFalse(self.f2.is_unit())  # 2/3 n'est pas une fraction unitaire
        self.assertFalse(self.f5.is_unit())  # zéro
        self.assertFalse(Fraction(1, 1).is_unit())  # pas une fraction unitaire

    def test_abs(self):
        """Test de la méthode abs"""
        self.assertEqual(abs(Fraction(-1, 2)), Fraction(1, 2))
        self.assertEqual(abs(Fraction(1, 2)), Fraction(1, 2))
        self.assertEqual(abs(Fraction(0)), Fraction(0))

    def test_comparison_operators(self):
        """Test des opérateurs de comparaison"""
        # Test
        self.assertTrue(self.f1 < self.f6)  # 1/2 < 5
        self.assertFalse(self.f6 < self.f1)  # 5 > 1/2
        self.assertTrue(self.f1 < 1)  # 1/2 < 1

        # Test <=
        self.assertTrue(self.f1 <= self.f6)  # 1/2 <= 5
        self.assertTrue(self.f1 <= self.f4)  # 1/2 <= 2/4 (equal)
        self.assertFalse(self.f6 <= self.f1)  # 5 > 1/2

        # Test >
        self.assertTrue(self.f6 > self.f1)  # 5 > 1/2
        self.assertFalse(self.f1 > self.f6)  # 1/2 < 5
        self.assertTrue(self.f6 > 4)  # 5 > 4

        # Test >=
        self.assertTrue(self.f6 >= self.f1)  # 5 >= 1/2
        self.assertTrue(self.f1 >= self.f4)  # 1/2 >= 2/4 (equal)
        self.assertFalse(self.f1 >= self.f6)  # 1/2 < 5

        # Additional test cases for better coverage
        self.assertFalse(Fraction(0) > self.f1)  # 0 > 1/2
        self.assertTrue(Fraction(0) < self.f1)  # 0 < 1/2
        self.assertTrue(self.f5 <= 0)  # 0 <= 0
        self.assertTrue(self.f5 >= 0)  # 0 >= 0

if __name__ == '__main__':
    unittest.main()