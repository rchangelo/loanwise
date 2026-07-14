"""Shared UI helpers: theme, cards, pro placeholders, and chart styling."""

from __future__ import annotations

from typing import Optional

import streamlit as st
import plotly.graph_objects as go

PRIMARY = "#FF7A00"
PRIMARY_DARK = "#E66A00"
PRIMARY_LIGHT = "#FFE9D6"
BG = "#FFFFFF"
TEXT = "#F38510"
MUTED = "#6B7280"
SUCCESS = "#16A34A"
WARNING = "#F59E0B"
ERROR = "#DC2626"
CARD_BORDER = "#F1F1F1"

# CSS injected once per app run to give LoanWise its premium look.
THEME_CSS = f"""
<style>
    /* Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    .lw-main .block-container {{
        padding-top: 2rem; max-width: 1100px;
    }}
    /* Headings */
    .lw-title {{
        font-size: 2.6rem; font-weight: 700; color: {TEXT};
        letter-spacing: -0.02em; margin: 0;
    }}
    .lw-subtitle {{
        font-size: 1.05rem; color: {MUTED}; margin-top: 0.3rem; font-weight: 400;
    }}
    .lw-section {{
        font-size: 1.25rem; font-weight: 600; color: {TEXT};
        margin: 1.5rem 0 0.75rem 0;
    }}
    /* Cards */
    .lw-card {{
        background: {BG}; border: 1px solid {CARD_BORDER};
        border-radius: 16px; padding: 1.25rem 1.4rem;
        box-shadow: 0 4px 18px rgba(0,0,0,0.05);
        height: 100%;
    }}
    .lw-card-label {{
        font-size: 0.78rem; font-weight: 500; color: {MUTED};
        text-transform: uppercase; letter-spacing: 0.04em;
    }}
    .lw-card-value {{
        font-size: 1.6rem; font-weight: 700; color: {TEXT}; margin-top: 0.25rem;
    }}
    .lw-card-accent {{
        font-size: 1.6rem; font-weight: 700; color: {PRIMARY}; margin-top: 0.25rem;
    }}
    .lw-card-sub {{
        font-size: 0.8rem; color: {MUTED}; margin-top: 0.2rem;
    }}
    /* Winner badge */
    .lw-winner {{
        background: {PRIMARY_LIGHT}; color: {PRIMARY_DARK};
        font-weight: 600; padding: 0.35rem 0.8rem; border-radius: 999px;
        display: inline-block; font-size: 0.85rem;
    }}
    /* Pro button styling */
    .lw-pro-btn {{
        opacity: 0.65; cursor: not-allowed;
    }}
    /* Divider */
    .lw-divider {{
        height: 1px; background: {CARD_BORDER}; margin: 1.5rem 0; border: none;
    }}
    /* Tagline */
    .lw-tagline {{
        font-size: 0.95rem; color: {MUTED}; font-style: italic;
    }}
</style>
"""


def inject_theme() -> None:
    """Inject the LoanWise theme CSS. Call once at app startup."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def card(label: str, value: str, sub: Optional[str] = None, accent: bool = False) -> None:
    """Render a single metric card."""
    value_cls = "lw-card-accent" if accent else "lw-card-value"
    sub_html = f'<div class="lw-card-sub">{sub}</div>' if sub else ""
    st.markdown(
        f"""
        <div class="lw-card">
            <div class="lw-card-label">{label}</div>
            <div class="{value_cls}">{value}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str) -> None:
    """Render a section sub-header."""
    st.markdown(f'<div class="lw-section">{title}</div>', unsafe_allow_html=True)


def pro_placeholder(label: str, key: Optional[str] = None) -> None:
    """Render a disabled Pro-version button that shows a dialog when clicked."""
    st.markdown(
        f"""
        <div class="lw-pro-btn">
            <button disabled style="
                width:100%; padding:0.55rem 0.75rem; border-radius:10px;
                border:1px solid {CARD_BORDER}; background:#FAFAFA;
                color:{MUTED}; font-weight:500; font-size:0.9rem;">
                ⭐ {label} (Pro)
            </button>
        </div>
        """,
        unsafe_allow_html=True,
    )


def doughnut_chart(principal: float, interest: float) -> go.Figure:
    """Build a clean doughnut chart of principal vs interest."""
    total = principal + interest
    p_pct = principal / total * 100 if total else 0
    i_pct = interest / total * 100 if total else 0

    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Principal", "Interest"],
                values=[principal, interest],
                hole=0.62,
                marker=dict(colors=[PRIMARY, "#E5E7EB"]),
                textinfo="label+percent",
                textposition="outside",
                textfont=dict(size=13, color=TEXT),
                showlegend=False,
                hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>",
            )
        ]
    )
    fig.update_traces(
        texttemplate=["Principal " + f"{p_pct:.1f}%", "Interest " + f"{i_pct:.1f}%"],
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=20, b=20),
        height=320,
        plot_bgcolor=BG,
        paper_bgcolor=BG,
        annotations=[
            dict(
                text=f"<b>Total</b><br>₹{total:,.0f}",
                x=0.5, y=0.5, font_size=13, showarrow=False, font_color=TEXT,
            )
        ],
    )
    return fig
