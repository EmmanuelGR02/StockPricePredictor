import os
import openai
import yfinance as yf
from datetime import datetime, timedelta
import pytz
from StockData import StockData  

class StockPricePredictor:
    def run_test(self):
        # Initialize the StockData class
        stock_data = StockData()  

        # Set the ticker symbol for testing
        ticker_symbol = "AMZN"

        # Retrieve recent news headlines
        headlines = stock_data.retrieveNewsHeading(ticker_symbol)

        # Check if any headlines were retrieved
        if not headlines:
            print(f"No recent headlines found for {ticker_symbol}.")
            return

        # Print retrieved headlines for debugging
        print(f"Recent Headlines for {ticker_symbol}:")
        for title, link in headlines.items():
            print(f"- {title}: {link}")

        # Use OpenAI API to get the news sentiment
        news_sentiment = stock_data.getNews(headlines, ticker_symbol)

        # Print the results
        print(f"Sentiment results for {ticker_symbol}: {news_sentiment}")

# Running the test
if __name__ == "__main__":
    test_stock_data = StockPricePredictor()  
    test_stock_data.run_test()  
