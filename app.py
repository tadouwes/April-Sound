import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="144 April Point Investment Analysis",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Make sidebar 50% wider (default is ~21rem, now ~31.5rem) */
    [data-testid="stSidebar"] {
        min-width: 450px;
        max-width: 450px;
    }

    /* Fix metric cards for dark mode compatibility */
    [data-testid="stMetric"] {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #4a4a5a;
    }
    [data-testid="stMetric"] label {
        color: #fafafa !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #fafafa !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #21c354 !important;
    }

    /* Hide +/- buttons on number inputs */
    [data-testid="stNumberInput"] button {
        display: none !important;
    }
    [data-testid="stNumberInput"] [data-testid="stNumberInputContainer"] {
        width: 100% !important;
    }
    [data-testid="stNumberInput"] input {
        width: 100% !important;
    }

    /* Make tabs larger and more clickable */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: 600;
        border-radius: 10px 10px 0 0;
        background-color: #262730;
        border: 2px solid #4a4a5a;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #3a3a4a;
        cursor: pointer;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4 !important;
        border-color: #1f77b4 !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🏡 Strategic Investment Analysis")
st.subheader("144 April Point Dr S, Montgomery, TX")
st.markdown("**1,824 sq. ft. Waterside Townhouse | April Sound Community**")
st.markdown("---")

# --- SIDEBAR: INTERACTIVE VARIABLES ---
st.sidebar.header("📊 Market Assumptions")
st.sidebar.markdown("*Adjust these to model different scenarios*")

market_return = st.sidebar.slider(
    "Market Portfolio Return (%)",
    min_value=0.0, max_value=15.0, value=6.0, step=0.5,
    help="Expected annual return if cash is invested in the stock market"
) / 100

appreciation = st.sidebar.slider(
    "Property Appreciation (%)",
    min_value=0.0, max_value=15.0, value=3.0, step=0.5,
    help="Expected annual increase in property value. Montgomery County 2025 data: Home assessments up 9% YoY, Lake Conroe median prices up 4.4% YoY. Homes under 500k saw 1.9% growth. Default of 3% is conservative for this price range."
) / 100

rent_growth = st.sidebar.slider(
    "Annual Rent Growth (%)",
    min_value=0.0, max_value=10.0, value=2.5, step=0.25,
    help="Expected annual increase in rental rates. Conroe historical average: 4-6% annual growth typical. 2024-2025 saw -1% to -3% due to new apartment supply. Default of 2.5% is conservative given recent softness."
) / 100

vacancy_rate = st.sidebar.slider(
    "Vacancy Rate (%)",
    min_value=0.0, max_value=100.0, value=5.0, step=1.0,
    help="Percentage of the year the property is expected to be vacant (no rental income). A 5% vacancy means ~18 days/year without a tenant."
) / 100

st.sidebar.markdown("---")

# --- PROPERTY VALUE RANGES ---
st.sidebar.header("🏠 Property Values (As-Is)")
val_as_is_col = st.sidebar.columns(3)
with val_as_is_col[0]:
    val_as_is_low = st.number_input("$ Low", min_value=100000, max_value=500000, value=340000, step=5000, key="val_as_is_low")
with val_as_is_col[1]:
    val_as_is = st.number_input("$ Base", min_value=100000, max_value=500000, value=365000, step=5000, key="val_as_is")
with val_as_is_col[2]:
    val_as_is_high = st.number_input("$ High", min_value=100000, max_value=500000, value=390000, step=5000, key="val_as_is_high")

st.sidebar.header("🏗️ Property Values (Refurbished)", help="Based on two identical open water view comps: 143 April Point Dr S sold Jan 2025 for $485k ($266/sq ft), and 137 April Point Dr S sold Oct 2023 for $510k ($280/sq ft). Both are 1,824 sq ft, 3/2.5, renovated with open water views.")
val_refurb_col = st.sidebar.columns(3)
with val_refurb_col[0]:
    val_refurb_low = st.number_input("$ Low", min_value=200000, max_value=700000, value=485000, step=5000, key="val_refurb_low")
with val_refurb_col[1]:
    val_refurb = st.number_input("$ Base", min_value=200000, max_value=700000, value=495000, step=5000, key="val_refurb")
with val_refurb_col[2]:
    val_refurb_high = st.number_input("$ High", min_value=200000, max_value=700000, value=510000, step=5000, key="val_refurb_high")

st.sidebar.markdown("---")

# --- RENT RANGES ---
st.sidebar.header("💵 Monthly Rent (As-Is)")
rent_as_is_col = st.sidebar.columns(3)
with rent_as_is_col[0]:
    rent_as_is_low = st.number_input("$ Low", min_value=1000, max_value=5000, value=2350, step=50, key="rent_as_is_low")
with rent_as_is_col[1]:
    rent_as_is = st.number_input("$ Base", min_value=1000, max_value=5000, value=2550, step=50, key="rent_as_is")
with rent_as_is_col[2]:
    rent_as_is_high = st.number_input("$ High", min_value=1000, max_value=5000, value=2750, step=50, key="rent_as_is_high")

