#! python3
# progression.py - Arithmetic and geometric progressions.

from abc import ABCMeta
from abc import abstractmethod


class Progression(metaclass=ABCMeta):
    """Abstract class for progressions."""

    def __init__(self, initial_term, ratio):
        """Initializes a Progression instance."""
        self.ratio = ratio
        self.terms = {1: initial_term}

    @staticmethod
    def _check_index(n):
        """If the index is not allowed, throws IndexError exception."""
        if n < 1:
            raise IndexError('index must be greater than or equal to 1')

    @abstractmethod
    def _nth_term(self, n):
        """Calculates the nth term."""
        pass

    @staticmethod
    @abstractmethod
    def get_ratio(term_1, term_2):
        """Returns the ratio between two terms."""
        pass

    @abstractmethod
    def sum_first_terms(self, n):
        """Returns the sum of n first terms."""
        pass

    def n_first_terms(self, n):
        """Returns the n first terms."""
        self._check_index(n)
        terms = list()

        for i in range(1, (n + 1)):
            terms.append(self.nth_term(i))

        return terms

    def nth_term(self, n):
        """Returns the nth term."""
        self._check_index(n)

        try:
            return self.terms[n]
        except KeyError:
            return self._nth_term(n)


class ArithmeticProgression(Progression):
    """Class for arithmetic progression."""

    @staticmethod
    def get_ratio(term_1, term_2):
        """Returns the ratio between two terms."""
        return term_2 - term_1

    @staticmethod
    def is_arithmetic(sequence, tolerance=1e-10):
        """Checks whether a sequence is a arithmetic progression."""
        sequence_size = len(sequence)

        if sequence_size < 3:
            raise TypeError('sequence should contain at least 3 items')

        diff = sequence[1] - sequence[0]

        for i in range(2, sequence_size):
            curr_diff = sequence[i] - sequence[i - 1]

            if abs(curr_diff - diff) > tolerance:
                return False

        return True

    def _nth_term(self, n):
        """Calculates the nth term."""
        self.terms[n] = self.terms[1] + (n - 1)*self.ratio
        return self.terms[n]

    def sum_first_terms(self, n):
        """Returns the sum of n first terms."""
        self._check_index(n)
        return n*(self.terms[1] + self.nth_term(n)) / 2


class GeometricProgression(Progression):
    """Class for geometric progression."""

    @staticmethod
    def get_ratio(term_1, term_2):
        """Returns the ratio between two terms."""
        return term_2 / term_1

    @staticmethod
    def is_geometric(sequence, tolerance=1e-10):
        """Checks whether a sequence is a geometric progression."""
        sequence_size = len(sequence)

        if sequence_size < 3:
            raise TypeError('sequence should contain at least 3 items')

        ratio = sequence[1] / sequence[0]

        for i in range(2, sequence_size):
            curr_ratio = sequence[i] / sequence[i - 1]

            if abs(curr_ratio - ratio) > tolerance:
                return False

        return True

    def _nth_term(self, n):
        """Calculates the nth term."""
        self.terms[n] = self.terms[1]*(self.ratio**(n - 1))
        return self.terms[n]

    def sum_first_terms(self, n):
        """Returns the sum of n first terms."""
        self._check_index(n)

        if self.ratio == 1:
            return n*self.terms[1]

        return self.terms[1]*(1 - self.ratio**n) / (1 - self.ratio)
