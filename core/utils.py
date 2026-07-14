"""Utility helpers for formatting and date calculations."""

from __future__ import annotations

from datetime import date
from datetime import timedelta
from typing import Optional


def format_inr(amount: float) -> str:
    """Format a number as Indian Rupees with lakh/crore grouping."""
    neg = amount < 0
    amount = abs(amount)
    whole = int(round(amount))
    s = str(whole)
    if len(s) > 3:
        last3 = s[-3:]
        rest = s[:-3]
        parts = []
        while len(rest) > 2:
            parts.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.insert(0, rest)
        grouped = ",".join(parts) + "," + last3
    else:
        grouped = s
    prefix = "-" if neg else ""
    return f"₹{prefix}{grouped}"


def format_number(amount: float, decimals: int = 2) -> str:
    """Format a number with thousand separators."""
    return f"{amount:,.{decimals}f}"


def format_percent(value: float, decimals: int = 1) -> str:
    """Format a fraction or percentage value as a percent string."""
    return f"{value:.{decimals}f}%"


def add_months(start: date, months: int) -> date:
    """Add a number of months to a date, clamping the day to month end."""
    y = start.year + (start.month - 1 + months) // 12
    m = (start.month - 1 + months) % 12 + 1
    # clamp day
    import calendar
    d = min(start.day, calendar.monthrange(y, m)[1])
    return date(y, m, d)


def completion_date(months: int, start: Optional[date] = None) -> date:
    """Return the loan completion date given a number of months."""
    start = start or date.today()
    return add_months(start, months)


def years_months_str(months: int) -> str:
    """Render a month count as a human-readable years + months string."""
    y = months // 12
    m = months % 12
    parts = []
    if y:
        parts.append(f"{y} yr{'s' if y != 1 else ''}")
    if m:
        parts.append(f"{m} mo{'s' if m != 1 else ''}")
    return " ".join(parts) if parts else "0 months"
