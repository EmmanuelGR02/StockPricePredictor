import os
import openai

class StockData:

    # use open AI API to ask it if the given news are good or bad (0,1)
    def getNews(self, news, symbol):
        # get key from env file
        openai.api_key = os.getenv("OPEN_AI_KEY")
        response = ""
        value = 0

        # handle errors
        if openai.api_key is None:
            print("API key is not set.")
        else:
            openai.api_key = openai.api_key

            try:
                # ask
                # the response should only be (good or bad)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Tell me if the following news header is (good or bad) for the comapny's stock, your answer should only be (good or bad): The pre orders for iphone 16 meet exeed expectations"}]
                )
                response = response.choices[0].message['content']
            except Exception as e:
                print(f"Error: {e}")

        # Set response to 1 if its good or 0 if its bad
        if (response.upper() == "GOOD"):
            value = 1
        elif (response.upper() == "BAD"):
            value = 0
        else:
            value = 0
            print("Chat GPT did not give a valid response!!")

        return value
    
