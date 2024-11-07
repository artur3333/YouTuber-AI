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
from datetime import datetime
from openai import OpenAI


sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1) # Set the standard output encoding to UTF-8


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
    global speak
    global conversation, history_conversation
    global now, prev
    global characters
    global token, nickname, channel
    global debug_option
    global LOG_FILE

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

    conversation = []
    history_conversation = {"history": conversation}

    now = ""
    prev = ""

    parser = argparse.ArgumentParser() # Command line arguments
    parser.add_argument("-id", "--video_id", type=str, help="Video ID")
    parser.add_argument("-tts", "--tts_type", type=str, help="TTS Type", choices=tts_list, default="pyttsx3")
    parser.add_argument("-p", "--platform", type=str, help="Platform", choices=platform_list)
    parser.add_argument("-d", "--debug", action="store_true", help="Debug mode")
    args = parser.parse_args()
    
    video_id = args.video_id
    tts_type = args.tts_type
    platform = args.platform
    debug_option = args.debug

    speak = False
    characters = 0

    LOG_FILE = "conversation_log.txt"

    if tts_type == "pyttsx3":
        PyTTSInitialization()


def WhatTTS(message): # Check which TTS to use 
    if tts_type == "openai":
        OAI_TTS(message)
    
    elif tts_type == "pyttsx3":
        Py_TTS(message)


def getMessage(): # Get the message with history
    message = [{"role": "system", "content": "Below is the conversation history.\n"}]
    global conversation
    global history_conversation

    # Read the history from the JSON file
    try:
        with open("conversation.json", "r") as f:
            data = json.load(f)
            conversation = data.get("history", [])
            if debug_option:
                print("Loaded history from JSON:", history_conversation)

    except FileNotFoundError:
        print("conversation.json file not found.")
        conversation = []
        history_conversation = {"history": conversation}

    # Append the messages to the message list
    for m in history_conversation["history"][:-1]:
        message.append(m)

    # Say to the AI that this is the last message
    if history_conversation:
        message.append({"role": "system", "content": "This is the last message.\n"})
        message.append(history_conversation["history"][-1])

    if debug_option:    
        print("Final message list:", message)
    return message


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
            speak = True
            winsound.PlaySound(wav_file_path, winsound.SND_FILENAME)
            speak = False

        else:
            print("Error in OAI_TTS: No speech file found or file is empty.")

    except Exception as e:
        print("Error in OAI_TTS: " + str(e))


# Read the YouTube chat
def YT_read_chat():
    global prev, now
    chat = pytchat.create(video_id=video_id)

    while chat.is_alive():
        try:
            for c in chat.get().sync_items():
                try:
                    # Print the chat message
                    chatmsg = (f"\n{c.datetime} {c.author.name} > {c.message}\n")
                    print(chatmsg)
                    message_youtube = (f"{c.author.name} said {c.message}")

                    if speak == False and now != prev:
                        conversation.append({"role": "user", "content": now})
                        prev = now

                    log_entry = (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {c.author.name} > {c.message}\n")
                    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
                        log_file.write(log_entry)

                    # Generate response
                    response = text_generator(message_youtube)
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


class TwitchBot(commands.Bot): # Twitch Bot class
    def __init__(self):
        super().__init__(token=token, prefix="!", initial_channels=[channel])

    async def event_ready(self):
        if debug_option:
            print(f"Bot is ready! {self.nick}")
    
    async def event_message(self, message):
        global prev, now

        username = message.author.name
        content = message.content
        datetime = message.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        chatmsg = (f"\n{datetime} {username} > {content}\n")
        print(chatmsg)
        message_twitch = (f"{username} said {content}")

        if speak == False and now != prev:
            conversation.append({"role": "user", "content": now})
            prev = now

        log_entry = (f"{datetime} - {username} > {content}\n")
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)

        response = text_generator(message_twitch)
        print(f"Response: {response}")

        WhatTTS(response)

        time.sleep(1)
        
        await self.handle_commands(message)


def text_generator(message): # Generate response
    global conversation
    global history_conversation
    global characters

    # calculate the total character count of the conversation
    characters = sum(len(d['content']) for d in conversation)

    # Remove older messages if character count exceeds 2000
    while characters > 2000:
        try:
            conversation.pop(2)
            characters = sum(len(d['content']) for d in conversation)
        except Exception as e:
            print("Error in popping older messages: " + str(e))

    # Append the new message to conversation history
    conversation.append({"role": "user", "content": message})
    history_conversation["history"] = conversation

    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump(history_conversation, f, indent=4)

    # Getting the message with history
    message_text = getMessage()

    client = OpenAI(api_key=OAI_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "max_tokens": 32,
                "content": "This is how a female streamer responded in a conversation. She would respond in a friendly manner. She would talk about the message and would elaborate on it as well as share some of her experiences if possible. She also can use only 32 tokens, so she can't speak much per message."
            },
            {
                "role": "user",
                "content": f"\n----------\n{message_text}\n----------\n"
            }
        ]
    )
    
    try:
        response_text = completion.choices[0].message.content

        response_text_for_history = (f"you responded: {response_text}")
        conversation.append({"role": "assistant", "content": response_text_for_history})
        history_conversation["history"] = conversation

        log_entry_responce = (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - AI > {response_text}\n")
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry_responce)

        with open("conversation.json", "w", encoding="utf-8") as f:
            json.dump(history_conversation, f, indent=4)

        return response_text
    
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
