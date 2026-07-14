"""Loan comparison engine for LoanWise.

Compares two loans side by side and determines which is cheaper.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .calculator import LoanCalculator, LoanResult


@dataclass
class LoanSpec:
    """Specification of a single loan offer."""

    principal: float
    annual_rate: float
    tenure_months: int


@dataclass
class ComparisonResult:
    """Outcome of comparing two loans."""

    loan_a: LoanResult
    loan_b: LoanResult
    interest_difference: float
    money_saved: float
    winner: str  # "Loan A", "Loan B", or "Equal"

    @property
    def winner_label(self) -> str:
        """Human-readable winner label."""
        if self.winner == "Equal":
            return "Both loans are equal"
        return f"{self.winner} is cheaper"


class LoanComparison:
    """Compare two loan offers and identify the cheaper one."""

    def __init__(self, spec_a: LoanSpec, spec_b: LoanSpec) -> None:
        self.spec_a = spec_a
        self.spec_b = spec_b

    def compare(self) -> ComparisonResult:
        """Run the comparison and return a :class:`ComparisonResult`."""
        calc_a = LoanCalculator(
            self.spec_a.principal, self.spec_a.annual_rate, self.spec_a.tenure_months
        )
        calc_b = LoanCalculator(
            self.spec_b.principal, self.spec_b.annual_rate, self.spec_b.tenure_months
        )
        res_a = calc_a.calculate()
        res_b = calc_b.calculate()

        interest_diff = res_a.total_interest - res_b.total_interest
        # money saved by choosing the cheaper loan
        if res_a.total_payment < res_b.total_payment:
            money_saved = res_b.total_payment - res_a.total_payment
            winner = "Loan A"
        elif res_b.total_payment < res_a.total_payment:
            money_saved = res_a.total_payment - res_b.total_payment
            winner = "Loan B"
        else:
            money_saved = 0.0
            winner = "Equal"

        return ComparisonResult(
            loan_a=res_a,
            loan_b=res_b,
            interest_difference=round(interest_diff, 2),
            money_saved=round(money_saved, 2),
            winner=winner,
        )
