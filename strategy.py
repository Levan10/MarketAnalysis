
def generate_signal(df):
    latest = df.iloc[-1]

    if latest["sma_20"] > latest["sma_50"] and latest["rsi"] < 70:
        return "Buy"
    elif latest["sma_20"] < latest["sma_50"] and latest["rsi"] > 30:
        return "Sell"
    elif latest["rsi"] > 70:
        return "Strong Sell"
    elif latest["rsi"] < 30:
        return "Strong Buy"
    else:
        return "Hold"



def morning_star_rating(df):
    """
    Calculate a composite 1-5 star rating based on SMA crossover, RSI, and volume trend.

    Scoring:
    - SMA20 > SMA50: +2 points (bullish)
    - RSI < 30: +2 points (oversold, potential buy)
    - RSI between 30 and 70: +1 point (neutral)
    - Today's volume > 20-day average volume: +1 point

    Returns a string of stars, e.g. "⭐⭐⭐☆☆"
    """
    latest = df.iloc[-1]

    score = 0

    # SMA crossover check
    if latest["sma_20"] > latest["sma_50"]:
        score += 2

    # RSI scoring
    rsi = latest["rsi"]
    if rsi < 30:
        score += 2
    elif 30 <= rsi <= 70:
        score += 1

    # Volume trend
    avg_volume = df["Volume"].rolling(window=20).mean().iloc[-1]
    if latest["Volume"] > avg_volume:
        score += 1

    # Limit score to max 5
    score = min(score, 5)

    stars = "⭐" * score + "☆" * (5 - score)
    return stars

