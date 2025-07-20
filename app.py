import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Crypto Screener (Coingecko)", layout="wide")
st.title("📊 Real-Time Crypto Screener (Top 250 Coins)")

@st.cache_data(ttl=60)
def load_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": 1,
        "sparkline": False
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        st.error(f"❌ Failed to fetch data from Coingecko: {e}")
        st.stop()

    df = pd.DataFrame(data)
    df = df[["id", "symbol", "name", "current_price", "price_change_percentage_24h", "market_cap"]]
    df.rename(columns={
        "id": "ID",
        "symbol": "Symbol",
        "name": "Name",
        "current_price": "Price (USD)",
        "price_change_percentage_24h": "24h Change (%)",
        "market_cap": "Market Cap"
    }, inplace=True)

    df["24h Change (%)"] = df["24h Change (%)"].round(2)
    df.sort_values(by="24h Change (%)", ascending=False, inplace=True)
    return df

# Load and display data
df = load_data()

coin = st.selectbox("🔍 Select a Coin", df["Name"].tolist())
selected = df[df["Name"] == coin]

st.metric(label=f"{selected['Name'].values[0]} Price", value=f"${selected['Price (USD)'].values[0]:,.2f}")
st.metric(label="24h Change (%)", value=f"{selected['24h Change (%)'].values[0]:.2f}%")

with st.expander("📋 View Top 250 Coins by Market Cap"):
    st.dataframe(df.reset_index(drop=True), use_container_width=True)
