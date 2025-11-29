import streamlit as st
import math

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Universal Franchise Calculator",
    page_icon="💰",
    layout="wide"
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    .upsell-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff4b4b;
        text-align: center;
        margin-top: 30px;
    }
    .verdict-box {
        padding: 15px;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        font-size: 24px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND LOGIC: INDUSTRY PROFILES ---
# Logic: different industries have different cost structures.
# COGS: Cost of Goods Sold (%)
# Labor: Staffing costs (%)
# Misc: Utilities/Marketing/Admin (%)
INDUSTRY_PROFILES = {
    "F&B (Cafe/QSR)": {
        "cogs": 0.32,      # High food cost
        "labor": 0.25,     # High staffing needs
        "misc": 0.15,      # Utilities/Wastage
        "desc": "High volume, high waste, labor intensive."
    },
    "Fitness/Gym": {
        "cogs": 0.05,      # No physical goods
        "labor": 0.20,     # Trainers/Front desk
        "misc": 0.25,      # High marketing & maintenance
        "desc": "Recurring revenue, high rent, high equipment cost."
    },
    "Retail (Clothing/Goods)": {
        "cogs": 0.40,      # Inventory cost is high
        "labor": 0.15,     # Floor staff
        "misc": 0.10,      # Theft/Utilities
        "desc": "Inventory management is the killer."
    },
    "Cloud Kitchen": {
        "cogs": 0.35,      # Food cost
        "labor": 0.20,     # Cooks
        "misc": 0.30,      # Aggregator Commissions (UberEats/DoorDash take ~30%)
        "desc": "Low rent, but the apps take your margin."
    },
    "Service (Salon/Spa)": {
        "cogs": 0.10,      # Consumables
        "labor": 0.45,     # Highly skilled labor is expensive
        "misc": 0.10,      # Laundry/Utilities
        "desc": "Staff retention is your biggest risk."
    }
}

# --- SIDEBAR INPUTS ---
st.sidebar.header("🧮 Franchise Inputs")

industry = st.sidebar.selectbox(
    "Select Industry Type",
    options=list(INDUSTRY_PROFILES.keys())
)

st.sidebar.subheader("Financials")
setup_cost = st.sidebar.number_input("Total Setup Cost ($)", min_value=1000, value=150000, step=1000)
rent = st.sidebar.number_input("Monthly Rent ($)", min_value=0, value=4000, step=100)
footfall = st.sidebar.number_input("Daily Footfall (Customers)", min_value=1, value=80, step=1)
ticket_size = st.sidebar.number_input("Average Ticket Size ($)", min_value=1.0, value=15.0, step=0.5)

# --- CALCULATIONS ---
profile = INDUSTRY_PROFILES[industry]

# Revenue
daily_revenue = footfall * ticket_size
monthly_revenue = daily_revenue * 30
annual_revenue = monthly_revenue * 12

# Costs
monthly_cogs = monthly_revenue * profile['cogs']
monthly_labor = monthly_revenue * profile['labor']
monthly_misc = monthly_revenue * profile['misc']
total_monthly_expenses = rent + monthly_cogs + monthly_labor + monthly_misc

# Profit
monthly_net_profit = monthly_revenue - total_monthly_expenses
annual_net_profit = monthly_net_profit * 12
margin_percent = (monthly_net_profit / monthly_revenue) * 100 if monthly_revenue > 0 else 0

# ROI / Payback
if monthly_net_profit > 0:
    payback_months = setup_cost / monthly_net_profit
    payback_years = payback_months / 12
else:
    payback_months = float('inf')
    payback_years = float('inf')

# --- GENERATING THE NARRATIVES ---

# 1. The Verdict
verdict_color = "red"
verdict_text = "RED LIGHT"
verdict_sub = "Do not sign this lease."

if monthly_net_profit <= 0:
    verdict_text = "RED LIGHT (Negative Cashflow)"
    verdict_sub = "You are paying to work here. Burn this plan."
    verdict_color = "#ff4b4b"
elif payback_months > 36:
    verdict_text = "RED LIGHT (Slow ROI)"
    verdict_sub = f"It takes {payback_months:.1f} months to get your money back. Too risky."
    verdict_color = "#ff4b4b"
elif payback_months > 18:
    verdict_text = "YELLOW LIGHT (Grind Mode)"
    verdict_sub = "It works, but you're buying yourself a job, not a business."
    verdict_color = "#ffa500"
else:
    verdict_text = "GREEN LIGHT (Money Printer)"
    verdict_sub = f"ROI in {payback_months:.1f} months. Scale this immediately."
    verdict_color = "#0df2c9"

# 2. Reality Check (The Pessimist)
reality_check = ""
if industry == "F&B (Cafe/QSR)":
    reality_check = f"Your COGS are {profile['cogs']*100}%. If ingredients go up by 5% or your chef quits, that ${monthly_net_profit:,.0f} profit vanishes. Have you accounted for spoilage?"
elif industry == "Fitness/Gym":
    reality_check = f"Rent is a fixed killer here. If footfall drops to {int(footfall*0.7)}, you still pay full rent. Plus, equipment maintenance will eat your cash flow in Year 2."
elif industry == "Cloud Kitchen":
    reality_check = "You saved on rent, but the aggregators are taking 30% off the top. You don't own the customer; the app does. One algorithm change and you're invisible."
elif industry == "Service (Salon/Spa)":
    reality_check = f"Your labor is {profile['labor']*100}% of revenue. If your best stylist leaves and takes 20 clients, this model collapses."
else:
    reality_check = f"You are banking on {footfall} people every single day. If it rains for a week, do you have the working capital to cover that ${rent:,.0f} rent?"

# 3. The Jay Pitch (The Optimist/Salesman)
jay_pitch = ""
if monthly_net_profit > 0:
    jay_pitch = f"Look at the upside. We're generating ${annual_revenue:,.0f} top line. With a {margin_percent:.1f}% margin, this is a scalable cash cow. Put a manager in place, optimize the COGS, and we franchise this to 10 locations in 5 years."
else:
    jay_pitch = "Okay, the numbers look rough now, but this is a 'turnaround play.' If we renegotiate rent and double the ticket size through upsells, we flip this asset."

# --- MAIN UI LAYOUT ---

st.title("Universal Franchise Calculator 🏦")
st.markdown(f"**Industry Model:** {industry} | **Profile:** {profile['desc']}")

# Top Level Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Revenue", f"${monthly_revenue:,.0f}", f"Annual: ${annual_revenue:,.0f}")
col2.metric("Monthly Expenses", f"${total_monthly_expenses:,.0f}", f"Rent: ${rent:,.0f}")
col3.metric("Net Profit (Monthly)", f"${monthly_net_profit:,.0f}", f"Margin: {margin_percent:.1f}%", delta_color="normal")

st.divider()

# The Verdict Section
st.markdown(f"""
<div class="verdict-box" style="background-color: {verdict_color}; color: black;">
    {verdict_text}<br>
    <span style="font-size: 16px; font-weight: normal;">{verdict_sub}</span>
</div>
""", unsafe_allow_html=True)

# Analysis Columns
c1, c2 = st.columns(2)

with c1:
    st.subheader("🧐 The Reality Check")
    st.info(reality_check)

with c2:
    st.subheader("🚀 The Jay Pitch")
    st.success(jay_pitch)

# --- THE UPSELL SECTION ---
st.markdown("---")

st.markdown("""
<div class="upsell-container">
    <h2>💼 Need to pitch this to an investor?</h2>
    <p>Investors don't just look at spreadsheets; they buy the vision. <br>
    Get the professional decks, legal templates, and financial models used to close deals.</p>
</div>
""", unsafe_allow_html=True)

col_spacer_l, col_btn, col_spacer_r = st.columns([1, 2, 1])
with col_btn:
    st.link_button("Download the Asset Kit 📂", "https://INSERT_LINK_HERE.com", use_container_width=True, type="primary")