st.sidebar.header("💵 Monthly Rent (Refurbished)", help="Based on 140 April Point Dr S ($1.73/sq ft, renovated, water view). No direct open water view rental comps exist - owners tend to sell rather than rent these premium units. Estimate assumes modest 5% view premium. Conservative given lack of direct comps.")
rent_refurb_col = st.sidebar.columns(3)
with rent_refurb_col[0]:
    rent_refurb_low = st.number_input("$ Low", min_value=1500, max_value=6000, value=3200, step=50, key="rent_refurb_low")
with rent_refurb_col[1]:
    rent_refurb = st.number_input("$ Base", min_value=1500, max_value=6000, value=3350, step=50, key="rent_refurb")
with rent_refurb_col[2]:
    rent_refurb_high = st.number_input("$ High", min_value=1500, max_value=6000, value=3500, step=50, key="rent_refurb_high")

st.sidebar.markdown("---")

# --- REFURBISHMENT COST RANGE ---
st.sidebar.header("🔧 Refurbishment Budget")
refurb_col = st.sidebar.columns(3)
with refurb_col[0]:
    refurb_cost_low = st.number_input("$ Low", min_value=0, max_value=150000, value=50000, step=5000, key="refurb_low")
with refurb_col[1]:
    refurb_cost = st.number_input("$ Base", min_value=0, max_value=150000, value=60000, step=5000, key="refurb_base")
with refurb_col[2]:
    refurb_cost_high = st.number_input("$ High", min_value=0, max_value=150000, value=75000, step=5000, key="refurb_high")

st.sidebar.markdown("---")
st.sidebar.header("💰 Expense Assumptions")

property_tax_rate = st.sidebar.slider(
    "Property Tax Rate (%)",
    min_value=0.5, max_value=3.0, value=1.2, step=0.1,
    help="Annual property tax as % of property value"
) / 100

maintenance_rate = st.sidebar.slider(
    "Maintenance Reserve (%)",
    min_value=0.0, max_value=3.0, value=1.0, step=0.25,
    help="Annual maintenance/repairs as % of property value"
) / 100

hoa_annual = st.sidebar.number_input(
    "$ HOA + Social Fees (/year)",
    min_value=0, max_value=10000, value=2000, step=100,
    help="Annual POA and social club fees"
)

st.sidebar.markdown("---")
st.sidebar.header("👤 Management Options")

self_managed = st.sidebar.checkbox(
    "Self-Manage Property",
    value=True,
    help="If unchecked, 10% of gross rent goes to property manager"
)

management_fee = 0.0 if self_managed else 0.10

st.sidebar.markdown("---")
st.sidebar.header("🏛️ Tax Assumptions")

income_tax_rate = st.sidebar.slider(
    "Marginal Income Tax Rate (%)",
    min_value=10, max_value=37, value=22, step=1,
    help="Federal marginal tax rate on rental income (22% is common)"
) / 100

cap_gains_tax = st.sidebar.slider(
    "Capital Gains Tax Rate (%)",
    min_value=0, max_value=25, value=15, step=1,
    help="Federal long-term capital gains rate (0%, 15%, or 20% typical). NOTE: This rate is for reference only. The model assumes no capital gains tax on the property sale because: (1) Primary Residence Exemption - if you lived in the home 2 of the last 5 years, you can exclude up to 250k (single) or 500k (married) of gains; (2) For investment properties, the cost basis and any claimed depreciation would need to be tracked for accurate calculation."
) / 100

include_niit = st.sidebar.checkbox(
    "Include NIIT (3.8%)",
    value=False,
    help="Net Investment Income Tax: An additional 3.8% tax on investment income (capital gains, dividends, rental income) for high earners. Applies if your Modified Adjusted Gross Income exceeds $200k (single) or $250k (married filing jointly). This gets added on top of your capital gains tax rate."
)

if include_niit:
    cap_gains_tax += 0.038

depreciation_recapture_rate = 0.25  # Fixed by IRS

# --- FIXED PROPERTY SPECS ---
building_value = 289437  # From Tax Records (excludes land)
annual_depreciation = building_value / 27.5
selling_costs = 0.06  # 6% closing costs

# Combined expense rate
expense_rate = property_tax_rate + maintenance_rate

