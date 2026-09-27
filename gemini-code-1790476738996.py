import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------------------------------------------------------
# SEITEN-KONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Trading Journal Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .metric-card {
        background-color: #1e222d;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #2a2e39;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSIONS & SPEICHER-INITIALISIERUNG
# -----------------------------------------------------------------------------
if 'trades' not in st.session_state:
    # Beispieldaten zum Start
    st.session_state.trades = pd.DataFrame([
        {"ID": 1, "Date": "2026-05-24", "Symbol": "NVDA", "Side": "LONG", "Entry": 1024.87, "Target": 1120.00, "Stop": 975.00, "PnL": 955.00, "Setup": "Breakout", "Score": 85},
        {"ID": 2, "Date": "2026-05-24", "Symbol": "AAPL", "Side": "LONG", "Entry": 178.50, "Target": 187.50, "Stop": 170.00, "PnL": 153.60, "Setup": "Pullback", "Score": 78},
        {"ID": 3, "Date": "2026-05-23", "Symbol": "TSLA", "Side": "LONG", "Entry": 185.00, "Target": 195.00, "Stop": 180.00, "PnL": -620.45, "Setup": "Reversal", "Score": 60},
        {"ID": 4, "Date": "2026-05-22", "Symbol": "MSFT", "Side": "SHORT", "Entry": 415.00, "Target": 400.00, "Stop": 420.00, "PnL": 502.00, "Setup": "Trend Continuation", "Score": 90}
    ])

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.title("📈 Trading Journal Pro")
st.sidebar.caption("100% Private. Local Execution.")

page = st.sidebar.radio(
    "Navigation", 
    ["Dashboard & Risk Sizing", "Trades Log", "Performance Analytics", "Setup Score Calculator", "Settings"]
)

st.sidebar.divider()
st.sidebar.info("💡 Tip: Multi-Asset Trade Tracking & Guardrails enabled.")

# -----------------------------------------------------------------------------
# 1. DASHBOARD & RISK-BASED POSITION SIZING
# -----------------------------------------------------------------------------
if page == "Dashboard & Risk Sizing":
    st.title("📊 Today's Overview & Position Sizing")
    
    # Key Metrics Header
    col1, col2, col3, col4 = st.columns(4)
    today_pnl = st.session_state.trades["PnL"].sum()
    
    col1.metric("Today's P&L", f"${today_pnl:,.2f}", "+1.2%")
    col2.metric("Consecutive Losses", "1 / 3")
    col3.metric("Guardrails Status", "🟢 OK (Within Limits)")
    col4.metric("Win Rate", f"{(len(st.session_state.trades[st.session_state.trades['PnL'] > 0]) / len(st.session_state.trades) * 100):.1f}%")

    st.divider()

    # Risk Calculator Section
    st.subheader("🧮 Risk-Based Position Sizing")
    col_calc_left, col_calc_right = st.columns(2)

    with col_calc_left:
        account_equity = st.number_input("Account Equity ($)", value=20135.00, step=500.0)
        risk_percentage = st.slider("Risk Target (%)", min_value=0.25, max_value=5.0, value=1.0, step=0.25)
        entry_price = st.number_input("Entry Price ($)", value=462.75, step=0.5)
        stop_loss = st.number_input("Stop Loss ($)", value=456.50, step=0.5)
        take_profit = st.number_input("Target Price ($)", value=480.00, step=0.5)

    with col_calc_right:
        risk_amount = account_equity * (risk_percentage / 100)
        stop_distance = abs(entry_price - stop_loss)
        
        if stop_distance > 0:
            suggested_qty = int(risk_amount / stop_distance)
            planned_rr = abs(take_profit - entry_price) / stop_distance
        else:
            suggested_qty = 0
            planned_rr = 0.0

        st.markdown(f"""
        ### Calculation Results
        * **Risk Amount:** `${risk_amount:,.2f}`
        * **Stop Distance:** `${stop_distance:,.2f}`
        * **Suggested Shares / Units:** `{suggested_qty}`
        * **Planned Risk/Reward (R:R):** `{planned_rr:.2f}`
        """)

        if st.button("Start Session / Save Plan", type="primary"):
            st.success("Session configured successfully with current Risk Parameters!")

