# YouTuber-AI

**YouTuber-AI** is a Python application that reads live chat messages from a specified YouTube livestream and generates AI-driven responses using OpenAI's GPT-3.5 model. The responses can be converted to speech using a Text-to-Speech (TTS) engine, providing a more engaging, conversational experience for livestream audiences. 

## Features
- **AI-Powered Responses**: Uses OpenAI’s API to generate responses based on livestream chat messages.
- **Text-to-Speech Output**: Converts responses to speech using `pyttsx3` (currently the only supported TTS engine).
- **Live Chat Processing**: Reads and processes messages from YouTube livestreams in real time.

## Requirements
- Python 3.x
- OpenAI API Key (required for generating AI responses)
- Dependencies (installed via `requirements.txt`)

## Installation
1. Clone the repository and navigate to the project folder:
    ```bash
    git clone https://github.com/artur3333/YouTuber-AI.git
    cd YouTuber-AI
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure your OpenAI API key:
    - Open the `config.json` file in a text editor.
    - Replace `"YOUR_OpenAI_KEY"` with your actual OpenAI API key:
      ```json
      {
          "apikeys": [
              {
                  "OAI_key": "YOUR_OpenAI_KEY"
              }
          ]
      }
      ```

## Usage
To start YouTuber-AI, open a terminal, navigate to the project directory, and run:

```bash
python main.py -id <LIVE_STREAM_ID> -tts pyttsx3
