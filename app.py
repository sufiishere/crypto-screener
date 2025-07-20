import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Crypto Screener", layout="wide")
st.title("📊 Real-Time Crypto Screener (Binance - USDT Pairs)")

@st.cache_data(ttl=60)
def load_binance_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()

    if isinstance(data, list):
        df = pd.DataFrame(data)
        df = df[df['symbol'].str.endswith('USDT')]
        df['priceChangePercent'] = df['priceChangePercent'].astype(float)
        df['lastPrice'] = df['lastPrice'].astype(float)
        df = df.sort_values(by='priceChangePercent', ascending=False)
        return df[['symbol', 'lastPrice', 'priceChangePercent']]
    else:
        st.error("❌ Failed to fetch data from Binance API.")
        st.stop()

# Load data
df = load_binance_data()

# Dropdown to select a coin
coin = st.selectbox("Select a Coin:", df['symbol'].tolist())

# Show selected coin data
selected = df[df['symbol'] == coin]
st.metric(label=f"📈 {coin} Price", value=selected['lastPrice'].values[0])
st.metric(label="24h Change (%)", value=f"{selected['priceChangePercent'].values[0]:.2f}%")

# Optional: show full table
with st.expander("View All USDT Pairs"):
    st.dataframe(df.reset_index(drop=True))
