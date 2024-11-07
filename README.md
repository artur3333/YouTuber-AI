# YouTuber-AI

**YouTuber-AI** is a Python application that reads live chat messages from a specified YouTube or Twitch livestream and generates AI-driven responses using OpenAI's `gpt-4o-mini` model, remembers previous messages from users, and saves the chat logs for future reference. It also generate spoken responses using text-to-speech (TTS) systems. The program includes both command-line and graphical user interface (GUI).

## Features
- **AI-Powered Responses**: Uses OpenAI’s API to generate conversational responses from live chat messages in real time.
- **Chat History**: Remembers chat history for context-aware responses.
- **Chat Logging**: Saves chat logs for later review.
- **Text-to-Speech Output**: Converts responses to audio using either `pyttsx3` or `OpenAI's TTS` options, making the interaction vocal and dynamic.
- **Multi-Platform**: Choose between different platforms: `youtube` or `twitch`.
- **Live Chat Processing**: Reads and processes messages from YouTube or Twitch livestreams.
- **Configurable TTS Options**: Choose between different TTS engines.
- **UI interface**: Provides an intuitive interface (`ui_app.py`) for setting configurations and running the program.

## Requirements
- **Python**: 3.x
- **API Key**: OpenAI API key (required for AI-driven responses)
- **FFmpeg**: Required for handling audio processing
- **Dependencies**: Install via `requirements.txt`
- **Twitch token**: Can be generated on [this website](https://twitchtokengenerator.com/) by setting the flag on `chat:read` and `chat:edit`.

## Installation

1. **Clone the repository** and navigate to the project folder:
    ```bash
    git clone https://github.com/artur3333/YouTuber-AI.git
    cd YouTuber-AI
    ```

2. **Install the required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install FFmpeg**:
   FFmpeg is needed for audio processing. Follow the instructions below based on your operating system:

   - **Ubuntu or Debian-based systems**:
     ```bash
     sudo apt update && sudo apt install ffmpeg
     ```
   - **macOS (using Homebrew)**:
     ```bash
     brew install ffmpeg
     ```
   - **Windows**:
     - Download FFmpeg from [FFmpeg's official site](https://ffmpeg.org/download.html).
     - Unzip the downloaded file, and add the files (ffmpeg.exe and ffprobe.exe) contained in FFmpeg `bin` directory to the project's PATH. 

4. **Configure your OpenAI API key**:
    - Open the `config.json` file in a text editor.
    - Replace `YOUR_OpenAI_KEY` with your actual OpenAI API key as shown below:
      ```json
      {
          "apikeys": [
              {
                  "OAI_key": "YOUR_OpenAI_KEY"
              }
          ]
      }
      ```

5. **Configure your Twitch Token and Channel**:
    - Open the `config.json` file in a text editor.
    - Replace `YOUR_TWITCH_TOKEN` with your Twitch token which can be generated on [this website](https://twitchtokengenerator.com/).
    - Replace `YOUR_NICKNAME` with your nickname.
    - Replace `YOUR_CHANNEL` with the name of your Twitch Channel.
      ```json
      {
          "apikeys": [
              {
                  "OAI_key": "YOUR_OpenAI_KEY"
              }
          ],
            
          "twitch": [
              {
                "token": "YOUR_TWITCH_TOKEN",
                "nickname": "YOUR_NICKNAME",
                "channel": "YOUR_CHANNEL"
              }
          ]
      }
      ```

## Directory Tree

```plaintext
YouTuber-AI
├── main.py                 # Main script to run the application
├── ui_app.py               # GUI application for easier configuration and management
├── config.json             # Configuration file for storing API keys and settings
├── conversation.json       # Stores the conversation history used for generating responses
├── conversation_log.txt    # Saves all chat logs and AI responses
├── ffmpeg.exe              # FFmpeg executable for audio processing (Windows)
├── ffprobe.exe             # FFprobe executable for media information (Windows)
├── icon.ico                # The Icon
├── requirements.txt        # List of Python dependencies
└── README.md               # Project readme with usage instructions and details
```

## Usage
### Command Line Interface (CLI)
To start YouTuber-AI, open a terminal in the project directory and run main.py with the necessary arguments:

```bash
python main.py -id <LIVE_STREAM_ID> -tts <TTS_TYPE> -p <PLATFORM> -d
```
- -id <LIVE_STREAM_ID>: YouTube only. The ID of the live stream.
- -tts <TTS_TYPE>: Text-to-Speech type. Options: `pyttsx3` or `openai`.
- -p <PLATFORM>: Platform for streaming. Options: `youtube` or `twitch`.
- -d: Enables debug mode for detailed logs.

---
### Graphical User Interface (GUI)
To start YouTuber-AI, open a terminal in the project directory and run ui_app.py:
```bash
python ui_app.py
```
- Enter the YouTube Stream ID (if applicable).
- Select the TTS Type (either `pyttsx3` or `openai`).
- Choose the Platform (`YouTube` or `Twitch`).
- Optionally, check Enable Debug Mode for detailed logs.

---

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork** the repository.
2. **Create a new branch** for your feature or bug fix.
3. **Make your changes** and test them.
4. **Submit** a pull request describing your changes.
