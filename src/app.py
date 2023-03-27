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
def chatgpt_request(prompt):
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
def chatgpt_interaction(event):
    prompt = user_input.value
    response = chatgpt_request(prompt)
    response_area.value = f"> {prompt}\n{response}"
    user_input.value = ""

# Panel UI components
title = pn.pane.Markdown("# ChatGPT Panel Application")
user_input = pn.widgets.TextInput(name="Your message")
send_button = pn.widgets.Button(name="Send", button_type="primary")
send_button.on_click(chatgpt_interaction)
response_area = pn.widgets.TextAreaInput(value="", disabled=True, height=500, css_classes=["text-area-scrollbar"])

# Arrange components and create the panel application
layout = pn.Column(
    title,
    response_area,
    pn.Row(user_input, send_button, width=600),
)

layout.servable()
