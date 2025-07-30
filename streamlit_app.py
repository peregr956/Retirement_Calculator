import streamlit as st
import plotly.graph_objects as go
from simulator.user_profile import UserProfile
from simulator.investment_account import InvestmentAccount
from simulator.simulation_engine import SimulationEngine

# --- Utility Function ---
def generate_contribution_list(start_value, years, growth_rate=0.03):
    return [round(start_value * ((1 + growth_rate) ** i), 2) for i in range(years)]

# --- App Title ---
st.title("📈 Retirement Projection Simulator")

# --- User Profile Inputs ---
st.sidebar.header("👤 User Profile")
current_age = st.sidebar.number_input("Current Age", value=35)
retirement_age = st.sidebar.number_input("Retirement Age", value=65)
end_age = st.sidebar.number_input("End Age", value=85)
salary = st.sidebar.number_input("Current Salary ($)", value=100000)
salary_growth = st.sidebar.slider("Salary Growth Rate (%)", 0.0, 10.0, 2.0) / 100
inflation = st.sidebar.slider("Inflation Rate (%)", 0.0, 10.0, 2.0) / 100

user = UserProfile(current_age, retirement_age, end_age, salary, salary_growth, inflation)
projection_years = end_age - current_age + 1

# --- 401(k) Inputs ---
st.sidebar.header("💼 401(k)")
k401_balance = st.sidebar.number_input("401(k) Starting Balance", value=100000)
k401_return = st.sidebar.slider("401(k) Annual Return (%)", 0.0, 15.0, 7.0) / 100
k401_max_out = st.sidebar.checkbox("Max Out 401(k) (Start at $23,000)")
employer_match_pct = st.sidebar.slider("Employer Match (% of Salary)", 0.0, 20.0, 5.0) / 100

if k401_max_out:
    k401_contributions = generate_contribution_list(23000, projection_years)
else:
    contrib = st.sidebar.number_input("Annual Contribution ($)", value=22500)
    k401_contributions = [contrib] * projection_years

# --- IRA Inputs ---
st.sidebar.header("🏦 IRA")
ira_balance = st.sidebar.number_input("IRA Starting Balance", value=30000)
ira_return = st.sidebar.slider("IRA Annual Return (%)", 0.0, 15.0, 7.0) / 100
ira_max_out = st.sidebar.checkbox("Max Out IRA (Start at $7,000)")

if ira_max_out:
    ira_contributions = generate_contribution_list(7000, projection_years)
else:
    ira_contrib = st.sidebar.number_input("Annual IRA Contribution ($)", value=7000)
    ira_contributions = [ira_contrib] * projection_years

# --- Build Accounts and Run Simulation ---
k401 = InvestmentAccount("401(k)", k401_balance, k401_return, k401_contributions, employer_match_pct)
ira = InvestmentAccount("IRA", ira_balance, ira_return, ira_contributions)
engine = SimulationEngine(user, [k401, ira])

results = engine.run_projection()
income_summary = engine.compute_monthly_income_at_retirement()

# --- Display Projection Table ---
st.subheader("📊 Projection Table")
st.dataframe(results.style.format("${:,.0f}"))

# --- Plotly Chart for Real Dollar Balances ---
st.subheader("📈 Inflation-Adjusted Balance Over Time")

fig = go.Figure()
for col in results.columns:
    if "(Today's $" in col:
        fig.add_trace(go.Scatter(
            x=results.index,
            y=results[col],
            mode='lines+markers',
            name=col.split(" ")[0],
            hovertemplate="Age: %{x}<br>Real Value: $%{y:,.0f}<extra></extra>"
        ))

fig.update_layout(
    xaxis_title="Age",
    yaxis_title="Inflation-Adjusted Balance ($)",
    hovermode="x unified",
    legend_title="Account"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("💰 Monthly Retirement Take-Home Pay")

st.markdown(
    """
    These estimates assume you fully deplete your accounts by end of retirement.

    - **Fixed purchasing power**: Withdrawals keep your lifestyle constant, adjusted for inflation.
    - **Growing withdrawals**: You increase your purchasing power each year (e.g. 2% real growth).
    """
)

# Merge both summaries
income_table = {
    "Account": [],
    "Fixed (Real $)": [],
    "Fixed (Nominal $)": [],
    "Growing (Real $)": [],
    "Growing (Nominal $)": []
}

for i in range(len(income_summary)):
    acc = income_summary[i]["account"]
    income_table["Account"].append(acc)
    income_table["Fixed (Real $)"].append(f"${income_summary[i]['real_monthly']:,.0f}")
    income_table["Fixed (Nominal $)"].append(f"${income_summary[i]['nominal_monthly_first_year']:,.0f}")
    income_table["Growing (Real $)"].append(f"${income_summary_growing[i]['real_monthly']:,.0f}")
    income_table["Growing (Nominal $)"].append(f"${income_summary_growing[i]['nominal_monthly_first_year']:,.0f}")

st.table(income_table)

