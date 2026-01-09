import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    layout="wide"
)

plt.style.use("seaborn-v0_8-whitegrid")

# --------------------------------------------------
# Custom CSS – FINAL UI
# --------------------------------------------------
st.markdown(
    """
    <style>
    /* Main app background (dark brown, readable with black & white text) */
    .stApp {
        background-color: #a89582;
        color: #000000;
    }

    /* Sidebar background: neutral light */
    section[data-testid="stSidebar"] {
        background-color: #f1f3f5;
    }

    /* Sidebar text: black */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div {
        color: #000000 !important;
    }

    /* Text input & selectbox background: light orange */
    section[data-testid="stSidebar"] input {
        background-color: #ffe8cc !important;
        color: #000000 !important;
        caret-color: #000000 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #ffe8cc !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] input {
        color: #000000 !important;
    }

    /* Headings */
    h1, h2, h3 {
        color: #3b2f2f;
        font-weight: 700;
    }

    /* KPI cards */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border-left: 6px solid #2f9e44;
        padding: 14px;
        border-radius: 10px;
    }

    /* KPI heading visibility FIX */
    div[data-testid="metric-container"] div:first-child {
        color: #000000 !important;
        opacity: 1 !important;
        font-weight: 600 !important;
        font-size: 0.9rem;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background-color: #ced4da;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.title("Stock Selector")

ticker = st.sidebar.text_input(
    "Stock Ticker",
    value="RELIANCE.NS"
)

time_range = st.sidebar.selectbox(
    "Time Range",
    ["1Y", "3Y", "5Y", "MAX"]
)

metric_view = st.sidebar.radio(
    "Metric to View",
    [
        "Closing Price",
        "Cumulative Returns",
        "Daily Returns",
        "Volatility",
        "Drawdown"
    ]
)

# --------------------------------------------------
# Helper functions
# --------------------------------------------------
def get_start_date(range_option):
    return {
        "1Y": "2023-01-01",
        "3Y": "2021-01-01",
        "5Y": "2019-01-01",
        "MAX": None
    }[range_option]


@st.cache_data
def load_stock_data(ticker, start=None):
    df = yf.download(ticker, start=start, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


# --------------------------------------------------
# Load data
# --------------------------------------------------
df = load_stock_data(ticker, get_start_date(time_range))

if df.empty:
    st.error("Invalid ticker or no data available.")
    st.stop()

# --------------------------------------------------
# Derived metrics
# --------------------------------------------------
df["Daily_Return"] = df["Close"].pct_change()
df["Cumulative_Return"] = (1 + df["Daily_Return"]).cumprod()
df["Volatility"] = df["Daily_Return"].rolling(20).std()

rolling_peak = df["Close"].cummax()
df["Drawdown"] = (df["Close"] - rolling_peak) / rolling_peak

# KPI values
latest_price = df["Close"].iloc[-1]
total_return = df["Cumulative_Return"].iloc[-1] - 1
avg_daily_return = df["Daily_Return"].mean()
annualized_volatility = df["Daily_Return"].std() * np.sqrt(252)
max_drawdown = df["Drawdown"].min()

stock_name = ticker.replace(".NS", "")

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown("## Stock Analysis Dashboard")
st.caption(f"**{ticker}** | Time Range: **{time_range}**")

# --------------------------------------------------
# KPI Summary
# --------------------------------------------------
st.markdown("### Key Metrics")

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Latest Price", f"₹ {latest_price:,.1f}")
k2.metric("Total Return", f"{total_return * 100:.1f}%")
k3.metric("Avg Daily Return", f"{avg_daily_return * 100:.2f}%")
k4.metric("Annualized Volatility", f"{annualized_volatility * 100:.1f}%")
k5.metric("Max Drawdown", f"{max_drawdown * 100:.1f}%")

st.markdown("---")

# --------------------------------------------------
# Metric Plot + Dynamic Observation
# --------------------------------------------------
st.markdown(f"### {metric_view}")

fig, ax = plt.subplots(figsize=(13, 5))

if metric_view == "Closing Price":
    ax.plot(df.index, df["Close"], linewidth=2)
    ax.set_ylabel("Price")

    start_price = df["Close"].iloc[0]
    end_price = df["Close"].iloc[-1]
    price_change_pct = (end_price - start_price) / start_price * 100

    observation = (
        f"{stock_name} stock moved from approximately ₹{start_price:,.0f} "
        f"to ₹{end_price:,.0f} over the selected period, representing a "
        f"{price_change_pct:.1f}% change in price. This reflects the overall "
        f"direction and strength of the stock’s trend."
    )

elif metric_view == "Cumulative Returns":
    ax.plot(df.index, df["Cumulative_Return"], linewidth=2)
    ax.set_ylabel("Cumulative Return")

    observation = (
        f"{stock_name} stock has delivered approximately "
        f"{total_return * 100:.1f}% cumulative returns over the selected "
        f"{time_range} period, indicating long-term wealth creation."
    )

elif metric_view == "Daily Returns":
    ax.plot(df.index, df["Daily_Return"], linewidth=1)
    ax.set_ylabel("Daily Return")

    max_daily = df["Daily_Return"].max() * 100
    min_daily = df["Daily_Return"].min() * 100

    observation = (
        f"{stock_name} stock’s daily returns ranged between "
        f"{min_daily:.2f}% and {max_daily:.2f}%, highlighting short-term "
        f"price volatility during the period."
    )

elif metric_view == "Volatility":
    ax.plot(df.index, df["Volatility"], linewidth=2)
    ax.set_ylabel("Rolling Volatility (20D)")

    vol_min = df["Volatility"].min() * 100
    vol_max = df["Volatility"].max() * 100

    observation = (
        f"{stock_name} stock’s rolling volatility ranged between "
        f"{vol_min:.2f}% and {vol_max:.2f}%, indicating varying levels "
        f"of risk and market uncertainty."
    )

else:  # Drawdown
    ax.plot(df.index, df["Drawdown"], linewidth=2)
    ax.set_ylabel("Drawdown")

    observation = (
        f"{stock_name} stock experienced a maximum drawdown of "
        f"{max_drawdown * 100:.1f}%, representing the worst historical "
        f"loss an investor could have faced."
    )

ax.set_xlabel("Date")
st.pyplot(fig)

st.markdown("#### Observation")
st.write(observation)

st.markdown("---")

