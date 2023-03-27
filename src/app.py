import os
import requests

import panel as pn
from dotenv import load_dotenv

# CSS To make the box scrollable
css = """
.text-area-scrollbar textarea {
    overflow-y: scroll !important;
}
"""


pn.extension(raw_css=[css])

load_dotenv()

# Replace with your OpenAI API key
api_key = os.environ["OPENAI_API_KEY"]

# Set up the ChatGPT API endpoint
url = "https://api.openai.com/v1/engines/text-davinci-002/completions"

# Function to send a request to the ChatGPT API
def send_request(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    data = {
        "prompt": prompt,
        "max_tokens": 50,
        "n": 1,
        "stop": None,
        "temperature": 0.8,
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code == 200:
        return response_json["choices"][0]["text"].strip()
    else:
        return "Error: Unable to process your request."

# Function to handle user input and display response from ChatGPT
def send_prompt(event=None):
    prompt = user_input.value
    response = send_request(prompt)
    response_area.value = f"> {prompt}\n{response}"

    conversation_history.value += f"USER: {user_input.value}\nChatGPT: {response}\n{'-' * 10}"


    user_input.value = ""

# Panel UI components
title = pn.pane.Markdown("# ChatGPT Panel Application")
title = pn.pane.Markdown("### Conversation History")
user_input = pn.widgets.TextInput(name="Type message here...")
send_button = pn.widgets.Button(name="Send", button_type="primary")

response_area = pn.widgets.TextAreaInput(value="", disabled=True, height=500, css_classes=["text-area-scrollbar"])
conversation_history = pn.widgets.TextAreaInput(value="", disabled=True, height=300, css_classes=["text-area-scrollbar"])

send_button.on_click(send_prompt)

# Arrange components and create the panel application
layout = pn.Column(
    title,
    pn.Row(response_area, conversation_history),
    pn.Row(user_input, send_button, width=600),
)

layout.servable()
