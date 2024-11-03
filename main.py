import json
import pyttsx3
import pytchat
import time
import argparse
import winsound
from pydub import AudioSegment
from pathlib import Path
import os
import sys
from twitchio.ext import commands
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
    global platform
    global OAI_key
    global token, nickname, channel

    try:
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
        OAI_key = data["apikeys"][0]["OAI_key"]
        token = data["twitch"][0]["token"]
        nickname = data["twitch"][0]["nickname"]
        channel = data["twitch"][0]["channel"]

    except FileNotFoundError:
        print("Unable to open JSON file.")
        exit()   

    tts_list = ["pyttsx3", "openai"]
    platform_list = ["youtube", "twitch"]

    parser = argparse.ArgumentParser() # Command line arguments
    parser.add_argument("-id", "--video_id", type=str, help="Video ID")
    parser.add_argument("-tts", "--tts_type", type=str, help="TTS Type", choices=tts_list, default="pyttsx3")
    parser.add_argument("-p", "--platform", type=str, help="Platform", choices=platform_list)
    args = parser.parse_args()
    
    video_id = args.video_id
    tts_type = args.tts_type
    platform = args.platform

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
    client = OpenAI(api_key=OAI_key)
    speech_file_path = Path(__file__).parent / "speech.mp3"
    wav_file_path = Path(__file__).parent / "speech.wav"

    try:
        response = client.audio.speech.create(
            model = "tts-1",
            voice = "nova",
            input = message
        )

        with open(speech_file_path, "wb") as file:
            for chunk in response.iter_bytes():
                file.write(chunk)

        # Convert mp3 to wav
        if speech_file_path.exists() and os.path.getsize(speech_file_path) > 0:
            audio = AudioSegment.from_mp3(speech_file_path)
            audio.export(wav_file_path, format="wav")

            # Play the audio
            winsound.PlaySound(wav_file_path, winsound.SND_FILENAME)

        else:
            print("Error in OAI_TTS: No speech file found or file is empty.")

    except Exception as e:
        print("Error in OAI_TTS: " + str(e))


# Read the YouTube chat
def YT_read_chat():
    chat = pytchat.create(video_id=video_id)

    while chat.is_alive():
        try:
            for c in chat.get().sync_items():
                try:
                    # Print the chat message
                    print(f"\n{c.datetime} {c.author.name} > {c.message}\n")
                    message = c.message

                    # Generate response
                    response = text_generator(message)
                    print(f"Response: {response}")

                    # pass the response to TTS controller
                    WhatTTS(response)

                    time.sleep(1)
                
                except Exception as e:
                    print("Error in read_chat: " + str(e))
                    continue
        
        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Exiting...\n")
            sys.exit(0)


# Read the Twitch chat
class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=token, prefix="!", initial_channels=[channel])

    async def event_ready(self):
        print(f"Bot is ready! {self.nick}")
    
    async def event_message(self, message):
        username = message.author.name
        content = message.content
        datetime = message.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        print (f"\n{datetime} {username} > {content}\n")

        response = text_generator(content)
        print(f"Response: {response}")

        WhatTTS(response)

        time.sleep(1)
        
        await self.handle_commands(message)


def text_generator(message): # Generate response
    client = OpenAI(api_key=OAI_key)
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
    # Initialize variables (video_id, tts_type)
    VariableInitialization()
    bot = TwitchBot()

    # Check the platform
    try:
        if platform == "youtube":
            print("\nStarting YouTube Chat Reader!\n\n")
            YT_read_chat()

        elif platform == "twitch":
            print("\nStarting Twitch Chat Reader!\n\n")
            bot.run()

    except Exception as e:
        print("Error in main: " + str(e))
    
    print("\nStopping...\n")
    time.sleep(2)


if __name__ == "__main__": 
    main()
