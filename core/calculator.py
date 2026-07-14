"""Core loan calculation engine for LoanWise.

Contains the reusable :class:`LoanCalculator` class, which performs all
standard amortization math (EMI, total interest, balance, completion date)
using the standard reducing-balance EMI formula.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

from .utils import completion_date, years_months_str


@dataclass
class LoanResult:
    """Container for the result of a loan calculation."""

    emi: float
    principal: float
    total_interest: float
    total_payment: float
    months: int
    completion: date
    schedule: List[dict] = field(default_factory=list)

    @property
    def interest_pct(self) -> float:
        """Interest as a percentage of total payment."""
        if self.total_payment <= 0:
            return 0.0
        return self.total_interest / self.total_payment * 100

    @property
    def principal_pct(self) -> float:
        """Principal as a percentage of total payment."""
        if self.total_payment <= 0:
            return 0.0
        return self.principal / self.total_payment * 100

    @property
    def duration_str(self) -> str:
        """Human-readable loan duration."""
        return years_months_str(self.months)


class LoanCalculator:
    """Reusable loan calculator using the standard reducing-balance EMI formula.

    EMI = P * r * (1+r)^n / ((1+r)^n - 1)

    where P = principal, r = monthly interest rate, n = number of months.
    """

    def __init__(self, principal: float, annual_rate: float, tenure_months: int) -> None:
        self.principal = float(principal)
        self.annual_rate = float(annual_rate)
        self.tenure_months = int(tenure_months)

    @property
    def monthly_rate(self) -> float:
        """Monthly interest rate as a decimal (e.g. 0.008 for 9.6% p.a.)."""
        return self.annual_rate / 100 / 12

    def calculate(self, start_date: Optional[date] = None) -> LoanResult:
        """Compute EMI, totals, completion date, and full amortization schedule."""
        p = self.principal
        r = self.monthly_rate
        n = self.tenure_months

        if n <= 0:
            return LoanResult(0.0, p, 0.0, p, 0, completion_date(0, start_date))
        if p <= 0:
            return LoanResult(0.0, 0.0, 0.0, 0.0, n, completion_date(n, start_date))

        if r == 0:
            emi = p / n
        else:
            factor = (1 + r) ** n
            emi = p * r * factor / (factor - 1)

        schedule: List[dict] = []
        balance = p
        total_interest = 0.0
        for month in range(1, n + 1):
            interest = balance * r
            principal_part = emi - interest
            # final month: settle any rounding remainder
            if month == n:
                principal_part = balance
                emi_month = balance + interest
            else:
                emi_month = emi
            balance -= principal_part
            total_interest += interest
            schedule.append(
                {
                    "month": month,
                    "emi": round(emi_month, 2),
                    "principal": round(principal_part, 2),
                    "interest": round(interest, 2),
                    "balance": round(max(balance, 0.0), 2),
                }
            )

        total_payment = p + total_interest
        comp = completion_date(n, start_date)
        return LoanResult(
            emi=round(emi, 2),
            principal=round(p, 2),
            total_interest=round(total_interest, 2),
            total_payment=round(total_payment, 2),
            months=n,
            completion=comp,
            schedule=schedule,
        )

    @staticmethod
    def tenure_to_months(value: float, unit: str) -> int:
        """Convert a tenure value with unit ('Years' or 'Months') to months."""
        if unit == "Years":
            return int(round(value * 12))
        return int(round(value))
