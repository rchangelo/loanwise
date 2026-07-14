"""LoanWise — Loan Decision Planner.

Entry point for the Streamlit application. Run with:

    streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Ensure the package root is importable when run as `streamlit run app.py`
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ui import (  # noqa: E402
    render_about_page,
    render_comparison_page,
    render_dashboard,
    render_emi_page,
    render_scenario_page,
)
from ui.theme import inject_theme  # noqa: E402


PAGES = {
    "Dashboard": render_dashboard,
    "EMI Calculator": render_emi_page,
    "Loan Comparison": render_comparison_page,
    "What If Planner": render_scenario_page,
    "About": render_about_page,
}


def configure_page() -> None:
    """Set page config and inject theme."""
    st.set_page_config(
        page_title="LoanWise — Loan Decision Planner",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_theme()


def render_sidebar() -> str:
    """Render the sidebar navigation and return the selected page name."""
    with st.sidebar:
        st.markdown(
            "<div style='text-align:center; padding:0.5rem 0 1rem 0;'>"
            "<div style='font-size:1.5rem; font-weight:700; color:#FF7A00;'>LoanWise</div>"
            "<div style='font-size:0.8rem; color:#6B7280; font-style:italic;'>"
            "Make smarter loan decisions<br>before they cost you lakhs."
            "</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<hr class='lw-divider'>", unsafe_allow_html=True)
        selection = st.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")
        st.markdown("<hr class='lw-divider'>", unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align:center; color:#9CA3AF; font-size:0.75rem;'>"
            "Free Version · 100% Offline · No data stored"
            "</div>",
            unsafe_allow_html=True,
        )
    return selection


def main() -> None:
    """Application entry point."""
    configure_page()
    page = render_sidebar()
    renderer = PAGES[page]
    renderer()


if __name__ == "__main__":
    main()
