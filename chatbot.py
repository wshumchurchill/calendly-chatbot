# Function calling coding challenge
## Overview
# Your task is to create an interactive chatbot using OpenAI's function
# calling capabilities.
# This chatbot will allow users to interact with their Calendly account
# directly through the chat interface.
# The chatbot should be able to list scheduled events and cancel events
# using the Calendly API. 

## Requirements
# Build a simple chatbot that can interact with the REST API. The chatbot
# may be a web server, and the user may interact
# with it through REST API. It will be a bonus if you can make the chatbot
# interactive through a web interface.
# Use OpenAI's function calling feature to integrate external APIs with
# your chatbot.
# This will involve crafting requests to the Calendly API and processing
# responses within the chatbot's logic.

# Specifically, you'll need to implement the following functionality:
# - Once the user says something like "show me the scheduled events",
# retrieve a list of the user's scheduled events from Calendly.

# - When the user says something like "cancel my event at 3pm today", find
# the event and cancel it from Calendly.



import os
from openai import OpenAI
from langchain.agents.format_scratchpad.openai_tools import (format_to_openai_tool_messages)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor
import requests
from datetime import datetime, timezone



os.environ["OPENAI_API_KEY"] = '' # need to input openai api key
client = OpenAI()

calendly_api_key = '' # need to have calendly api key here
headers = {
    'Authorization': f'Bearer {calendly_api_key}',
    'Content-Type': 'application/json'
}

@tool
def List_Events(min_start_time=None, status=None) -> str:
    """List all of the user's scheduled events from Calendly based on the time, which should be an ISO 8601 date-time string"""
    params = {
        'user': '', # need to input user uri here
    }
    # simple checks
    if min_start_time:
        params['min_start_time'] = min_start_time
    if status:
        params['status'] = status
    
    event_url = 'https://api.calendly.com/scheduled_events'
    
    response = requests.request("GET", event_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()

    else:
        return f'Error: {response.status_code}, Details: {response.text}'

@tool
def Cancel_Event(uuid: str) -> str:
    "Cancel a Calendly event with a specified uuid"

    url = f"https://api.calendly.com/scheduled_events/{uuid}/cancellation"

    payload = {"reason": "user cancelled via chatbot"}

    response = requests.request("POST", url, json=payload, headers=headers)

    print("this is the response", response.text)
    if response.status_code == 201:
        return response.json()
    else:
        return f'Error: {response.status_code}, Details: {response.text}'

today_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
curr_tz = datetime.now().astimezone().tzinfo
print("this is the current date and time: ", today_date)
print("this is the current timezone: ", curr_tz)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", f"You are an assistant that calls the Calendly API to do one of two things: retrieve the scheduled events or cancel an event from Calendly.\
To cancel an event, you must first transform the date provided by the user, which is in {curr_tz} timezone, into an ISO 8601 date-time string in UTC timezone. \
After adjusting the user-specified time into UTC timezone as an ISO 8601 date-time string, use the ISO 8601 date-time string to find the corresponding event, \
and determine the event's unique id, and then subsequently cancel that event. Recall that today's date and time in the user's timezone is {today_date}."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

tools = [List_Events, Cancel_Event]

def main(input:str):
    llm = ChatOpenAI(temperature=0, model="gpt-4-0125-preview")
    llm_with_tools = llm.bind_tools(tools)
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    result = agent_executor.invoke(
        {
            "input": input,
        }
    )
    return result["output"]
    

if __name__ == "__main__":
    main("Show me the scheduled events") # this is just for testing purposes on the backend
    



