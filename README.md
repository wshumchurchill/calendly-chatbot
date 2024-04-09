# calendly-chatbot
function calling calendly api using langchain

# Instructions for Development:
Clone repository and navigate to root directory. Then, you want to create the conda environment using the environment.yml file by doing

- conda env create --file environment.yml
- conda activate function-calling

Before you start up the flask server, first navigate to chatbot.py. You will need to input your Calendly API Key, your OpenAI API key, as well as your Calendly user URI.
You can get your calendly user URI by running the following:
curl --request GET \
--url https://api.calendly.com/users/me \
--header 'authorization: Bearer {access_token}'

After inputting all your secret keys to the chatbot.py file, you can now start the flask server, which will handle all requests. Might take a second to load the first time.
The web interface can be accessed via http://127.0.0.1:8080

Enjoy :)