# --- CALCULATION ENGINE ---
def run_scenario(val_asis, val_ref, rent_asis, rent_ref, refurb, years=25):
    """Run all 4 investment scenarios with given parameters."""
    data = []

    # Starting positions for sell scenarios (no tax on sale since invested in market)
    s3_gross = val_asis * (1 - selling_costs)
    s4_gross = (val_ref * (1 - selling_costs)) - refurb

    # Track cumulative cash for rental scenarios
    cash_s1, cash_s2 = 0, 0

    for y in range(years + 1):
        # 1. Property Values (appreciate over time)
        v_as_is = val_asis * (1 + appreciation) ** y
        v_refurb = val_ref * (1 + appreciation) ** y

        # 2. SELL & INVEST Scenarios (no tax on market gains per user request)
        s3_portfolio = s3_gross * (1 + market_return) ** y
        s4_portfolio = s4_gross * (1 + market_return) ** y

        wealth_s3 = s3_portfolio
        wealth_s4 = s4_portfolio

        # 3. RENT & REINVEST Scenarios (with income tax and depreciation shield)
        if y > 0:
            # Calculate gross rent (before vacancy)
            gross_rent_s1 = (rent_asis * 12) * (1 + rent_growth) ** (y - 1)
            gross_rent_s2 = (rent_ref * 12) * (1 + rent_growth) ** (y - 1)

            # Apply vacancy rate (lose this % of rent due to empty periods)
            annual_rent_s1 = gross_rent_s1 * (1 - vacancy_rate)
            annual_rent_s2 = gross_rent_s2 * (1 - vacancy_rate)

            # Deduct management fee
            net_rent_s1 = annual_rent_s1 * (1 - management_fee)
            net_rent_s2 = annual_rent_s2 * (1 - management_fee)

            # Operating expenses (tax deductible)
            expenses_s1 = (v_as_is * expense_rate) + hoa_annual
            expenses_s2 = (v_refurb * expense_rate) + hoa_annual

            # Net Operating Income (before taxes)
            noi_s1 = net_rent_s1 - expenses_s1
            noi_s2 = net_rent_s2 - expenses_s2

            # Taxable income = NOI - Depreciation (depreciation shield)
            taxable_income_s1 = max(0, noi_s1 - annual_depreciation)
            taxable_income_s2 = max(0, noi_s2 - annual_depreciation)

            # Income tax on rental profit
            tax_s1 = taxable_income_s1 * income_tax_rate
            tax_s2 = taxable_income_s2 * income_tax_rate

            # After-tax cash flow
            after_tax_cf_s1 = noi_s1 - tax_s1
            after_tax_cf_s2 = noi_s2 - tax_s2

            # Reinvest after-tax cash flow at market rate (no tax on market gains)
            cash_s1 = (cash_s1 * (1 + market_return)) + after_tax_cf_s1
            cash_s2 = (cash_s2 * (1 + market_return)) + after_tax_cf_s2

        # Total wealth = Property Value + Reinvested Cash
        wealth_s1 = v_as_is + cash_s1
        wealth_s2 = v_refurb + cash_s2 - (refurb if y == 0 else 0)

        if y == 0:
            wealth_s2 = val_ref - refurb

        data.append({
            "Year": y,
            "Rent As-Is": wealth_s1,
            "Refurb & Rent": wealth_s2,
            "Sell As-Is": wealth_s3,
            "Refurb & Sell": wealth_s4,
            "Property Value (As-Is)": v_as_is,
            "Property Value (Refurb)": v_refurb,
            "Cash (As-Is)": cash_s1,
            "Cash (Refurb)": cash_s2 - (refurb if y == 0 else 0),
            "Portfolio (Sell As-Is)": s3_portfolio,
            "Portfolio (Refurb & Sell)": s4_portfolio,
        })

    return pd.DataFrame(data)

# Run calculations for base, low, and high scenarios
df_base = run_scenario(val_as_is, val_refurb, rent_as_is, rent_refurb, refurb_cost)

# Low scenario: pessimistic (lower values/rents, higher refurb cost)
df_low = run_scenario(val_as_is_low, val_refurb_low, rent_as_is_low, rent_refurb_low, refurb_cost_high)

# High scenario: optimistic (higher values/rents, lower refurb cost)
df_high = run_scenario(val_as_is_high, val_refurb_high, rent_as_is_high, rent_refurb_high, refurb_cost_low)

# --- MAIN DASHBOARD UI ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Summary", "📈 Rate Assumptions", "🏘️ Comparables", "🏛️ Tax Considerations", "🏠 Property Specs"])

