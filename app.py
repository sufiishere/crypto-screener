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
    df = pd.DataFrame(data)
    df = df[df['symbol'].str.endswith('USDT')]
    df['priceChangePercent'] = df['priceChangePercent'].astype(float)
    df['lastPrice'] = df['lastPrice'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df[['symbol', 'lastPrice', 'priceChangePercent', 'volume']].sort_values(by='volume', ascending=False)

df = load_binance_data()

st.sidebar.header("🔍 Filters")
min_volume = st.sidebar.slider("Minimum Volume", 0.0, 1000000000.0, 10000000.0, step=1000000.0)
min_change = st.sidebar.slider("Minimum % Change (24h)", -50.0, 50.0, -5.0, step=0.5)
max_change = st.sidebar.slider("Maximum % Change (24h)", -50.0, 50.0, 50.0, step=0.5)
search = st.sidebar.text_input("Search Pair (e.g., BTC)")

filtered_df = df[
    (df['volume'] >= min_volume) &
    (df['priceChangePercent'] >= min_change) &
    (df['priceChangePercent'] <= max_change)
]

if search:
    filtered_df = filtered_df[filtered_df['symbol'].str.contains(search.upper())]

st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
