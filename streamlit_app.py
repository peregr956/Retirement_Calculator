import streamlit as st
from simulator.user_profile import UserProfile
from simulator.investment_account import InvestmentAccount
from simulator.simulation_engine import SimulationEngine

def generate_contribution_list(start_value, years, growth_rate=0.03):
    return [round(start_value * ((1 + growth_rate) ** i), 2) for i in range(years)]

st.title("📈 Retirement Projection Simulator")

# --- User Profile ---
st.sidebar.header("User Profile")
current_age = st.sidebar.number_input("Current Age", value=35)
retirement_age = st.sidebar.number_input("Retirement Age", value=65)
end_age = st.sidebar.number_input("End Age", value=85)
salary = st.sidebar.number_input("Current Salary", value=100000)
salary_growth = st.sidebar.slider("Salary Growth Rate", 0.0, 0.10, 0.02)
inflation = st.sidebar.slider("Inflation Rate", 0.0, 0.10, 0.02)

user = UserProfile(current_age, retirement_age, end_age, salary, salary_growth, inflation)
projection_years = end_age - current_age + 1

# --- TSP ---
st.sidebar.subheader("TSP / 401(k)")
tsp_balance = st.sidebar.number_input("TSP Starting Balance", value=100000)
tsp_return = st.sidebar.slider("TSP Annual Return", 0.00, 0.15, 0.07)
tsp_max_out = st.sidebar.checkbox("Max Out TSP ($23,000 increasing)")

if tsp_max_out:
    tsp_contributions = generate_contribution_list(23000, projection_years)
else:
    tsp_contrib_input = st.sidebar.number_input("Annual TSP Contribution", value=22500)
    tsp_contributions = [tsp_contrib_input] * projection_years

tsp_match = st.sidebar.number_input("Employer Match", value=4500)

# --- IRA ---
st.sidebar.subheader("IRA")
ira_balance = st.sidebar.number_input("IRA Starting Balance", value=30000)
ira_return = st.sidebar.slider("IRA Annual Return", 0.00, 0.15, 0.07)
ira_max_out = st.sidebar.checkbox("Max Out IRA ($7,000 increasing)")

if ira_max_out:
    ira_contributions = generate_contribution_list(7000, projection_years)
else:
    ira_contrib_input = st.sidebar.number_input("Annual IRA Contribution", value=7000)
    ira_contributions = [ira_contrib_input] * projection_years

# --- Simulation ---
tsp = InvestmentAccount("TSP", tsp_balance, tsp_return, tsp_contributions, tsp_match)
ira = InvestmentAccount("IRA", ira_balance, ira_return, ira_contributions)
engine = SimulationEngine(user, [tsp, ira])
results = engine.run_projection()

# --- Output ---
st.subheader("Projection Results")
st.dataframe(results)
st.line_chart(results[[col for col in results.columns if "Today's $" in col]])
