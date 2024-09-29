import os
import openai
import yfinance as yf
from datetime import datetime, timedelta
import pytz

class StockData:
    # return the most recent headlines for the given stock
    def retrieveNewsHeading(self, symbol):
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
            print("Article:", article)  # Debugging line
            
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
    
