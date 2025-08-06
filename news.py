import requests

API_KEY = "8c50f187815c495fa911f27f32575098"  # Replace this!

def fetch_news(company_name):
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={company_name}&"
        "sortBy=publishedAt&"
        "language=en&"
        f"apiKey={API_KEY}"
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        articles = response.json().get("articles", [])

        return [(a["title"], a["url"]) for a in articles[:5]]
    except Exception as e:
        print("NewsAPI error:", e)
        return []
