import json
import pyttsx3
import pytchat
import time
import argparse
from pydub import AudioSegment
from pydub.playback import play
from pathlib import Path
import os
from openai import OpenAI

def PyTTSInitialization(): # Initialize pyttsx3
    global engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', voices[1].id)

def VariableInitialization(): # Initialize all the variables and read the JSON file for API keys and other configurations
    global video_id
    global tts_type
    global OAI

    try:
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("Unable to open JSON file.")
        exit()

    class OAI: 
        key = data["apikeys"][0]["OAI_key"]

    tts_list = ["pyttsx3", "openai"]

    parser = argparse.ArgumentParser() # Command line arguments
    parser.add_argument("-id", "--video_id", type=str, help="Video ID")
    parser.add_argument("-tts", "--tts_type", type=str, help="TTS Type", choices=tts_list, default="pyttsx3")
    args = parser.parse_args()
    
    video_id = args.video_id
    tts_type = args.tts_type

    if tts_type == "pyttsx3":
        PyTTSInitialization()

def WhatTTS(message): # Check which TTS to use 
    if tts_type == "openai":
        OAI_TTS(message)
    
    elif tts_type == "pyttsx3":
        Py_TTS(message)

def Py_TTS(message): # pyttsx3 TTS function
    try:
        engine.say(message)
        engine.runAndWait()
    except Exception as e:
        print("PyTTS error: " + str(e))

def OAI_TTS(message): # OpenAI TTS function
    global client
    client = OpenAI(api_key=OAI.key)
    speech_file_path = Path(__file__).parent / "speech.mp3"

    try:
        response = client.audio.speech.create(
            model = "tts-1",
            voice = "nova",
            input = message,
        )

        response.stream_to_file(speech_file_path)

        if speech_file_path.exists() and os.path.getsize(speech_file_path) > 0:
            sound = AudioSegment.from_mp3(speech_file_path)
            print("\nSaying... ")
            play(sound)
        else:
            print("Error in OAI_TTS: No speech file found.")

    except Exception as e:
        print("Error in OAI_TTS: " + str(e))

def read_chat(): # Read the chat
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

def text_generator(message): # Generate response
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
    
def main(): # Main function
    VariableInitialization()
    print("\nReading Chat!\n\n")
    read_chat()
    print("\nProgram terminated.\n")

if __name__ == "__main__": 
    main()