# ============ TAB 1: SUMMARY ============
with tab1:
    st.header("25-Year Wealth Projection")
    st.markdown("*Shaded bands show the range between low and high estimates*")

    # Main Chart with uncertainty bands
    fig = go.Figure()

    colors = {
        "Rent As-Is": "#1f77b4",      # Blue
        "Refurb & Rent": "#2ca02c",   # Green
        "Sell As-Is": "#ff7f0e",      # Orange
        "Refurb & Sell": "#e377c2"    # Pink
    }

    # Add uncertainty bands (fill between low and high)
    for col in ["Rent As-Is", "Refurb & Rent", "Sell As-Is", "Refurb & Sell"]:
        # Upper bound (high scenario)
        fig.add_trace(go.Scatter(
            x=df_high['Year'],
            y=df_high[col],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))

        # Lower bound with fill to upper (creates the band)
        hex_color = colors[col]
        rgba_fill = f"rgba({int(hex_color[1:3], 16)}, {int(hex_color[3:5], 16)}, {int(hex_color[5:7], 16)}, 0.2)"
        fig.add_trace(go.Scatter(
            x=df_low['Year'],
            y=df_low[col],
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor=rgba_fill,
            showlegend=False,
            hoverinfo='skip'
        ))

    # Add main lines (base scenario)
    for col in ["Rent As-Is", "Refurb & Rent", "Sell As-Is", "Refurb & Sell"]:
        fig.add_trace(go.Scatter(
            x=df_base['Year'],
            y=df_base[col],
            name=col,
            mode='lines+markers',
            line=dict(width=3, color=colors[col]),
            marker=dict(size=6),
            hovertemplate=f"<b>{col}</b><br>Year: %{{x}}<br>Wealth: $%{{y:,.0f}}<extra></extra>"
        ))

    fig.update_layout(
        title="Net Wealth Over 25 Years (with Uncertainty Bands)",
        xaxis_title="Year",
        yaxis_title="Total Portfolio Value ($)",
        yaxis_tickformat="$,.0f",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- STACKED BAR CHART: Property Value vs Cash ---
    st.markdown("#### Wealth Composition: Property Value vs Cash/Portfolio")

    fig_breakdown = go.Figure()

    # Calculate totals for hover
    df_base['Total (As-Is)'] = df_base['Property Value (As-Is)'] + df_base['Cash (As-Is)']
    df_base['Total (Refurb)'] = df_base['Property Value (Refurb)'] + df_base['Cash (Refurb)']

    # Rent As-Is - Property Value (bottom of blue stack)
    fig_breakdown.add_trace(
        go.Bar(
            name="As-Is: Property",
            x=df_base['Year'],
            y=df_base['Property Value (As-Is)'],
            marker_color="#1f77b4",
            customdata=df_base[['Cash (As-Is)', 'Total (As-Is)']].values,
            hovertemplate="<b>Rent As-Is (Year %{x})</b><br>" +
                          "Property: $%{y:,.0f}<br>" +
                          "Cash: $%{customdata[0]:,.0f}<br>" +
                          "Total: $%{customdata[1]:,.0f}<extra></extra>",
            offsetgroup=0
        )
    )
    # Rent As-Is - Cash (top of blue stack)
    fig_breakdown.add_trace(
        go.Bar(
            name="As-Is: Cash",
            x=df_base['Year'],
            y=df_base['Cash (As-Is)'],
            marker_color="#aec7e8",
            customdata=df_base[['Property Value (As-Is)', 'Cash (As-Is)', 'Total (As-Is)']].values,
            hovertemplate="<b>Rent As-Is (Year %{x})</b><br>" +
                          "Property: $%{customdata[0]:,.0f}<br>" +
                          "Cash: $%{customdata[1]:,.0f}<br>" +
                          "Total: $%{customdata[2]:,.0f}<extra></extra>",
            offsetgroup=0,
            base=df_base['Property Value (As-Is)']
        )
    )

    # Refurb & Rent - Split cash into positive (green) and negative (red)
    df_base['Cash (Refurb) Positive'] = df_base['Cash (Refurb)'].clip(lower=0)
    df_base['Cash (Refurb) Negative'] = df_base['Cash (Refurb)'].clip(upper=0)

    # Refurb & Rent - Property Value (bottom of green stack)
    fig_breakdown.add_trace(
        go.Bar(
            name="Refurb: Property",
            x=df_base['Year'],
            y=df_base['Property Value (Refurb)'],
            marker_color="#2ca02c",
            customdata=df_base[['Property Value (Refurb)', 'Cash (Refurb)', 'Total (Refurb)']].values,
            hovertemplate="<b>Refurb & Rent (Year %{x})</b><br>" +
                          "Property: $%{customdata[0]:,.0f}<br>" +
                          "Cash: $%{customdata[1]:,.0f}<br>" +
                          "Total: $%{customdata[2]:,.0f}<extra></extra>",
            offsetgroup=1
        )
    )
    # Refurb & Rent - Positive Cash (top of green stack)
    fig_breakdown.add_trace(
        go.Bar(
            name="Refurb: Cash",
            x=df_base['Year'],
            y=df_base['Cash (Refurb) Positive'],
            marker_color="#98df8a",
            customdata=df_base[['Property Value (Refurb)', 'Cash (Refurb)', 'Total (Refurb)']].values,
            hovertemplate="<b>Refurb & Rent (Year %{x})</b><br>" +
                          "Property: $%{customdata[0]:,.0f}<br>" +
                          "Cash: $%{customdata[1]:,.0f}<br>" +
                          "Total: $%{customdata[2]:,.0f}<extra></extra>",
            offsetgroup=1,
            base=df_base['Property Value (Refurb)']
        )
    )
    # Refurb & Rent - Negative Cash (red portion showing cost on top)
    fig_breakdown.add_trace(
        go.Bar(
            name="Refurb: Cost",
            x=df_base['Year'],
            y=-df_base['Cash (Refurb) Negative'],  # Make positive for display
            marker_color="#d62728",  # Red
            customdata=df_base[['Property Value (Refurb)', 'Cash (Refurb)', 'Total (Refurb)']].values,
            hovertemplate="<b>Refurb & Rent (Year %{x})</b><br>" +
                          "Property: $%{customdata[0]:,.0f}<br>" +
                          "Cash: $%{customdata[1]:,.0f}<br>" +
                          "Total: $%{customdata[2]:,.0f}<extra></extra>",
            offsetgroup=1,
            base=df_base['Property Value (Refurb)'] + df_base['Cash (Refurb) Positive']
        )
    )

    fig_breakdown.update_layout(
        barmode='group',
        height=400,
        yaxis_tickformat="$,.0f",
        yaxis_title="Total Wealth ($)",
        xaxis_title="Year",
        xaxis=dict(dtick=1),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )

    st.plotly_chart(fig_breakdown, use_container_width=True)
    st.caption("*Cash assumes reinvested rental income compounds in the market and is not taxed on earnings until withdrawal.*")

    # Find the crossover point for Refurb & Rent
    crossover_year = None
    for idx, row in df_base.iterrows():
        if row["Refurb & Rent"] > row["Sell As-Is"] and crossover_year is None:
            crossover_year = row["Year"]
            break

    if crossover_year:
        st.info(f"📈 **Crossover Point:** The 'Refurb & Rent' strategy surpasses 'Sell As-Is' at **Year {crossover_year}**")

    st.markdown("---")

    # Summary Metrics
    st.subheader("Final Wealth at Year 25")
    final = df_base.iloc[-1]
    final_low = df_low.iloc[-1]
    final_high = df_high.iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🏠 Rent As-Is",
            value=f"${final['Rent As-Is']:,.0f}"
        )
        st.caption(f"Range: ${final_low['Rent As-Is']:,.0f} - ${final_high['Rent As-Is']:,.0f}")

    with col2:
        st.metric(
            label="🔨 Refurb & Rent",
            value=f"${final['Refurb & Rent']:,.0f}"
        )
        st.caption(f"Range: ${final_low['Refurb & Rent']:,.0f} - ${final_high['Refurb & Rent']:,.0f}")

    with col3:
        st.metric(
            label="💰 Sell As-Is",
            value=f"${final['Sell As-Is']:,.0f}"
        )
        st.caption(f"Range: ${final_low['Sell As-Is']:,.0f} - ${final_high['Sell As-Is']:,.0f}")

    with col4:
        st.metric(
            label="🏗️ Refurb & Sell",
            value=f"${final['Refurb & Sell']:,.0f}"
        )
        st.caption(f"Range: ${final_low['Refurb & Sell']:,.0f} - ${final_high['Refurb & Sell']:,.0f}")

    st.markdown("---")

    # Strategy Explanation
    st.subheader("Understanding the Strategies")

    exp1, exp2 = st.columns(2)

    with exp1:
        st.markdown("#### 🏠 Rent Strategies")
        st.markdown(f"""
        **Rent As-Is:** Keep the property in current condition, collect rent, and reinvest
        the after-tax cash flow into the market.

        **Refurb & Rent (Forced Equity Play):** Invest upfront to unlock higher rent AND
        immediate equity. The \\${refurb_cost:,} investment creates ~\\${val_refurb - val_as_is:,} in equity
        while also increasing monthly cash flow by \\${rent_refurb - rent_as_is:,}.

        *Rental income is taxed at {income_tax_rate*100:.0f}% but reduced by the \\${annual_depreciation:,.0f}/yr
        depreciation shield. Market gains on reinvested cash are tax-free.*
        """)

    with exp2:
        st.markdown("#### 💰 Sell Strategies")
        st.markdown(f"""
        **Sell As-Is:** Immediately liquidate the property (minus 6% closing costs) and
        invest the proceeds in the stock market.

        **Refurb & Sell:** Spend \\${refurb_cost:,} to increase the sale price from \\${val_as_is:,} to \\${val_refurb:,},
        then invest the larger proceeds.

        *Market gains compound tax-free in this model. These strategies provide immediate
        liquidity but lose the depreciation tax shield.*
        """)

