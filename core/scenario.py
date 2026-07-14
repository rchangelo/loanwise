"""What-If scenario planner engine for LoanWise.

Simulates the effect of changes to a baseline loan:
  - increased EMI
  - annual prepayment
  - one-time prepayment
  - interest rate reduction

Returns the new EMI, interest saved, years reduced, and new completion date.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from .calculator import LoanCalculator, LoanResult
from .utils import completion_date, years_months_str


@dataclass
class ScenarioInput:
    """User inputs for a what-if scenario."""

    principal: float
    annual_rate: float
    tenure_months: int
    extra_emi: float = 0.0
    annual_prepayment: float = 0.0
    one_time_prepayment: float = 0.0
    rate_reduction: float = 0.0  # percentage points to subtract from rate


@dataclass
class ScenarioResult:
    """Outcome of a what-if scenario simulation."""

    baseline: LoanResult
    new_emi: float
    new_months: int
    interest_saved: float
    years_reduced_months: int
    new_completion: date

    @property
    def years_reduced_str(self) -> str:
        """Human-readable years/months reduced."""
        return years_months_str(self.years_reduced_months)


class ScenarioPlanner:
    """Simulate loan changes and quantify the savings."""

    def __init__(self, scenario: ScenarioInput) -> None:
        self.scenario = scenario

    def simulate(self, start_date: Optional[date] = None) -> ScenarioResult:
        """Run the simulation and return a :class:`ScenarioResult`."""
        s = self.scenario
        baseline_calc = LoanCalculator(s.principal, s.annual_rate, s.tenure_months)
        baseline = baseline_calc.calculate(start_date=start_date)

        new_rate = max(s.annual_rate - s.rate_reduction, 0.0)
        r = new_rate / 100 / 12
        n = s.tenure_months

        # Base EMI under the (possibly reduced) rate
        if r == 0:
            base_emi = s.principal / n
        else:
            factor = (1 + r) ** n
            base_emi = s.principal * r * factor / (factor - 1)

        new_emi = base_emi + s.extra_emi

        # Simulate month by month with prepayments
        balance = s.principal
        if s.one_time_prepayment > 0:
            balance = max(balance - s.one_time_prepayment, 0.0)

        month = 0
        annual_counter = 0
        while balance > 0.01 and month < n * 2 + 12:
            month += 1
            interest = balance * r
            principal_part = new_emi - interest
            if principal_part <= 0:
                # EMI doesn't cover interest; bail out
                break
            if principal_part >= balance:
                principal_part = balance
            balance -= principal_part

            # annual prepayment every 12 months
            annual_counter += 1
            if annual_counter == 12 and s.annual_prepayment > 0:
                balance = max(balance - s.annual_prepayment, 0.0)
                annual_counter = 0

        new_months = month
        # total paid under scenario
        total_paid = new_emi * new_months + s.one_time_prepayment
        # add annual prepayments made
        annual_payments_made = new_months // 12
        total_paid += annual_payments_made * s.annual_prepayment
        # cap at principal
        if total_paid > s.principal + (new_emi * new_months):
            total_paid = s.principal + (new_emi * new_months)
        new_interest = max(total_paid - s.principal, 0.0)

        interest_saved = max(baseline.total_interest - new_interest, 0.0)
        years_reduced = max(baseline.months - new_months, 0)

        return ScenarioResult(
            baseline=baseline,
            new_emi=round(new_emi, 2),
            new_months=new_months,
            interest_saved=round(interest_saved, 2),
            years_reduced_months=years_reduced,
            new_completion=completion_date(new_months, start_date),
        )
