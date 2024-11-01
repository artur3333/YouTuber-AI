import json
import pyttsx3
import pytchat
import time
import argparse
from openai import OpenAI

def PyTTSInitialization():
    global engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', voices[1].id)

def VariableInitialization():
    global OAI_key
    global video_id
    global tts_type
    global OAI

    try:
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("Unable to open JSON file.")
        exit()

    tts_list = ["pyttsx3"]

    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--video_id", type=str, help="Video ID")
    parser.add_argument("-tts", "--tts_type", type=str, help="TTS Type", choices=tts_list, default="pyttsx3")
    args = parser.parse_args()
    
    video_id = args.video_id
    tts_type = args.tts_type

    if tts_type == "pyttsx3":
        PyTTSInitialization()

    class OAI:
        key = data["apikeys"][0]["OAI_key"]

def WhatTTS(message):
    if tts_type == "pyttsx3":
        PyTTS(message)

def PyTTS(message):
    try:
        engine.say(message)
        engine.runAndWait()
    except Exception as e:
        print("PyTTS error: " + str(e))

def read_chat():
    chat = pytchat.create(video_id=video_id)

    try:
        while chat.is_alive():
            for c in chat.get().sync_items():
                try:
                    print("\n" + c.datetime + " " + c.author.name + " > " + c.message + "\n")
                    message = c.message

                    response = text_generator(message)
                    print(response)

                    WhatTTS(response)

                    time.sleep(1)

                except Exception as e:
                    print("Error in read chat: " + str(e))
                    break
    except KeyboardInterrupt:
        print("\nInterrupted by user. Program terminated.\n")

def text_generator(message):
    client = OpenAI(api_key=OAI.key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "max_tokens": 16,
                "content": "This is how a female streamer responded in a conversation. She would respond in a friendly manner. She would talk about the message and would elaborate on it as well as share some of her experiences if possible. She also can use only 16 tokens, so she can't speak much per message."
            },
            {
                "role": "user",
                "content": "\n----------\n" + message + "\n----------\n"
            }
        ]
    )
    
    try:
        message_text = completion.choices[0].message.content
        return message_text
    except Exception as e:
        print("Error in text generator: " + str(e))
        return "Error in text generator"
    
def main():
    VariableInitialization()
    print("\nReading Chat!\n\n")
    read_chat()
    print("\nProgram terminated.\n")

if __name__ == "__main__":
    main()
