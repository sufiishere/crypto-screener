import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Crypto Screener", layout="wide")
st.title("📊 Real-Time Crypto Screener (Binance - USDT Pairs)")

# Fetch Binance Data Safely
@st.cache_data(ttl=60)
def load_binance_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"  # use HTTPS
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raise error for bad status
        data = response.json()
    except Exception as e:
        st.error("❌ Error fetching data from Binance API.")
        st.stop()

    if isinstance(data, list):
        df = pd.DataFrame(data)
        df = df[df['symbol'].str.endswith('USDT')]
        df['priceChangePercent'] = df['priceChangePercent'].astype(float)
        df['lastPrice'] = df['lastPrice'].astype(float)
        df = df.sort_values(by='priceChangePercent', ascending=False)
        return df[['symbol', 'lastPrice', 'priceChangePercent']]
    else:
        st.error("❌ Unexpected data format received from Binance.")
        st.stop()

# Load data
df = load_binance_data()

# Coin dropdown
coin = st.selectbox("🔍 Select a Coin", df['symbol'].tolist())

# Show selected coin metrics
selected = df[df['symbol'] == coin]
st.metric(label=f"{coin} Price", value=selected['lastPrice'].values[0])
st.metric(label="24h Change (%)", value=f"{selected['priceChangePercent'].values[0]:.2f}%")

# Show full table (expandable)
with st.expander("📋 View All USDT Pairs"):
    st.dataframe(df.reset_index(drop=True))
