"""EMI Calculator page for LoanWise."""

from __future__ import annotations

import streamlit as st

from core.calculator import LoanCalculator
from .theme import card, section_header, doughnut_chart, pro_placeholder
from core.utils import format_inr, format_percent


def render_emi_page() -> None:
    """Render the EMI Calculator page."""
    st.markdown(
        '<div class="lw-title" style="font-size:2rem;">EMI Calculator</div>'
        '<div class="lw-subtitle">Know your monthly payment and the true cost of your loan.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr class='lw-divider'>", unsafe_allow_html=True)

    col_in1, col_in2 = st.columns(2)

    with col_in1:
        loan_amount = st.number_input(
            "Loan Amount (₹)",
            min_value=0.0,
            value=500000.0,
            step=50000.0,
            format="%.2f",
            help="The principal amount you wish to borrow.",
        )
        interest_rate = st.number_input(
            "Interest Rate (% p.a.)",
            min_value=0.0,
            value=9.6,
            step=0.05,
            format="%.2f",
            help="Annual interest rate offered by the bank.",
        )

    with col_in2:
        tenure_value = st.number_input(
            "Loan Tenure",
            min_value=1,
            value=20,
            step=1,
            help="Duration of the loan.",
        )
        tenure_unit = st.selectbox("Tenure Unit", ["Years", "Months"], index=0)
        processing_fee = st.number_input(
            "Processing Fee (₹) (optional)",
            min_value=0.0,
            value=0.0,
            step=500.0,
            format="%.2f",
        )
        insurance = st.number_input(
            "Insurance (₹) (optional)",
            min_value=0.0,
            value=0.0,
            step=500.0,
            format="%.2f",
        )

    col_btn1, col_btn2, _ = st.columns([1, 1, 4])
    calculate = col_btn1.button("Calculate", use_container_width=True, type="primary")
    reset = col_btn2.button("Reset", use_container_width=True)

    if reset:
        st.session_state.pop("emi_result", None)
        st.rerun()

    if calculate:
        months = LoanCalculator.tenure_to_months(tenure_value, tenure_unit)
        calc = LoanCalculator(loan_amount, interest_rate, months)
        result = calc.calculate()
        # add fees into total payment
        result.total_payment = round(result.total_payment + processing_fee + insurance, 2)
        st.session_state["emi_result"] = result
        st.session_state["emi_inputs"] = (loan_amount, interest_rate, tenure_value, tenure_unit, processing_fee, insurance)

    result = st.session_state.get("emi_result")
    if result is None:
        # compute a default so the page isn't empty
        months = LoanCalculator.tenure_to_months(20, "Years")
        result = LoanCalculator(500000.0, 9.6, months).calculate()
        result.total_payment = round(result.total_payment, 2)

    section_header("Your Loan Summary")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("Monthly EMI", format_inr(result.emi), accent=True)
    with c2:
        card("Total Interest", format_inr(result.total_interest))
    with c3:
        card("Total Repayment", format_inr(result.total_payment))
    with c4:
        card("Loan Duration", result.duration_str, sub=f"Completes by {result.completion.strftime('%b %Y')}")

    c5, c6, c7 = st.columns(3)
    with c5:
        card("Principal", format_inr(result.principal), sub=f"{format_percent(result.principal_pct)} of repayment")
    with c6:
        card("Interest", format_inr(result.total_interest), sub=f"{format_percent(result.interest_pct)} of repayment")
    with c7:
        card("Completion Date", result.completion.strftime("%d %b %Y"))

    section_header("Principal vs Interest")

    col_chart, col_pie = st.columns([3, 2])
    with col_chart:
        st.plotly_chart(doughnut_chart(result.principal, result.total_interest), use_container_width=True)
    with col_pie:
        st.markdown(
            f"""
            <div style='display:flex; flex-direction:column; gap:1rem; padding-top:2rem;'>
              <div style='display:flex; align-items:center; gap:0.6rem;'>
                <span style='width:14px;height:14px;border-radius:4px;background:#FF7A00;display:inline-block;'></span>
                <span style='color:#E66A00;font-weight:600;'>Principal</span>
                <span style='color:#6B7280;margin-left:auto;'>{format_percent(result.principal_pct)}</span>
              </div>
              <div style='display:flex; align-items:center; gap:0.6rem;'>
                <span style='width:14px;height:14px;border-radius:4px;background:#E5E7EB;display:inline-block;'></span>
                <span style='color:#E66A007;font-weight:600;'>Interest</span>
                <span style='color:#6B7280;margin-left:auto;'>{format_percent(result.interest_pct)}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_header("Pro Features")
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        pro_placeholder("Export PDF")
    with pc2:
        pro_placeholder("Export Excel")
    with pc3:
        pro_placeholder("Save Scenario")
