"""UI pages for LoanWise."""

from .dashboard import render_dashboard
from .emi_page import render_emi_page
from .comparison_page import render_comparison_page
from .scenario_page import render_scenario_page
from .about_page import render_about_page

__all__ = [
    "render_dashboard",
    "render_emi_page",
    "render_comparison_page",
    "render_scenario_page",
    "render_about_page",
]
