"""Dashboard / welcome page for LoanWise."""

from __future__ import annotations

import streamlit as st

from .theme import card, section_header


def render_dashboard() -> None:
    """Render the LoanWise welcome dashboard."""
    st.markdown(
        '<div class="lw-title">LoanWise</div>'
        '<div class="lw-subtitle">Make smarter loan decisions before they cost you lakhs.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr class='lw-divider'>", unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:1.05rem; color:#4B5563; line-height:1.6;'>"
        "LoanWise is a <b>Loan Decision Planner</b> — not just a calculator. "
        "It helps you understand the long-term impact of your borrowing decisions "
        "before you commit. Compare offers, simulate prepayments, and see exactly "
        "how much interest you can save."
        "</div>",
        unsafe_allow_html=True,
    )

    section_header("What LoanWise can do for you")

    col1, col2, col3 = st.columns(3)
    with col1:
        card("EMI", "Calculate", "Know your exact monthly payment and total cost.")
    with col2:
        card("Total Interest", "Compare", "See which bank offer is truly cheaper.")
    with col3:
        card("Total Repayment", "Plan", "Simulate prepayments and rate changes.")

    col4, col5, col6 = st.columns(3)
    with col4:
        card("Loan Duration", "Visualize", "A clear doughnut of principal vs interest.")
    with col5:
        card("What If Planner", "Simulate", "See how ₹2,000 more EMI saves lakhs.")
    with col6:
        card("100% Private", "Offline", "No data leaves your device. Ever.")

    section_header("Quick start")
    st.markdown(
        "<div style='color:#4B5563; line-height:1.7;'>"
        "1. Open the <b>EMI Calculator</b> to compute your monthly payment.<br>"
        "2. Use <b>Loan Comparison</b> to compare two offers side by side.<br>"
        "3. Try the <b>What If Planner</b> to see how prepayments and rate changes affect your loan."
        "</div>",
        unsafe_allow_html=True,
    )
