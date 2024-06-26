# calendly-chatbot
This project is for using OpenAI's function calling feature via Langchain to craft requests to the Calendly API. Note that the chatbot currently only supports two functions: (1) retrieving list of user's scheduled events, and (2) cancels a user's event based on a specified time.


# Instructions for Development:
Clone repository and navigate to root directory. Then, you want to create the conda environment using the environment.yml file by doing

- conda env create --file environment.yml
- conda activate function-calling

Before you start up the flask server, first navigate to chatbot.py. You will need to input your Calendly API Key, your OpenAI API key, as well as your Calendly user URI.
You can get your calendly user URI by running the following:

curl --request GET \
--url https://api.calendly.com/users/me \
--header 'authorization: Bearer {access_token}'

Note – if you don't have a calendly API key or account, you will need to create one by following these instructions here: https://developer.calendly.com/how-to-authenticate-with-personal-access-tokens

After inputting all your secret keys to the chatbot.py file, you can now start the flask server, which will handle all requests. Might take a second to load the first time.
The web interface can be accessed via http://127.0.0.1:8080

Enjoy :)

