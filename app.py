import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Crypto Screener", layout="wide")
st.title("📊 Real-Time Crypto Screener (Binance - USDT Pairs)")

# Load Binance data with error handling
@st.cache_data(ttl=60)
def load_binance_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        st.error(f"❌ Error fetching data from Binance: {e}")
        st.stop()

    if not isinstance(data, list):
        st.error("❌ Unexpected data format received from Binance.")
        st.stop()

    try:
        df = pd.DataFrame(data)
        df = df[df['symbol'].str.endswith('USDT')]
        df['priceChangePercent'] = pd.to_numeric(df['priceChangePercent'], errors='coerce')
        df['lastPrice'] = pd.to_numeric(df['lastPrice'], errors='coerce')
        df = df.sort_values(by='priceChangePercent', ascending=False)
        return df[['symbol', 'lastPrice', 'priceChangePercent']]
    except Exception as e:
        st.error(f"❌ Error processing Binance data: {e}")
        st.stop()

# Load data
df = load_binance_data()

# UI components
coin = st.selectbox("🔍 Select a Coin", df['symbol'].tolist())

selected = df[df['symbol'] == coin]
st.metric(label=f"{coin} Price", value=selected['lastPrice'].values[0])
st.metric(label="24h Change (%)", value=f"{selected['priceChangePercent'].values[0]:.2f}%")

with st.expander("📋 View All USDT Pairs"):
    st.dataframe(df.reset_index(drop=True))