# -----------------------------------------------------------------------------
# 2. TRADES LOG & ENTRY
# -----------------------------------------------------------------------------
elif page == "Trades Log":
    st.title("📝 Trade Log")

    # Expandable Add Trade Form
    with st.expander("➕ Add New Trade", expanded=False):
        with st.form("new_trade_form"):
            f_col1, f_col2, f_col3 = st.columns(3)
            date = f_col1.date_input("Date", datetime.today())
            symbol = f_col2.text_input("Symbol", "NVDA").upper()
            side = f_col3.selectbox("Side", ["LONG", "SHORT"])

            f_col4, f_col5, f_col6 = st.columns(3)
            entry = f_col4.number_input("Entry Price", value=100.0)
            target = f_col5.number_input("Target Price", value=110.0)
            stop = f_col6.number_input("Stop Loss", value=95.0)

            f_col7, f_col8 = st.columns(2)
            pnl = f_col7.number_input("Realized PnL ($)", value=0.0)
            setup = f_col8.selectbox("Setup Type", ["Breakout", "Pullback", "Reversal", "Trend Continuation"])

            submit = st.form_submit_button("Save Trade")
            if submit:
                new_data = pd.DataFrame([{
                    "ID": len(st.session_state.trades) + 1,
                    "Date": str(date),
                    "Symbol": symbol,
                    "Side": side,
                    "Entry": entry,
                    "Target": target,
                    "Stop": stop,
                    "PnL": pnl,
                    "Setup": setup,
                    "Score": 75
                }])
                st.session_state.trades = pd.concat([st.session_state.trades, new_data], ignore_index=True)
                st.success("Trade successfully recorded!")

    # Display Trade Table
    st.dataframe(st.session_state.trades, use_container_width=True)

# -----------------------------------------------------------------------------
# 3. PERFORMANCE ANALYTICS & EDGE LAB
# -----------------------------------------------------------------------------
elif page == "Performance Analytics":
    st.title("📉 Performance Analytics")

    trades_df = st.session_state.trades
    total_trades = len(trades_df)
    winning_trades = trades_df[trades_df["PnL"] > 0]
    losing_trades = trades_df[trades_df["PnL"] < 0]

    winrate = (len(winning_trades) / total_trades * 100) if total_trades > 0 else 0
    gross_profit = winning_trades["PnL"].sum()
    gross_loss = abs(losing_trades["PnL"].sum())
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else gross_profit

    # Performance Stats Header
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    p_col1.metric("Total Trades", total_trades)
    p_col2.metric("Winrate", f"{winrate:.1f}%")
    p_col3.metric("Net Profit", f"${trades_df['PnL'].sum():,.2f}")
    p_col4.metric("Profit Factor", f"{profit_factor:.2f}")

    st.divider()

    # Equity Curve Chart
    st.subheader("Equity Curve")
    trades_df_sorted = trades_df.sort_values(by="Date").copy()
    trades_df_sorted["Cumulative_PnL"] = trades_df_sorted["PnL"].cumsum() + 20000

    fig = px.line(
        trades_df_sorted, 
        x="Date", 
        y="Cumulative_PnL", 
        markers=True,
        title="Account Growth ($)",
        labels={"Cumulative_PnL": "Account Balance ($)", "Date": "Trade Date"}
    )
    fig.update_traces(line_color="#00c853", line_width=3)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# 4. SETUP SCORE CALCULATOR
# -----------------------------------------------------------------------------
elif page == "Setup Score Calculator":
    st.title("🎯 Score Every Setup")
    st.caption("Calculate a practical 0–100 quality score before entering a trade.")[cite: 1]

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        s_symbol = st.selectbox("Product", ["BTC/USD", "EUR/USD", "NVDA", "AAPL", "NQ Futures"])
        s_trend = st.checkbox("Trend Alignment (Higher Timeframe aligned?)", value=True)
        s_rsi = st.checkbox("RSI / Momentum Indicator Support?", value=True)
        s_rr = st.checkbox("Risk/Reward Ratio >= 1:2?", value=True)
        s_level = st.checkbox("At key Support/Resistance or Value Area?", value=False)

    with col_s2:
        score = 0
        if s_trend: score += 30
        if s_rsi: score += 20
        if s_rr: score += 30
        if s_level: score += 20

        st.metric("Quality Score", f"{score} / 100")
        
        if score >= 80:
            st.success("🟢 Strong Setup: High probability alignment.")
        elif score >= 50:
            st.warning("🟡 Moderate Setup: Exercise caution and strictly follow stop loss.")
        else:
            st.error("🔴 Weak Setup: Avoid trade or wait for better confluence.")

# -----------------------------------------------------------------------------
# 5. SETTINGS & GUARDRAILS
# -----------------------------------------------------------------------------
elif page == "Settings":
    st.title("⚙️ Config & Guardrails")
    
    st.subheader("Risk Guardrails")
    st.number_input("Daily Loss Limit ($)", value=500.0)
    st.number_input("Max Trades Per Day", value=5)
    st.number_input("Max Consecutive Losses Before Cooldown", value=3)

    st.divider()
    st.subheader("Data Management")
    st.download_button(
        label="Export Trades CSV",
        data=st.session_state.trades.to_csv(index=False),
        file_name="trading_journal_export.csv",
        mime="text/csv"
    )