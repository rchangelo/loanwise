"""Loan Comparison page for LoanWise."""

from __future__ import annotations

import streamlit as st

from core.comparison import LoanComparison, LoanSpec
from .theme import card, section_header, pro_placeholder
from core.utils import format_inr


def render_comparison_page() -> None:
    """Render the side-by-side loan comparison page."""
    st.markdown(
        '<div class="lw-title" style="font-size:2rem;">Loan Comparison</div>'
        '<div class="lw-subtitle">Compare two loan offers and find the cheaper one.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr class='lw-divider'>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<h4 style='color:#FF7A00;'>Loan A</h4>", unsafe_allow_html=True)
        a_amount = st.number_input("Amount (₹) — A", min_value=0.0, value=500000.0, step=50000.0, format="%.2f", key="a_amount")
        a_rate = st.number_input("Interest Rate (% p.a.) — A", min_value=0.0, value=9.6, step=0.05, format="%.2f", key="a_rate")
        a_years = st.number_input("Tenure (Years) — A", min_value=1, value=20, step=1, key="a_years")

    with col_b:
        st.markdown("<h4 style='color:#FF7A00;'>Loan B</h4>", unsafe_allow_html=True)
        b_amount = st.number_input("Amount (₹) — B", min_value=0.0, value=500000.0, step=50000.0, format="%.2f", key="b_amount")
        b_rate = st.number_input("Interest Rate (% p.a.) — B", min_value=0.0, value=8.9, step=0.05, format="%.2f", key="b_rate")
        b_years = st.number_input("Tenure (Years) — B", min_value=1, value=20, step=1, key="b_years")

    compare = st.button("Compare Loans", use_container_width=True, type="primary")

    if compare or "cmp_result" in st.session_state:
        spec_a = LoanSpec(a_amount, a_rate, a_years * 12)
        spec_b = LoanSpec(b_amount, b_rate, b_years * 12)
        result = LoanComparison(spec_a, spec_b).compare()
        st.session_state["cmp_result"] = result
    else:
        # default comparison so page isn't empty
        result = LoanComparison(
            LoanSpec(500000.0, 9.6, 240), LoanSpec(500000.0, 8.9, 240)
        ).compare()

    res_a = result.loan_a
    res_b = result.loan_b

    section_header("Comparison Summary")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("EMI — Loan A", format_inr(res_a.emi), accent=True)
    with c2:
        card("EMI — Loan B", format_inr(res_b.emi), accent=True)
    with c3:
        card("Interest Difference", format_inr(abs(result.interest_difference)), sub="A vs B")
    with c4:
        card("Money Saved", format_inr(result.money_saved), sub="by choosing cheaper loan")

    # Winner banner
    winner_color = "#16A34A" if result.winner != "Equal" else "#6B7280"
    st.markdown(
        f"""
        <div style='text-align:center; margin:1.2rem 0;'>
            <span style='background:#FFE9D6; color:#E66A00; font-weight:600;
                  padding:0.5rem 1.4rem; border-radius:999px; font-size:1rem;'>
                🏆 {result.winner_label}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Detailed table
    section_header("Detailed Breakdown")
    table_data = {
        "Metric": [
            "Loan Amount", "Interest Rate", "Tenure", "Monthly EMI",
            "Total Interest", "Total Repayment", "Completion Date",
        ],
        "Loan A": [
            format_inr(res_a.principal),
            f"{res_a.principal and (res_a.total_interest / res_a.principal * 100 / (res_a.months / 12)):.2f}% p.a.",
            res_a.duration_str,
            format_inr(res_a.emi),
            format_inr(res_a.total_interest),
            format_inr(res_a.total_payment),
            res_a.completion.strftime("%b %Y"),
        ],
        "Loan B": [
            format_inr(res_b.principal),
            f"{res_b.principal and (res_b.total_interest / res_b.principal * 100 / (res_b.months / 12)):.2f}% p.a.",
            res_b.duration_str,
            format_inr(res_b.emi),
            format_inr(res_b.total_interest),
            format_inr(res_b.total_payment),
            res_b.completion.strftime("%b %Y"),
        ],
    }
    st.table(table_data)

    section_header("Pro Features")
    pc1, pc2 = st.columns(2)
    with pc1:
        pro_placeholder("Unlimited Comparisons")
    with pc2:
        pro_placeholder("Loan History")