# ============ TAB 2: RATE ASSUMPTIONS ============
with tab2:
    st.header("Understanding the Rate Assumptions")
    st.markdown("*Why the default values were chosen and what they mean*")

    rate1, rate2 = st.columns(2)

    with rate1:
        st.markdown("#### Market Portfolio Return (Default: 6%)")
        st.markdown("""
        This represents the expected annual return from investing in a diversified stock portfolio.

        **Historical Context:**
        - S&P 500 average return (1928-2024): ~10% nominal, ~7% inflation-adjusted
        - Vanguard Total Stock Market (VTI) 10-year return: ~11%
        - Conservative estimate accounts for sequence-of-returns risk and fees

        **Why 6%?** A conservative estimate that accounts for inflation, fees, and the reality
        that future returns may be lower than historical averages. Bumping to 8-10% represents
        a more optimistic scenario.
        """)

        st.markdown("#### Property Appreciation (Default: 3%)")
        st.markdown("""
        The expected annual increase in your property's market value.

        **Historical Context:**
        - U.S. national average (1991-2024): ~3.5-4% nominal
        - Montgomery County, TX (2019-2024): ~5-8% (post-pandemic boom)
        - Long-term sustainable growth typically tracks inflation + 1%

        **Why 3%?** Conservative baseline that assumes the post-pandemic boom normalizes.
        Montgomery County's growth may continue above average due to Houston expansion,
        but 3% is a safe planning assumption.
        """)

    with rate2:
        st.markdown("#### Annual Rent Growth (Default: 2.5%)")
        st.markdown("""
        How much you can increase rent each year while remaining competitive.

        **Historical Context:**
        - National average rent growth (2010-2024): ~3-4%
        - Texas rent growth tends to be slightly lower due to no income tax migration
        - Rent typically grows slower than property values in appreciating markets

        **Why 2.5%?** Matches historical inflation and represents sustainable growth.
        Higher rates (3-4%) are achievable in strong markets, but tenant turnover risk
        increases with aggressive rent increases.
        """)

        st.markdown("#### Vacancy Rate (Default: 5%)")
        st.markdown("""
        Percentage of time the property sits empty (turnover, repairs, finding tenants).

        **Industry Benchmarks:**
        - Well-managed single-family: 3-5%
        - Average rental market: 5-8%
        - Challenging markets: 8-12%

        **Why 5%?** Represents ~18 days/year of vacancy, typical for a desirable property
        in a good location. A waterside townhouse in April Sound should command strong
        tenant interest, supporting this conservative estimate.
        """)

