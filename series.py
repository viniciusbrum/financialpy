#! python3
# series.py - Uniform series of payments.

from progression import GeometricProgression


class UniformSeriesPayment(object):
    """Class for uniform series of payments."""

    def __init__(self, interest_rate, periods, first_payment):
        """Initializes a UniformSeriesPayment instance."""
        if first_payment not in (0, 1):
            raise TypeError('first payment must be 0 or 1')

        self.interest_rate = interest_rate
        self.periods = periods
        self.first_payment = first_payment
        self._ratio = 1 / (1 + interest_rate)
        self._payment = None
        self._present_value = None
        self._progression = None

    def payment(self, present_value, tolerance=0.01):
        """Calculates the fixed payment according to the present value."""
        if (self._present_value is not None
                and abs(present_value - self._present_value) <= tolerance):
            return self._payment

        self._present_value = present_value
        self._payment = self._calc_payment(present_value, self.interest_rate,
                                           self.periods, self.first_payment)
        self._progression = GeometricProgression(self._payment, self._ratio)
        return self._payment

    def present_value(self, payment, tolerance=0.01):
        """Calculates the present value according to the fixed payment."""
        if (self._payment is not None
                and abs(payment - self._payment) <= tolerance):
            return self._present_value

        self._payment = payment
        self._progression = GeometricProgression(payment, self._ratio)
        self._present_value = self._progression.sum_first_terms(self.periods)

        if self.first_payment == 1:
            self._present_value = self._present_value * self._ratio

        return self._present_value

    @staticmethod
    def _calc_payment(pv, i, n, k):
        factor = (1 / (1 + i)) if k == 0 else 1
        return pv * ((i * (1 + i)**n) / ((1 + i)**n - 1)) * factor
