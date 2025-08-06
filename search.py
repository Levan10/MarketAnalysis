import requests

#Allows user to search company name as ticker
def search_ticker(company_name):
    url = f"https://query1.finance.yahoo.com/v1/finance/search?q={company_name}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)

    try:
        results = res.json().get("quotes", [])
        return [
            {"symbol": r["symbol"], "name": r.get("shortname", r.get("longname", r["symbol"]))}
            for r in results if "symbol" in r
        ]
    except Exception as e:
        print("Error decoding JSON:", e)
        print("Response content:", res.text)
        return []
