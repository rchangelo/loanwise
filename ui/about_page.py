"""About page for LoanWise."""

from __future__ import annotations

import streamlit as st

from .theme import section_header


def render_about_page() -> None:
    """Render the About page."""
    st.markdown(
        '<div class="lw-title" style="font-size:2rem;">About LoanWise</div>'
        '<div class="lw-subtitle">Make smarter loan decisions before they cost you lakhs.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr class='lw-divider'>", unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:1.05rem; color:#4B5563; line-height:1.7;'>"
        "LoanWise helps borrowers understand the <b>long-term impact of loan decisions</b> "
        "before they borrow. It is not a simple EMI calculator — it is a decision planner "
        "that answers questions like:"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='margin:1rem 0; color:#1F2937; line-height:1.9;'>"
        "• Which loan is cheaper?<br>"
        "• Should I choose 15 years or 20 years?<br>"
        "• What if I increase my EMI by ₹2,000?<br>"
        "• What if I make an annual prepayment?<br>"
        "• How much interest can I save?<br>"
        "• Which bank offer is better?"
        "</div>",
        unsafe_allow_html=True,
    )

    section_header("Privacy & Offline")
    st.markdown(
        "<div style='color:#4B5563; line-height:1.7;'>"
        "• <b>No personal data is stored.</b> Everything runs in your browser session.<br>"
        "• <b>Works completely offline.</b> No accounts, no servers, no tracking.<br>"
        "• Your loan details never leave your device."
        "</div>",
        unsafe_allow_html=True,
    )

    section_header("Free vs Pro")
    st.markdown(
        "<div style='color:#4B5563; line-height:1.7;'>"
        "<b>Free version includes:</b><br>"
        "• EMI Calculator & Loan Summary<br>"
        "• One Doughnut Chart<br>"
        "• Loan Comparison<br>"
        "• What If Planner<br><br>"
        "<b>Pro version (coming soon):</b><br>"
        "• Export to PDF / Excel<br>"
        "• Save unlimited scenarios<br>"
        "• Loan history & prepayment timeline<br>"
        "• AI Loan Advisor"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<hr class='lw-divider'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align:center; color:#9CA3AF; font-size:0.85rem;'>"
        "LoanWise — Built with Python & Streamlit. For educational purposes only; "
        "always consult your bank for exact figures."
        "</div>",
        unsafe_allow_html=True,
    )
