# Import required libraries
import streamlit as st
import plotly.graph_objects as go
from strategy import generate_signal, morning_star_rating  # import morning_star_rating


# Import custom modules for stock data, indicators, signal generation, news, and ticker search
from analysis import fetch_stock_data, add_indicators
from news import fetch_news
from search import search_ticker

# Set page title and layout in Streamlit
st.set_page_config(page_title="Stock Analysis App", layout="wide")
st.title("📊 Stock Analyzer with Recent News")


    #interactive chart with:
    #Close price
    #SMA 20 (20-day Simple Moving Average)
    #SMA 50 (50-day Simple Moving Average)"""

# ---------- Plotting Function using Plotly ----------
def plot_stock(df):
    # Get the most recent close price
    current_price = df["Close"].iloc[-1]
    formatted_price = f"${current_price:,.2f}"

    # Show it above the chart
    st.subheader(f"Current Price: {formatted_price}")

    fig = go.Figure()

    # Plot the stock's closing price
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Close'],
        mode='lines', name='Close Price'
    ))

    # Plot SMA 20 (may contain NaNs for first 20 rows)
    fig.add_trace(go.Scatter(
        x=df.index, y=df['sma_20'],
        mode='lines', name='SMA 20',
        connectgaps=False  # prevents connecting over NaNs
    ))

    # Plot SMA 50
    fig.add_trace(go.Scatter(
        x=df.index, y=df['sma_50'],
        mode='lines', name='SMA 50',
        connectgaps=False
    ))

    # Set chart layout and titles
    fig.update_layout(
        title='📈 Stock Chart',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        hovermode='x unified'  # shows all values when hovering
    )

    # Display chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# ---------- User Input: Search for a company ----------
company_query = st.text_input(
    "🔎 Search for a Company (e.g., Apple, Tesla)", value="Apple"
)

# Get matching ticker symbols from the search query
ticker_options = search_ticker(company_query) if company_query else []

# If there are matching results, show dropdown to select one
if ticker_options:
    selected = st.selectbox(
        "Select a Ticker",
        ticker_options,
        format_func=lambda x: f"{x['symbol']} - {x['name']}"
    )

    ticker = selected["symbol"]

    # Dropdown for time range selection
    period_options = {
        "1 Day": "1d",
        "1 Month": "1mo",
        "3 Months": "3mo",
        "1 Year": "1y",
        "5 Years": "5y",
        "10 Years": "10y"
    }
    selected_period_label = st.selectbox("Select Time Range", list(period_options.keys()), index=3)
    selected_period = period_options[selected_period_label]

    # Fetch stock data with selected period
    df = fetch_stock_data(ticker, period=selected_period)

    # ---------- Fetch and Analyze the Stock ----------
    with st.spinner(f"Analyzing {ticker}..."):  # Get stock data from Yahoo
        df = add_indicators(df)             # Add SMA and RSI indicators
        signal = generate_signal(df)        # Generate buy/sell/hold signal
        rating = morning_star_rating(df)    # Generate Morning Star rating
        news = fetch_news(selected["name"]) # Fetch latest news for the company

    # ---------- Display Results ----------
    st.subheader(f"Signal: **{signal}**")
    st.subheader(f"🌟 Morning Star Rating: {rating}")   # Show Morning Star rating here
    plot_stock(df)  # Show interactive chart
    st.dataframe(df.tail(5))  # Show last 5 rows of data

    # ---------- Display News Headlines ----------
    st.subheader("Latest News")
    if news:
        for title, url in news:
            st.markdown(f"- [{title}]({url})")
    else:
        st.write("No news found.")
else:
    # If no matching tickers found
    st.warning("⚠️ No matching tickers found. Try a different company name.")
