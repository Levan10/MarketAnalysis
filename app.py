import streamlit as st
from analysis import fetch_stock_data, add_indicators
from strategy import generate_signal
from news import fetch_news
from search import search_ticker
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Analysis App", layout="wide")
st.title("📊 Stock Analyzer with Recent News")

def plot_stock(df):
    fig = go.Figure()

    # Plot Close for full range
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Close'],
        mode='lines', name='Close Price'
    ))

    # Plot SMA20 where available (NaNs will be ignored)
    fig.add_trace(go.Scatter(
        x=df.index, y=df['sma_20'],
        mode='lines', name='SMA 20',
        connectgaps=False
    ))

    # Plot SMA50 where available
    fig.add_trace(go.Scatter(
        x=df.index, y=df['sma_50'],
        mode='lines', name='SMA 50',
        connectgaps=False
    ))

    fig.update_layout(
        title='Stock Price with SMA20 and SMA50',
        xaxis_title='Date',
        yaxis_title='Price',
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)


company_query = st.text_input("🔎 Search for a Company (e.g., Apple, Tesla)", value="Apple")

ticker_options = search_ticker(company_query) if company_query else []

if ticker_options:
    selected = st.selectbox("Select a Ticker", ticker_options, format_func=lambda x: f"{x['symbol']} - {x['name']}")
    ticker = selected["symbol"]

    with st.spinner(f"Analyzing {ticker}..."):
        df = fetch_stock_data(ticker)
        df = add_indicators(df)
        signal = generate_signal(df)
        news = fetch_news(selected["name"])

    st.subheader(f"Signal: {signal}")
    plot_stock(df)  # Use full df including NaNs for proper zooming
    st.dataframe(df.tail(5))

    st.subheader("Latest News")
    if news:
        for title, url in news:
            st.markdown(f"- [{title}]({url})")
    else:
        st.write("No news found.")
else:
    st.warning("No matching tickers found.")
