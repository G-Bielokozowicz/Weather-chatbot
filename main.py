import tkinter as tk
from tkinter import scrolledtext

import spacy
import requests

nlp = spacy.load("en_core_web_md")
api_key = "019947b686adde825c5c6104b3e13d7e"


def get_weather(city_name):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city_name, api_key)
    response = requests.get(api_url)
    response_dict = response.json()
    weather = response_dict["weather"][0]["description"]
    if response.status_code == 200:
        return weather
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None


weather = nlp("Weather Conditions in a city")


def chatbot(statement):
    statement_doc = nlp(statement)
    min_similarity = 0.75

    if not statement_doc.has_vector:
        # Handle the case where the Doc object has no vectors
        return "Sorry, I couldn't understand your statement."

    if weather.has_vector and statement_doc.has_vector and weather.similarity(statement_doc) >= min_similarity:
        for ent in statement_doc.ents:
            if ent.label_ == "GPE":  # GeoPolitical Entity
                city = ent.text
                city_weather = get_weather(city)
                if city_weather is not None:
                    return "In " + city + ", the current weather is: " + city_weather
                else:
                    return "Something went wrong."
        else:
            return "You need to tell me a city to check."
    else:
        return "Sorry, I don't understand that. Please rephrase your statement."


def on_send():
    user_input = user_entry.get()
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    response = chatbot(user_input)
    chat_history.insert(tk.END, "Bot: " + response + "\n")
    user_entry.delete(0, tk.END)


root = tk.Tk()
root.title("Weather Chatbot")

chat_history = scrolledtext.ScrolledText(root, width=50, height=20, wrap=tk.WORD)
chat_history.pack(padx=10, pady=10)

user_entry = tk.Entry(root, width=50)
user_entry.pack(padx=10, pady=10)

send_button = tk.Button(root, text="Send", command=on_send)
send_button.pack(padx=10, pady=10)

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(padx=10, pady=10)

root.mainloop()
