import pandas as pd
import requests
import time


DF1 = pd.read_csv("nasdaq_df1.csv")


Tickers = DF1["Ticker"][:5]  

url = "https://alpha-vantage.p.rapidapi.com/query"
headers = {
    "X-RapidAPI-Key": "ef5a3c33d3msh7776c931f35e89cp18e5ffjsnf36112350622",
    "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}

results = []

for ticker in Tickers:
    try:
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": ticker,
            "outputsize": "compact",
            "datatype": "json"
        }

        response = requests.get(url, headers=headers, params=params)
        print(f" Response {response.status_code} for {ticker}")

        data = response.json()

        if "Time Series (Daily)" in data:
            latest_date = list(data["Time Series (Daily)"].keys())[0]
            daily = data["Time Series (Daily)"][latest_date]

            results.append({
                "Ticker": ticker,
                "Date": latest_date,
                "Open": float(daily["1. open"]),
                "High": float(daily["2. high"]),
                "Low": float(daily["3. low"]),
                "Close": float(daily["4. close"]),
                "Volume": int(daily["6. volume"])
            })

            print(f" Data collected for {ticker}")
        else:
            print(f" No data for {ticker}")
    except Exception as e:
        print(f" Error with {ticker}: {e}")

    time.sleep(12)

if results:
    DF2 = pd.DataFrame(results)
    DF2.to_csv("nasdaq_df2.csv", index=False)
    print(" File saved as nasdaq_df2.csv")
else:
    print(" No data to save.")