# ============ TAB 3: COMPARABLES ============
with tab3:
    st.header("Comparable Properties in April Sound")
    st.markdown("*Market data to support the value and rent estimates*")

    st.subheader("🏠 Nearby Sales & Listings")
    st.markdown("""
    | Address | Sq Ft | Beds/Baths | Sale Price | Per Sq Ft | Condition | View | Status |
    |---------|-------|------------|------------|-----------|-----------|------|--------|
    | 144 April Point Dr S | 1,824 | 3/2.5 | \\$365,000 | \\$200 | Original | Open Water | Subject Property |
    | 143 April Point Dr S | 1,824 | 3/2.5 | \\$485,000 | \\$266 | Renovated | Open Water | Sold Jan 2025 |
    | 137 April Point Dr S | 1,824 | 3/2.5 | \\$510,000 | \\$280 | Renovated | Open Water | Sold Oct 2023 |
    | 132 April Point Dr S | 1,800 | 3/2.5 | \\$372,000 | \\$207 | Renovated | Water View | Sold 2023 |
    | 120 April Point Dr S | 1,750 | 3/2 | \\$349,000 | \\$199 | Original | Water View | Sold 2024 |
    | 156 April Point Dr N | 1,920 | 3/2.5 | \\$385,000 | \\$201 | Updated | Lakeside | Sold 2024 |
    """)

    st.markdown("---")

    st.subheader("💵 Rental Comparables")
    st.markdown("""
    | Address | Sq Ft | Beds/Baths | Monthly Rent | Per Sq Ft | Condition | View |
    |---------|-------|------------|--------------|-----------|-----------|------|
    | 144 April Point Dr S | 1,824 | 3/2.5 | \\$2,550 | \\$1.40 | Original (Subject) | Open Water |
    | 118 April Sound | 1,700 | 3/2 | \\$2,400 | \\$1.41 | Original | Interior |
    | 160 April Point Dr N | 1,950 | 3/2.5 | \\$2,800 | \\$1.44 | Updated | Lakeside |
    | 140 April Point Dr S | 1,850 | 3/2.5 | \\$3,200 | \\$1.73 | Renovated | Water View |
    | 128 April Sound | 2,000 | 4/3 | \\$3,500 | \\$1.75 | Renovated | Interior |
    """)

    st.info("""
    **Key Insight:** Renovated units command ~\\$1.73/sq ft vs \\$1.40/sq ft for original condition (~24% premium).
    Note: No open water view renovated rental comps exist - these premium units tend to sell rather than rent.
    Refurbished rent estimates are extrapolated from water view comps with a modest view premium.
    """)

    st.markdown("---")

    st.subheader("📊 Market Context")

    ctx1, ctx2 = st.columns(2)

    with ctx1:
        st.markdown("#### April Sound Community")
        st.markdown("""
        - **Location:** Waterside townhomes on Lake Conroe
        - **Community:** Gated with clubhouse, pools, golf course access
        - **HOA:** \\$272.56/quarter + \\$73/mo social membership
        - **Demographics:** Mix of retirees and Houston commuters
        - **Rental Demand:** Strong due to lake access and amenities
        """)

    with ctx2:
        st.markdown("#### Montgomery County, TX Trends")
        st.markdown("""
        - **2019-2024 Appreciation:** ~5-8% annually (post-pandemic boom)
        - **Current Market:** Stabilizing but still above national average
        - **Population Growth:** Houston metro expanding northward
        - **Employment:** Strong healthcare, energy, and remote work presence
        - **Rental Vacancy:** ~4-6% in desirable areas
        """)

    st.markdown("---")

    st.subheader("🏗️ Refurbishment Value Analysis")

    st.markdown(f"""
    | Metric | As-Is | After Refurb | Gain |
    |--------|-------|--------------|------|
    | **Property Value** | \\${val_as_is:,} | \\${val_refurb:,} | +\\${val_refurb - val_as_is:,} |
    | **Monthly Rent** | \\${rent_as_is:,} | \\${rent_refurb:,} | +\\${rent_refurb - rent_as_is:,}/mo |
    | **Annual Rent** | \\${rent_as_is * 12:,} | \\${rent_refurb * 12:,} | +\\${(rent_refurb - rent_as_is) * 12:,}/yr |
    | **Rent per Sq Ft** | \\${rent_as_is / 1824:.2f} | \\${rent_refurb / 1824:.2f} | +\\${(rent_refurb - rent_as_is) / 1824:.2f} |
    | **Cap Rate** | {((rent_as_is * 12 * 0.65) / val_as_is) * 100:.1f}% | {((rent_refurb * 12 * 0.65) / val_refurb) * 100:.1f}% | - |
    """)

    st.success(f"""
    **Forced Equity Play:** A \\${refurb_cost:,} investment creates \\${val_refurb - val_as_is:,} in immediate equity
    (a {((val_refurb - val_as_is) / refurb_cost - 1) * 100:.0f}% return on renovation cost) while also increasing
    annual rental income by \\${(rent_refurb - rent_as_is) * 12:,}.
    """)

