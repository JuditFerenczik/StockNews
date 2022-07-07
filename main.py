import os
import requests
import datetime as dt
from twilio.rest import Client
from config import API_KEY_STOCK, APU_KEY_NEWS,account_sid,auth_token, FROM_NUMBER,TO_NUMBER
from twilio.http.http_client import TwilioHttpClient
# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
yesterday = str(dt.datetime.now().date() - dt.timedelta(days=1))
print(str(yesterday))
day_before_yesterday = str(dt.datetime.now().date() - dt.timedelta(days=10))
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

print(API_KEY_STOCK)
parameters_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_STOCK
}
r = requests.get("https://www.alphavantage.co/query", params=parameters_stock)
r.raise_for_status()
data = r.json()
print(data)
data = data['Time Series (Daily)']
stock_difference = abs((float(data[yesterday]['4. close'])-float(data[day_before_yesterday]['4. close']))
                       / float(data[day_before_yesterday]['4. close']))
stock_d = (float(data[yesterday]['4. close'])-float(data[day_before_yesterday]['4. close']))/float(data[day_before_yesterday]['4. close'])
arrow = "🔺" if stock_d > 0 else "🔻"
print(arrow)
print(stock_difference)

# first = True
# for item in data.keys():
#     if not first:
#         if abs((float(data[item]['4. close'])-previousItem)/previousItem) >= 0.05:
#             print(f"{item} -> Get news")
#     previousItem = float(data[item]['4. close'])
#     first = False
print(data)


url = "https://newsapi.org/v2/everything"
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
parameters_news={
    "q": COMPANY_NAME,
    "apikey":APU_KEY_NEWS,
    "sortBy" :"popularity"
}
if stock_difference >= 0.05:
    print("Get news!!")
    r2 = requests.get(url, params=parameters_news)
    r2.raise_for_status()
    data2 = r2.json()

    for i in range(0, 3):
        print(data2["articles"][i]["content"])
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"\n\n TESLA {arrow}{stock_difference*100:.1f}% \n️ Headline: {data2['articles'][i]['title']} \n Brief: {data2['articles'][i]['description']}",
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )
        print(message.status)

