#! python3
# series.py - Uniform series of payments.

from interest import CompoundInterest
from progression import GeometricProgression


class UniformSeriesPayment(object):
    """Class for uniform series of payments."""

    def __init__(self, interest_rate, periods, first_payment):
        """Initializes a UniformSeriesPayment instance."""
        if first_payment not in (0, 1):
            raise TypeError('first payment must be 0 or 1')

        self.interest_rate = interest_rate
        self.periods = periods # TODO: perpetuity?
        self.first_payment = first_payment # TODO: deferred?
        self._interest_system = CompoundInterest
        self._progression_ratio = self._interest_system.reduction_factor(
            interest_rate, 1)
        self._future_value = None
        self._payment = None
        self._present_value = None
        self._progression = None

    def accumulation_factor(self):
        """Calculates the accumulation factor."""
        return self._accumulation_factor(self.interest_rate, self.periods,
                                         self.first_payment,
                                         self._interest_system)

    def capital_recovery_factor(self):
        """Calculates the capital recovery factor."""
        return self._capital_recovery_factor(self.interest_rate, self.periods,
                                             self.first_payment,
                                             self._interest_system)

    def future_value(self, payment, tolerance=0.01):
        """Calculates the future value according to the fixed payment."""
        if (self._payment is not None
                and abs(payment - self._payment) <= tolerance):
            return self._future_value

        self._payment = payment
        self._progression = GeometricProgression(payment,
                                                 self._progression_ratio)
        self._future_value = self._fv_by_pmt(payment, self.interest_rate,
                                             self.periods, self.first_payment,
                                             self._interest_system)
        self._present_value = self._interest_system.present_value(
            self._future_value, interest_rate=self.interest_rate,
            periods=self.periods)
        return self._future_value

    def payment_by_present_value(self, present_value, tolerance=0.01):
        """Calculates the fixed payment according to the present value."""
        if (self._present_value is not None
                and abs(present_value - self._present_value) <= tolerance):
            return self._payment

        self._present_value = present_value
        self._future_value = self._interest_system.future_value(
            present_value, interest_rate=self.interest_rate,
            periods=self.periods)
        self._payment = self._pmt_by_pv(present_value, self.interest_rate,
                                        self.periods, self.first_payment,
                                        self._interest_system)
        self._progression = GeometricProgression(self._payment,
                                                 self._progression_ratio)
        return self._payment

    def payment_by_future_value(self, future_value, tolerance=0.01):
        """Calculates the fixed payment according to the future value."""
        if (self._future_value is not None
                and abs(future_value - self._future_value) <= tolerance):
            return self._payment

        self._future_value = future_value
        self._present_value = self._interest_system.present_value(
            future_value, interest_rate=self.interest_rate,
            periods=self.periods)
        self._payment = self._pmt_by_fv(future_value, self.interest_rate,
                                        self.periods, self.first_payment,
                                        self._interest_system)
        self._progression = GeometricProgression(self._payment,
                                                 self._progression_ratio)
        return self._payment

    def present_value(self, payment, tolerance=0.01):
        """Calculates the present value according to the fixed payment."""
        if (self._payment is not None
                and abs(payment - self._payment) <= tolerance):
            return self._present_value

        self._payment = payment
        self._progression = GeometricProgression(payment,
                                                 self._progression_ratio)
        self._present_value = self._progression.sum_first_terms(self.periods)

        if self.first_payment == 1:
            self._present_value = self._present_value * self._progression_ratio

        self._future_value = self._interest_system.future_value(
            self._present_value, interest_rate=self.interest_rate,
            periods=self.periods)
        return self._present_value

    def present_worth_factor(self):
        """Calculates the present worth factor."""
        return self._present_worth_factor(self.interest_rate, self.periods,
                                          self.first_payment,
                                          self._interest_system)

    def sinking_fund_factor(self):
        """Calculates the sinking fund factor."""
        return self._sinking_fund_factor(self.interest_rate, self.periods,
                                         self.first_payment,
                                         self._interest_system)

    @staticmethod
    def _accumulation_factor(i, n, k, int_sys):
        accum_factor_n = int_sys.accumulation_factor(i, n)
        accum_factor_1 = int_sys.accumulation_factor(i, 1)
        k_factor = accum_factor_1 if k == 0 else 1
        return ((accum_factor_n - 1) / i) * k_factor

    @staticmethod
    def _capital_recovery_factor(i, n, k, int_sys):
        accum_factor_n = int_sys.accumulation_factor(i, n)
        reduc_factor_1 = int_sys.reduction_factor(i, 1)
        k_factor = reduc_factor_1 if k == 0 else 1
        return ((accum_factor_n * i) / (accum_factor_n - 1)) * k_factor

    @staticmethod
    def _fv_by_pmt(pmt, i, n, k, int_sys):
        accum_factor_n = int_sys.accumulation_factor(i, n)
        accum_factor_1 = int_sys.accumulation_factor(i, 1)
        k_factor = accum_factor_1 if k == 0 else 1
        return pmt * ((accum_factor_n - 1) / i) * k_factor

    @staticmethod
    def _pmt_by_fv(fv, i, n, k, int_sys):
        accum_factor_n = int_sys.accumulation_factor(i, n)
        reduc_factor_1 = int_sys.reduction_factor(i, 1)
        k_factor = reduc_factor_1 if k == 0 else 1
        return fv * (i / (accum_factor_n - 1)) * k_factor

    @staticmethod
    def _pmt_by_pv(pv, i, n, k, int_sys):
        accum_factor_n = int_sys.accumulation_factor(i, n)
        reduc_factor_1 = int_sys.reduction_factor(i, 1)
        k_factor = reduc_factor_1 if k == 0 else 1
        return pv * ((i * accum_factor_n) / (accum_factor_n - 1)) * k_factor

    @staticmethod
    def _present_worth_factor(i, n, k, int_sys):
        accum_factor_n = int_sys.accumulation_factor(i, n)
        accum_factor_1 = int_sys.accumulation_factor(i, 1)
        k_factor = accum_factor_1 if k == 0 else 1
        return ((accum_factor_n - 1) / (i * accum_factor_n)) * k_factor

    @staticmethod
    def _pv_by_pmt(pmt, i, n, k, int_sys):
        accum_factor_n = int_sys.accumulation_factor(i, n)
        accum_factor_1 = int_sys.accumulation_factor(i, 1)
        k_factor = accum_factor_1 if k == 0 else 1
        return pmt * ((accum_factor_n - 1) / (i * accum_factor_n)) * k_factor

    @staticmethod
    def _sinking_fund_factor(i, n, k, int_sys):
        accum_factor_n = int_sys.accumulation_factor(i, n)
        reduc_factor_1 = int_sys.reduction_factor(i, 1)
        k_factor = reduc_factor_1 if k == 0 else 1
        return (i / (accum_factor_n - 1)) * k_factor


if __name__ == '__main__':
    print(UniformSeriesPayment(0.05, 6, 1).present_value(3000))
    print(UniformSeriesPayment(0.045, 12, 1).payment_by_present_value(0.7*20000))
    print(UniformSeriesPayment(0.04, 6, 1).capital_recovery_factor())
    print(UniformSeriesPayment(0.035, 4, 0).present_value(200))
    print(UniformSeriesPayment(0.04, 5, 0).payment_by_present_value(2000))
    print(UniformSeriesPayment(0.03, 6, 0).capital_recovery_factor())
    print(UniformSeriesPayment(0.01, 180, 1).future_value(500))
    print(UniformSeriesPayment(0.005, 12, 0).future_value(750))
    print(UniformSeriesPayment(0.07, 5, 0).sinking_fund_factor())
    print(UniformSeriesPayment(0.07, 5, 0).future_value(162.51))
    print(UniformSeriesPayment(0.07, 5, 1).sinking_fund_factor())
    print(UniformSeriesPayment(0.07, 5, 1).future_value(173.89))
