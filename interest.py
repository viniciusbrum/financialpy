#! python3
# interest.py - Simple and compound interest.

from abc import ABCMeta
from abc import abstractmethod
from itertools import zip_longest
import math


class AbstractInterest(metaclass=ABCMeta):
    """Abstract class for interest."""

    @staticmethod
    @abstractmethod
    def accumulation_factor(interest_rate, periods):
        """Calculates the accumulation factor."""
        pass

    @classmethod
    def future_value(cls, present_value, interest=None, interest_rate=None,
                     periods=None):
        """Calculates the future value from the present value, interest
        or interest rate and number of periods."""
        if interest is not None:
            return present_value + interest

        return present_value * cls.accumulation_factor(interest_rate, periods)

    @classmethod
    def interest(cls, present_value, future_value=None, interest_rate=None,
                 periods=None):
        """Calculates the interest from the present value, future value
        or interest rate and number of periods."""
        if future_value is not None:
            return future_value - present_value

        return present_value*(cls.accumulation_factor(interest_rate, periods) - 1)

    @classmethod
    @abstractmethod
    def interest_rate(cls, present_value, future_value, periods):
        """Calculates the interest rate."""
        pass

    @classmethod
    def interest_rate_period(cls, present_value, future_value=None,
                             interest=None):
        """Calculates the interest rate for the period from the present
        value and future value or interest."""
        if future_value is not None:
            interest = cls.interest(present_value, future_value=future_value)

        return interest / present_value

    @classmethod
    def internal_rate_return(cls, present_value, future_value, periods):
        """Calculates the internal rate of return."""
        return cls.interest_rate(present_value, future_value, periods)

    @classmethod
    def net_present_value(cls, future_values, interest_rates, periods):
        """Calculates the net present value from a cash flow."""
        npv = 0.0
        prev_f = future_values[0]
        prev_i = interest_rates[0]
        prev_n = periods[0]

        for f, i, n in zip_longest(future_values, interest_rates, periods):
            f = f if f is not None else prev_f
            i = i if i is not None else prev_i
            n = n if n is not None else prev_n
            npv += cls.present_value(f, interest_rate=i, periods=n)
            prev_f = f
            prev_i = i
            prev_n = n

        return npv

    @classmethod
    def present_value(cls, future_value, interest=None, interest_rate=None,
                      periods=None):
        """Calculates the present value from the future value and
        interest or interest rate and number of periods."""
        if interest is not None:
            return future_value - interest

        return future_value * cls.reduction_factor(interest_rate, periods)

    @classmethod
    def real_interest_rate_period(cls, present_value, inflation_rate,
                                  interest_rate=None, future_value=None,
                                  interest=None):
        """Calculates the real interest rate for the period from the
        present value, inflation rate, and interest rate, future value
        or interest."""
        if interest_rate is None:
            if future_value is not None:
                interest_rate = cls.interest_rate_period(
                    present_value, future_value=future_value)
            else:
                interest_rate = cls.interest_rate_period(present_value,
                                                         interest=interest)

        return (interest_rate - inflation_rate)/(1 + inflation_rate)

    @classmethod
    def real_interest_period(cls, present_value, inflation_rate,
                             interest_rate=None, future_value=None,
                             interest=None):
        """Calculates the real interest for the period from the present
        value, inflation rate, and interest rate, future value or
        interest."""
        if interest_rate is None:
            if future_value is not None:
                interest_rate = cls.interest_rate_period(
                    present_value, future_value=future_value)
            else:
                interest_rate = cls.interest_rate_period(present_value,
                                                         interest=interest)

        return present_value*(interest_rate - inflation_rate)

    @classmethod
    def real_or_effective_interest_rate(cls, real_interest_rate,
                                        effective_interest_rate,
                                        expected_inflation_rate):
        """Checks the best rate: a real interest rate or a effective
        interest rate according to expected inflation."""
        relation = (1 + effective_interest_rate)/(1 + real_interest_rate) - 1

        if expected_inflation_rate > relation:
            return real_interest_rate

        return effective_interest_rate

    @classmethod
    def reduction_factor(cls, interest_rate, periods):
        """Calculates the reduction factor."""
        return 1 / cls.accumulation_factor(interest_rate, periods)


class SimpleInterest(AbstractInterest):
    """Class for simple interest."""

    @staticmethod
    def accumulation_factor(interest_rate, periods):
        """Calculates the accumulation factor."""
        return 1 + (interest_rate*periods)

    @classmethod
    def equivalent_future_value(cls, future_values, interest_rate, from_periods,
                                to_periods):
        """Calculates a equivalent future value."""
        npv = cls.net_present_value(future_values, interest_rate, from_periods)
        i = interest_rate[0]
        sum_reduction_factor = 0.0

        for n in to_periods:
            sum_reduction_factor += cls.reduction_factor(i, n)

        return npv / sum_reduction_factor

    @staticmethod
    def equivalent_interest_rate(interest_rate, from_periods, to_periods):
        """Calculates a equivalent interest rate."""
        return interest_rate * (to_periods/from_periods)

    @classmethod
    def interest_rate(cls, present_value, future_value, periods):
        """Calculates the interest rate."""
        interest_rate_period = cls.interest_rate_period(
            present_value, future_value=future_value)
        return interest_rate_period / periods

    @staticmethod
    def is_proportional(interest_rate_n, n_periods, interest_rate_m, m_periods,
                        tolerance=1e-4):
        """Checks whether two interest rates are proportional."""
        interests_q = interest_rate_n / interest_rate_m
        periods_q = n_periods / m_periods
        return abs(interests_q - periods_q) < tolerance

    @classmethod
    def periods(cls, present_value, future_value, interest_rate):
        """Calculates the number of periods."""
        interest_rate_period = cls.interest_rate_period(
            present_value, future_value=future_value)
        return interest_rate_period / interest_rate


class CompoundInterest(AbstractInterest):
    """Class for compound interest."""

    @staticmethod
    def accumulation_factor(interest_rate, periods):
        """Calculates the accumulation factor."""
        return (1 + interest_rate) ** periods

    @classmethod
    def interest_rate(cls, present_value, future_value, periods):
        """Calculates the interest rate."""
        interest_rate_period = cls.interest_rate_period(
            present_value, future_value=future_value)
        return (1 + interest_rate_period)**(1 / periods) - 1

    @classmethod
    def is_equivalent(cls, interest_rate_n, n_periods, interest_rate_m,
                      m_periods, tolerance=1e-4):
        """Checks whether two interest rates are equivalent."""
        acc_factor_n = cls.accumulation_factor(interest_rate_n, n_periods)
        acc_factor_m = cls.accumulation_factor(interest_rate_m, m_periods)
        return abs(acc_factor_n - acc_factor_m) < tolerance

    @classmethod
    def periods(cls, present_value, future_value, interest_rate):
        """Calculates the number of periods."""
        interest_rate_period = cls.interest_rate_period(
            present_value, future_value=future_value)
        return math.log((1 + interest_rate_period), (1 + interest_rate))
