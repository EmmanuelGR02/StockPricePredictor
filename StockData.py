import os
import openai
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import pandas as panda
import matplotlib.pyplot as plt
import numpy as np

class StockData:
    # return the most recent headlines for the given stock
    def retrieveNewsHeadlines(self, symbol):
        # Get the news for the ticker symbol stock
        ticker = yf.Ticker(symbol)
        news = ticker.news

        # Get current time
        currentTime = datetime.now(pytz.UTC)
        # Define threshold for 48 hours ago
        timeThreshold = currentTime - timedelta(hours=48)

        # Define dictionary where all of the headlines will go
        headlinesDict = {}
        for article in news:
            # Print the entire article for debugging
            print("Article:", article) 
            
            # Safely get the providerPublishTime
            publish_time_unix = article.get('providerPublishTime')
            if publish_time_unix is not None:
                # Convert Unix time to datetime
                pub_date = datetime.fromtimestamp(publish_time_unix, tz=pytz.UTC)
                if pub_date >= timeThreshold:
                    headlinesDict[article['title']] = article['link']
            else:
                print(f"No providerPublishTime found for article '{article.get('title', 'Unknown')}'")

        return headlinesDict
        

    # use open AI API to ask it if the given news are good or bad (0,1)
    def getNews(self, headlines, symbol):
        # get key from env file
        openai.api_key = os.getenv("OPEN_AI_KEY")
        valuesList = []
        onesCount = 0
        zerosCount = 0
        invalidCount = 0

        # handle errors
        if openai.api_key is None:
            print("API key is not set.")
        else:
            openai.api_key = openai.api_key

            try:
                # ask chap gpt about all of the headlines from the healines dictionary passed
                # the response should only be (good or bad)
                for headline in headlines:
                    # set value back to -1
                    value = -1
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": "Tell me if the following news header is (good or bad) for " + symbol + "'s stock, your answer should only be (good or bad): " + headline}]
                    )
                    response = response.choices[0].message['content']
                    # print response for debugging
                    print(response)

                    # Set response to 1 if its good or 0 if its bad
                    if (response.upper() == "GOOD"):
                        value = 1
                    elif (response.upper() == "BAD"):
                        value = 0
                    else:
                        value = -1
                        print("\nChat GPT did not give a valid response for the following headline: " + headline)
                    
                    # add value to list
                    valuesList.append(value)

            except Exception as e:
                print(f"Error: {e}")

            # print value list for debugging
            print(valuesList)

            # get the total count of 0s, 1s and -1s
            for values in valuesList:
                if values == 0:
                    zerosCount += 1
                elif values == 1:
                    onesCount += 1
                else:
                    invalidCount += 1

            # display counts for debugging
            print("\n0s count = " + str(zerosCount))
            print("1s count = " + str(onesCount) )
            print("-1s count = " + str(invalidCount) )

        return valuesList
    
    def getStockData(self, symbol):
        # get data about the stock from yfinance
        stock = yf.Ticker(symbol)
        history = stock.history(period = "1y")

        # calculate MAs
        history["5MA"] = history["Close"].rolling(window = 5).mean()
        history["10MA"] = history["Close"].rolling(window = 10).mean()
        history["25MA"] = history["Close"].rolling(window = 25).mean()
        history["50MA"] = history["Close"].rolling(window = 50).mean()
        history["100MA"] = history["Close"].rolling(window = 100).mean()

        # Get price metrics
        currentPrice = history["Close"][-1]
        openPrice = history["Open"][-1]
        averagePrice = (history["High"] + history["Low"]) / 2

        priceChange = currentPrice - openPrice
        history["LongReturn"] = (history["Close"] / history["Close"].shift(1)).apply(lambda x: np.log(x))
        volatility = history["LongReturn"].std()

        averageVolume = history["Volume"].rolling(window = 10).mean()
        currentVolume = history["Volume"][-1]
        volumeChange = currentVolume - averageVolume[-1]

        PEratio = stock.info.get("trailingPE")
        eps = stock.info.get("trailingEps")

        # More data? 

        # dictinonary to store results
        stockData = {
            "Current Price" : currentPrice,
            "open Price" : openPrice,
            "Average Price" : averagePrice,
            "Price Change" : priceChange,
            "5MA" : history["5MA"][-1],
            "10MA" : history["10MA"][-1],
            "25MA" : history["25MA"][-1],
            "50MA" : history["50MA"][-1],
            "100MA" : history["100MA"][-1],
            "Volatility" : volatility,
            "Volume Change" : volumeChange,
            "PE Ratio" : PEratio,
            "EPS" : eps
        }
        
        return stockData, history
    
    # visualize stock data
    def plot_stock_data(self, symbol, history):

        # Plot the stock price and moving averages
        plt.figure(figsize=(10,6))
        plt.plot(history['Close'], label='Close Price', color='blue')
        plt.plot(history['5MA'], label='5-Day MA', color='red')
        plt.plot(history['10MA'], label='10-Day MA', color='green')
        plt.plot(history['25MA'], label='25-Day MA', color='purple')
        plt.plot(history['50MA'], label='50-Day MA', color='orange')
        plt.plot(history['100MA'], label='100-Day MA', color='brown')

        plt.title(f'{symbol} Price and Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
    
    