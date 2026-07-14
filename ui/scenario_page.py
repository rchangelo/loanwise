"""What-If Scenario Planner page for LoanWise."""

from __future__ import annotations

import streamlit as st

from core.scenario import ScenarioInput, ScenarioPlanner
from .theme import card, section_header, pro_placeholder
from core.utils import format_inr, years_months_str


def render_scenario_page() -> None:
    """Render the What-If Scenario Planner page."""
    st.markdown(
        '<div class="lw-title" style="font-size:2rem;">What If Planner</div>'
        '<div class="lw-subtitle">See how small changes save you lakhs before you commit.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr class='lw-divider'>", unsafe_allow_html=True)

    col_base, col_whatif = st.columns(2)

    with col_base:
        st.markdown("<h4 style='color:#FF7A00;'>Your Current Loan</h4>", unsafe_allow_html=True)
        principal = st.number_input("Loan Amount (₹)", min_value=0.0, value=500000.0, step=50000.0, format="%.2f", key="s_principal")
        rate = st.number_input("Interest Rate (% p.a.)", min_value=0.0, value=9.6, step=0.05, format="%.2f", key="s_rate")
        years = st.number_input("Tenure (Years)", min_value=1, value=20, step=1, key="s_years")

    with col_whatif:
        st.markdown("<h4 style='color:#FF7A00;'>What If I…</h4>", unsafe_allow_html=True)
        extra_emi = st.number_input("Increase EMI by (₹/month)", min_value=0.0, value=2000.0, step=500.0, format="%.2f", key="s_extra")
        annual_prepay = st.number_input("Annual Prepayment (₹/year)", min_value=0.0, value=0.0, step=10000.0, format="%.2f", key="s_annual")
        one_time = st.number_input("One-Time Prepayment (₹)", min_value=0.0, value=0.0, step=50000.0, format="%.2f", key="s_onetime")
        rate_reduction = st.number_input("Interest Rate Reduction (% points)", min_value=0.0, value=0.0, step=0.1, format="%.2f", key="s_reduction")

    simulate = st.button("Simulate", use_container_width=True, type="primary")

    scenario = ScenarioInput(
        principal=principal,
        annual_rate=rate,
        tenure_months=years * 12,
        extra_emi=extra_emi,
        annual_prepayment=annual_prepay,
        one_time_prepayment=one_time,
        rate_reduction=rate_reduction,
    )

    if simulate or "scn_result" in st.session_state:
        result = ScenarioPlanner(scenario).simulate()
        st.session_state["scn_result"] = result
    else:
        # default scenario
        result = ScenarioPlanner(ScenarioInput(500000.0, 9.6, 240, extra_emi=2000.0)).simulate()

    baseline = result.baseline

    section_header("Baseline vs What If")

    c1, c2, c3 = st.columns(3)
    with c1:
        card("Baseline EMI", format_inr(baseline.emi))
    with c2:
        card("New EMI", format_inr(result.new_emi), accent=True)
    with c3:
        card("Baseline Interest", format_inr(baseline.total_interest))

    c4, c5, c6 = st.columns(3)
    with c4:
        card("Interest Saved", format_inr(result.interest_saved), accent=True, sub="with your changes")
    with c5:
        card("Years Reduced", result.years_reduced_str, sub="finish earlier")
    with c6:
        card("New Completion Date", result.new_completion.strftime("%b %Y"), sub=f"was {baseline.completion.strftime('%b %Y')}")

    # Professional summary cards
    section_header("Your Summary")
    st.markdown(
        f"""
        <div style='display:flex; flex-direction:column; gap:1rem;'>
            <div class='lw-card' style='display:flex; align-items:center; gap:1rem;'>
                <span style='font-size:1.6rem;'>💰</span>
                <div>
                    <div style='font-weight:600; font-size:1.1rem; color:#1F2937;'>
                        You save {format_inr(result.interest_saved)} in interest
                    </div>
                    <div style='color:#6B7280; font-size:0.9rem;'>
                        Over the life of the loan by making these changes.
                    </div>
                </div>
            </div>
            <div class='lw-card' style='display:flex; align-items:center; gap:1rem;'>
                <span style='font-size:1.6rem;'>⏱️</span>
                <div>
                    <div style='font-weight:600; font-size:1.1rem; color:#1F2937;'>
                        You finish {result.years_reduced_str.lower()} earlier
                    </div>
                    <div style='color:#6B7280; font-size:0.9rem;'>
                        New completion: {result.new_completion.strftime('%B %Y')} instead of {baseline.completion.strftime('%B %Y')}.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section_header("Pro Features")
    pc1, pc2 = st.columns(2)
    with pc1:
        pro_placeholder("Prepayment Timeline")
    with pc2:
        pro_placeholder("AI Loan Advisor")
