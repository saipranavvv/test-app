import streamlit as st
import requests
import json

from dataclasses import dataclass

def chat_with_gemma(prompt):
    """Sends a prompt to the locally running Gemma model and returns the response."""

    url = "http://localhost:11434/api/generate"  # Ollama's default API endpoint
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "gemma2:2b",  # Replace with the exact name if different (e.g., "gemma2:2b")
        "prompt": prompt,
        "stream": False # Important: Gemma returns a stream by default. Set to false to get a single response.
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        json_response = response.json()
        # Extract the generated text.  The structure can vary, so inspect the JSON!
        # Example 1 (common):
        # generated_text = json_response['response']
        # Example 2 (if it's nested):
        generated_text = ""
        for part in json_response['response']:
            generated_text += part

        return generated_text

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"Error parsing Ollama response: {e}.  Raw Response: {json_response}")
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON response: {e}. Response text: {response.text}")
        return None






@dataclass
class Message:
    actor: str
    payload: str

USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"
if MESSAGES not in st.session_state:
    st.session_state[MESSAGES] = [Message(actor=ASSISTANT, payload="Hi Pranav ! How can I help you?")]

msg: Message
for msg in st.session_state[MESSAGES]:
    st.chat_message(msg.actor).write(msg.payload)

prompt: str = st.chat_input("Enter a prompt here")

if prompt:
    st.session_state[MESSAGES].append(Message(actor=USER, payload=prompt))
    st.chat_message(USER).write(prompt)
    response: str = chat_with_gemma(prompt)
    st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response))
    st.chat_message(ASSISTANT).write(response) 
