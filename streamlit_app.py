import streamlit as st
from simulator.user_profile import UserProfile
from simulator.investment_account import InvestmentAccount
from simulator.simulation_engine import SimulationEngine

st.title("📈 Retirement Projection Simulator")

st.sidebar.header("User Profile")
current_age = st.sidebar.number_input("Current Age", value=35, min_value=18, max_value=100)
retirement_age = st.sidebar.number_input("Retirement Age", value=65, min_value=30, max_value=100)
end_age = st.sidebar.number_input("End of Life Age", value=85, min_value=retirement_age, max_value=120)
salary = st.sidebar.number_input("Current Salary ($)", value=100000)
salary_growth = st.sidebar.slider("Salary Growth Rate", 0.0, 0.10, 0.02)
inflation = st.sidebar.slider("Inflation Rate", 0.0, 0.10, 0.02)

st.sidebar.header("Investment Accounts")
tsp_balance = st.sidebar.number_input("TSP Starting Balance ($)", value=100000)
tsp_contrib = st.sidebar.number_input("Annual Contribution to TSP ($)", value=22500)
tsp_match = st.sidebar.number_input("Employer Match ($)", value=4500)
tsp_return = st.sidebar.slider("TSP Annual Return", 0.0, 0.15, 0.07)

ira_balance = st.sidebar.number_input("IRA Starting Balance ($)", value=30000)
ira_contrib = st.sidebar.number_input("Annual Contribution to IRA ($)", value=7000)
ira_return = st.sidebar.slider("IRA Annual Return", 0.0, 0.15, 0.07)

user = UserProfile(current_age, retirement_age, end_age, salary, salary_growth, inflation)

tsp = InvestmentAccount("TSP", tsp_balance, tsp_return, tsp_contrib, tsp_match)
ira = InvestmentAccount("IRA", ira_balance, ira_return, ira_contrib)

engine = SimulationEngine(user, [tsp, ira])
results = engine.run_projection()

st.subheader("Projection Results")
st.dataframe(results)

st.line_chart(results[[col for col in results.columns if "Today's $" in col]])
