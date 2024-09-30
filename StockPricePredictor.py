import os
import openai
import yfinance as yf
from datetime import datetime, timedelta
import pytz
from StockData import StockData  

class StockPricePredictor:
    def run_test(self):
        # Set the ticker symbol for testing
        ticker_symbol = "V"

        # Initialize the StockData class
        stock_data = StockData()  
        data, history = stock_data.getStockData(ticker_symbol)

        # Retrieve recent news headlines
        headlines = stock_data.retrieveNewsHeadlines(ticker_symbol)

        # Check if any headlines were retrieved
        if not headlines:
            print(f"No recent headlines found for {ticker_symbol}.")
            return

        # Print retrieved headlines for debugging
        print(f"Recent Headlines for {ticker_symbol}:")
        for title, link in headlines.items():
            print(f"- {title}: {link}")

        # Use OpenAI API to get the news sentiment
        news_sentiment = stock_data.getSentimentValues(headlines, ticker_symbol)

        # Print the results
        print(f"Sentiment results for {ticker_symbol}: {news_sentiment}")

        for key, value in data.items():
            print(f"{key}: {value}")

        stock_data.plot_stock_data(ticker_symbol, history)



# Running the test
if __name__ == "__main__":
    test_stock_data = StockPricePredictor()  
    test_stock_data.run_test()  