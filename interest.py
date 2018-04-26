#! python3
# interest.py - Simple and compound interest.

from abc import ABCMeta
from abc import abstractmethod


class AbstractInterest(metaclass=ABCMeta):
    """Abstract class for interest."""

    @staticmethod
    @abstractmethod
    def accumulation_factor(interest_rate, periods):
        """Calculates the accumulation factor."""
        pass

    @classmethod
    def reduction_factor(cls, interest_rate, periods):
        """Calculates the reduction factor."""
        return 1 / cls.accumulation_factor(interest_rate, periods)

    @staticmethod
    def future_value(present_value, interest):
        """Calculates the future value from the present value and
        interest."""
        return present_value + interest

    @staticmethod
    def present_value(future_value, interest):
        """Calculates the present value from the future value and
        interest."""
        return future_value - interest

    @staticmethod
    def interest(present_value, future_value):
        """Calculates the interest from the present value and future
        values."""
        return future_value - present_value

    @staticmethod
    def interest_rate_period(present_value, future_value=None, interest=None):
        """Calculates the interest rate for the period from the present
        value and future value or interest."""
        if future_value is not None:
            return future_value/present_value - 1

        return interest / present_value


class SimpleInterest(AbstractInterest):
    """Class for simple interest."""

    @staticmethod
    def accumulation_factor(interest_rate, periods):
        """Calculates the accumulation factor."""
        return 1 + (interest_rate*periods)

    @staticmethod
    def internal_rate_return(present_value, future_value, periods):
        """Calculates the internal rate of return."""
        return (future_value/present_value - 1) / periods

    @staticmethod
    def is_proportional(interest_rate_n, n_periods, interest_rate_m, m_periods,
                        tolerance=1e-4):
        """Checks whether two interest rates are proportional."""
        interests_q = interest_rate_n / interest_rate_m
        periods_q = n_periods / m_periods
        return abs(interests_q - periods_q) < tolerance


class CompoundInterest(AbstractInterest):
    """Class for compound interest."""

    @staticmethod
    def accumulation_factor(interest_rate, periods):
        """Calculates the accumulation factor."""
        return (1 + interest_rate) ** periods

    @staticmethod
    def internal_rate_return(present_value, future_value, periods):
        """Calculates the internal rate of return."""
        return (future_value/present_value)**(1/periods) - 1

    @classmethod
    def is_equivalent(cls, interest_rate_n, n_periods, interest_rate_m,
                      m_periods, tolerance=1e-4):
        """Checks whether two interest rates are equivalent."""
        acc_factor_n = cls.accumulation_factor(interest_rate_n, n_periods)
        acc_factor_m = cls.accumulation_factor(interest_rate_m, m_periods)
        return abs(acc_factor_n - acc_factor_m) < tolerance
