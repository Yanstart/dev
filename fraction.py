class NegativeDenominatorError(Exception):
   """Exception raised when denominator is negative"""
   pass


class ZeroDenominatorError(Exception):
    """Exception raised when denominator is zero"""
    pass


def _gcd(a, b):
    """Calculate GCD using Euclidean algorithm
    PRE: a, b sont des entiers (int)
    POST: retourne le PGCD de a et b
    """
    while b:
        a, b = b, a % b
    return abs(a)


class Fraction:
    """Class representing a fraction and operations on it

    Author : V. Van den Schrieck
    Date : October 2021
    This class allows fraction manipulations through several operations.
    """

    def __init__(self, num=0, den=1):
        """This builds a fraction based on some numerator and denominator.
        PRE: num, den sont des entiers (int), den != 0
        POST: crée une fraction réduite avec num comme numérateur et den comme dénominateur
        RAISES: ZeroDenominatorError si den == 0
        """
        if den == 0:
            raise ZeroDenominatorError("Le dénominateur ne peut pas être zéro")

        if den < 0:
            num, den = -num, -den

        gcd = _gcd(num, den)
        self._num = num // gcd
        self._den = den // gcd

    @property
    def numerator(self):
        """Getter pour le numérateur
        PRE: -
        POST: retourne le numérateur de la fraction
        """
        return self._num

    @property
    def denominator(self):
        """Getter pour le dénominateur
        PRE: -
        POST: retourne le dénominateur de la fraction
        """
        return self._den

    def __str__(self):
        """Return a textual representation of the reduced form of the fraction
        PRE: -
        POST: retourne une chaîne "num/den" de la fraction réduite
        """
        if self._den == 1:
            return str(self._num)
        return f"{self._num}/{self._den}"

    def as_mixed_number(self):
        """Return a textual representation of the reduced form of the fraction as a mixed number
        PRE: -
        POST: retourne une chaîne représentant le nombre mixte (ex: "2 + 1/4" pour 9/4)
        """
        abs_num = abs(self._num)
        abs_den = abs(self._den)
        sign = "-" if self._num * self._den < 0 else ""

        quotient = abs_num // abs_den
        remainder = abs_num % abs_den

        if remainder == 0:
            return f"{sign}{quotient}"
        if quotient == 0:
            return str(self)
        return f"{sign}{quotient} + {remainder}/{abs_den}"

    def __add__(self, other):
        """Overloading of the + operator for fractions
        PRE: other est Fraction ou int
        POST: retourne une nouvelle Fraction = self + other
        """
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self._num * other._den + other._num * self._den,
                        self._den * other._den)

    def __sub__(self, other):
        """Overloading of the - operator for fractions
        PRE: other est Fraction ou int
        POST: retourne une nouvelle Fraction = self - other
        """
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self._num * other._den - other._num * self._den,
                        self._den * other._den)

    def __mul__(self, other):
        """Overloading of the * operator for fractions
        PRE: other est Fraction ou int
        POST: retourne une nouvelle Fraction = self * other
        """
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self._num * other._num, self._den * other._den)

    def __truediv__(self, other):
        """Overloading of the / operator for fractions
        PRE: other est Fraction ou int, et non nul
        POST: retourne une nouvelle Fraction = self / other
        RAISES: ZeroDenominatorError si other == 0
        """
        if isinstance(other, int):
            if other == 0:
                raise ZeroDenominatorError("Division par zéro")
            other = Fraction(other)
        if other._num == 0:
            raise ZeroDenominatorError("Division par zéro")
        return Fraction(self._num * other._den, self._den * other._num)

    def __pow__(self, other):
        """Overloading of the ** operator for fractions
        PRE: other est un entier positif ou nul
        POST: retourne une nouvelle Fraction = self ** other
        """
        if not isinstance(other, int) or other < 0:
            raise ValueError("L'exposant doit être un entier positif ou nul")
        return Fraction(self._num ** other, self._den ** other)

    def __eq__(self, other):
        """Overloading of the == operator for fractions
        PRE: other est Fraction ou int
        POST: retourne True si les fractions sont égales, False sinon
        """
        if isinstance(other, int):
            other = Fraction(other)
        return self._num * other._den == other._num * self._den

    def __float__(self):
        """Returns the decimal value of the fraction
        PRE: -
        POST: retourne la valeur décimale (float) de la fraction
        """
        return self._num / self._den

    def is_zero(self):
        """Check if a fraction's value is 0
        PRE: -
        POST: retourne True si la fraction vaut 0, False sinon
        """
        return self._num == 0

    def is_integer(self):
        """Check if a fraction is integer
        PRE: -
        POST: retourne True si la fraction est un entier, False sinon
        """
        return self._den == 1

    def is_proper(self):
        """Check if the absolute value of the fraction is < 1
        PRE: -
        POST: retourne True si |fraction| < 1, False sinon
        """
        return abs(self._num) < abs(self._den)

    def is_unit(self):
        """Check if a fraction is a unit fraction
        PRE: -
        POST: retourne True si la fraction est une fraction unitaire (numérateur = ±1 et dénominateur > 1)
        """
        return abs(self._num) == 1 and self._den > 1

    def is_adjacent_to(self, other):
        """Check if two fractions differ by a unit fraction
        PRE: other est une Fraction
        POST: retourne True si |self - other| = 1
        """
        if not isinstance(other, Fraction):
            return False
        diff = abs(self - other)
        return diff == Fraction(1)  # Check if difference is exactly 1

    def __abs__(self):
        """Return the absolute value of the fraction
        PRE: -
        POST: retourne la valeur absolue de la fraction sous forme de nouvelle Fraction
        """
        return Fraction(abs(self._num), self._den)
# TODO : [BONUS] You can overload other operators (ex : <, >, ...)

    def __lt__(self, other):
        """Overloading of the < operator for fractions
        PRE: other est Fraction ou int
        POST: retourne True si self < other, False sinon
        """
        if isinstance(other, int):
            other = Fraction(other)
        return self._num * other._den < other._num * self._den

    def __le__(self, other):
        """Overloading of the <= operator for fractions
        PRE: other est Fraction ou int
        POST: retourne True si self <= other, False sinon
        """
        if isinstance(other, int):
            other = Fraction(other)
        return self._num * other._den <= other._num * self._den

    def __gt__(self, other):
        """Overloading of the > operator for fractions
        PRE: other est Fraction ou int
        POST: retourne True si self > other, False sinon
        """
        if isinstance(other, int):
            other = Fraction(other)
        return self._num * other._den > other._num * self._den

    def __ge__(self, other):
        """Overloading of the >= operator for fractions
        PRE: other est Fraction ou int
        POST: retourne True si self >= other, False sinon
        """
        if isinstance(other, int):
            other = Fraction(other)
        return self._num * other._den >= other._num * self._den