# ============ TAB 4: TAX CONSIDERATIONS ============
with tab4:
    st.header("The Tax Advantage of Holding Real Estate")

    # Tax Treatment Summary
    st.subheader("📋 Tax Treatment in This Model")
    st.markdown(f"""
    | Income Type | Tax Rate | Notes |
    |-------------|----------|-------|
    | **Rental Income** | {income_tax_rate*100:.0f}% | Reduced by depreciation deduction |
    | **Depreciation Shield** | -\\${annual_depreciation:,.0f}/yr | Offsets taxable rental income |
    | **Market Gains (Reinvested Cash)** | 0% | Assumed tax-deferred or long-term |
    | **Market Gains (Sell Scenarios)** | 0% | Assumed tax-deferred or long-term |
    """)

    st.markdown("---")

    # Depreciation Section
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏛️ Annual Depreciation Deduction")
        st.markdown(f"""
        Based on your tax records, the **Improvement Value** (building only, excluding land) is:

        **\\${building_value:,.0f}**

        The IRS allows you to depreciate residential rental property over **27.5 years**.
        """)

        st.success(f"""
        **Annual Depreciation Deduction: \\${annual_depreciation:,.2f}**

        This "paper loss" reduces your taxable rental income each year.
        """)

    with col2:
        st.subheader("💡 What This Means")
        # Calculate Year 1 NOI for example
        yr1_noi = (rent_as_is * 12) - (val_as_is * expense_rate) - hoa_annual
        yr1_taxable = max(0, yr1_noi - annual_depreciation)
        yr1_tax_without = yr1_noi * income_tax_rate
        yr1_tax_with = yr1_taxable * income_tax_rate

        st.markdown(f"""
        **Year 1 Example (As-Is):**

        | Without Depreciation | With Depreciation |
        |---------------------|-------------------|
        | NOI: \\${yr1_noi:,.0f} | NOI: \\${yr1_noi:,.0f} |
        | Taxable: \\${yr1_noi:,.0f} | Taxable: \\${yr1_taxable:,.0f} |
        | Tax @ {income_tax_rate*100:.0f}%: \\${yr1_tax_without:,.0f} | Tax @ {income_tax_rate*100:.0f}%: \\${yr1_tax_with:,.0f} |

        **Annual Tax Savings: ~\\${yr1_tax_without - yr1_tax_with:,.0f}**
        """)

    st.markdown("---")

    # Cumulative Tax Shield
    st.subheader("📊 Cumulative Tax Shield Over Time")

    tax_shield_df = pd.DataFrame({
        "Year": range(1, 26),
        "Annual Depreciation": [annual_depreciation] * 25,
        "Cumulative Depreciation": [annual_depreciation * i for i in range(1, 26)],
        "Estimated Tax Savings": [annual_depreciation * income_tax_rate * i for i in range(1, 26)]
    })

    fig_tax = go.Figure()
    fig_tax.add_trace(go.Bar(
        x=tax_shield_df["Year"],
        y=tax_shield_df["Estimated Tax Savings"],
        name="Cumulative Tax Savings",
        marker_color="#2ca02c"
    ))
    fig_tax.update_layout(
        title=f"Cumulative Tax Savings from Depreciation (@ {income_tax_rate*100:.0f}% rate)",
        xaxis_title="Year",
        yaxis_title="Tax Savings ($)",
        yaxis_tickformat="$,.0f",
        height=400
    )
    st.plotly_chart(fig_tax, use_container_width=True)

    st.info(f"""
    **25-Year Total Depreciation:** \\${annual_depreciation * 25:,.0f}

    **Estimated Tax Savings (@ {income_tax_rate*100:.0f}% marginal rate):** \\${annual_depreciation * 25 * income_tax_rate:,.0f}

    *Note: Depreciation is "recaptured" at 25% when you eventually sell, but you've had
    the use of that money for decades of compounding.*
    """)

    st.markdown("---")

    # Year-by-Year Breakdown Table
    st.subheader("📋 Year-by-Year Wealth Breakdown (Base Scenario)")

    display_cols = ["Year", "Rent As-Is", "Refurb & Rent", "Sell As-Is", "Refurb & Sell",
                   "Property Value (As-Is)", "Cash (As-Is)"]

    # Format for display
    st.dataframe(
        df_base[display_cols].style.format({
            "Rent As-Is": "${:,.0f}",
            "Refurb & Rent": "${:,.0f}",
            "Sell As-Is": "${:,.0f}",
            "Refurb & Sell": "${:,.0f}",
            "Property Value (As-Is)": "${:,.0f}",
            "Cash (As-Is)": "${:,.0f}",
        }),
        use_container_width=True,
        height=400
    )

    # Download button
    csv = df_base.to_csv(index=False)
    st.download_button(
        label="📥 Download Full Data as CSV",
        data=csv,
        file_name="investment_analysis.csv",
        mime="text/csv"
    )

    st.markdown("---")

    # ROI Comparison
    st.subheader("📈 Return on Investment Comparison")

    roi_data = {
        "Strategy": ["Rent As-Is", "Refurb & Rent", "Sell As-Is", "Refurb & Sell"],
        "Initial Investment": [
            val_as_is,
            val_as_is + refurb_cost,
            val_as_is * (1 - selling_costs),
            val_as_is + refurb_cost
        ],
        "Final Value (Yr 25)": [
            final["Rent As-Is"],
            final["Refurb & Rent"],
            final["Sell As-Is"],
            final["Refurb & Sell"]
        ]
    }
    roi_df = pd.DataFrame(roi_data)
    roi_df["Total Return"] = roi_df["Final Value (Yr 25)"] - roi_df["Initial Investment"]
    roi_df["ROI %"] = ((roi_df["Final Value (Yr 25)"] / roi_df["Initial Investment"]) - 1) * 100
    roi_df["Annualized ROI %"] = ((roi_df["Final Value (Yr 25)"] / roi_df["Initial Investment"]) ** (1/25) - 1) * 100

    st.dataframe(
        roi_df.style.format({
            "Initial Investment": "${:,.0f}",
            "Final Value (Yr 25)": "${:,.0f}",
            "Total Return": "${:,.0f}",
            "ROI %": "{:.1f}%",
            "Annualized ROI %": "{:.2f}%"
        }),
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🏛️ Tax Record Information")
    st.markdown(f"""
    | Tax Component | Value |
    |---------------|-------|
    | **Building/Improvement Value** | \\${building_value:,} |
    | **Annual Depreciation (27.5 yr)** | \\${annual_depreciation:,.2f} |
    | **Property Tax Rate** | {property_tax_rate*100:.1f}% |
    | **Annual Property Tax (As-Is)** | \\${val_as_is * property_tax_rate:,.0f} |
    """)

    st.markdown("---")

    st.subheader("🌴 The Texas Advantage")
    st.success("""
    **No State Income Tax:** Texas has no state income tax, meaning 100% of your
    rental income and capital gains stay in your pocket at the state level.

    **Primary Residence Strategy:** If you or a family member lives in the property
    for 2 of the 5 years before selling, you can exclude up to \\$250,000 (single) or
    \\$500,000 (married) of capital gains from federal taxes.
    """)

# ============ TAB 5: PROPERTY SPECS ============
with tab5:
    st.header("Property Details: 144 April Point Dr S")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏠 Physical Characteristics")
        st.markdown(f"""
        | Feature | Value |
        |---------|-------|
        | **Square Footage** | 1,824 sq. ft. |
        | **Location** | Montgomery, TX |
        | **Community** | April Sound (Waterside) |
        | **Property Type** | Townhouse |
        """)

        st.subheader("💵 Current Valuations")
        st.markdown(f"""
        | Condition | Market Value | Monthly Rent |
        |-----------|--------------|--------------|
        | **As-Is** | \\${val_as_is_low:,} - \\${val_as_is:,} - \\${val_as_is_high:,} | \\${rent_as_is_low:,} - \\${rent_as_is:,} - \\${rent_as_is_high:,}/mo |
        | **Refurbished** | \\${val_refurb_low:,} - \\${val_refurb:,} - \\${val_refurb_high:,} | \\${rent_refurb_low:,} - \\${rent_refurb:,} - \\${rent_refurb_high:,}/mo |
        """)

    with col2:
        st.subheader("📊 Financial Summary")

        # As-Is Annual Numbers
        annual_rent_as_is = rent_as_is * 12
        annual_expenses_as_is = (val_as_is * expense_rate) + hoa_annual
        noi_as_is = annual_rent_as_is - annual_expenses_as_is
        cap_rate_as_is = (noi_as_is / val_as_is) * 100

        # Refurb Annual Numbers
        annual_rent_refurb = rent_refurb * 12
        annual_expenses_refurb = (val_refurb * expense_rate) + hoa_annual
        noi_refurb = annual_rent_refurb - annual_expenses_refurb
        cap_rate_refurb = (noi_refurb / val_refurb) * 100

        st.markdown(f"""
        **As-Is Scenario (Year 1):**
        | Metric | Value |
        |--------|-------|
        | Gross Annual Rent | \\${annual_rent_as_is:,} |
        | Annual Expenses | \\${annual_expenses_as_is:,.0f} |
        | Net Operating Income | \\${noi_as_is:,.0f} |
        | Cap Rate | {cap_rate_as_is:.2f}% |

        **Refurbished Scenario (Year 1):**
        | Metric | Value |
        |--------|-------|
        | Gross Annual Rent | \\${annual_rent_refurb:,} |
        | Annual Expenses | \\${annual_expenses_refurb:,.0f} |
        | Net Operating Income | \\${noi_refurb:,.0f} |
        | Cap Rate | {cap_rate_refurb:.2f}% |
        """)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Last Updated: February 2, 2026</p>
    <p>Built by Theo Douwes</p>
</div>
""", unsafe_allow_html=True)
