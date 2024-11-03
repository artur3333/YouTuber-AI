# YouTuber-AI

**YouTuber-AI** is a Python application that reads live chat messages from a specified YouTube livestream and generates AI-driven responses using OpenAI's GPT-3.5 model. The responses are converted to speech using a Text-to-Speech (TTS) engine, creating an interactive and engaging experience for livestream audiences.

## Features
- **AI-Powered Responses**: Leverages OpenAI’s API to generate conversational responses from live chat messages in real time.
- **Text-to-Speech Output**: Converts responses to audio using either `pyttsx3` or `OpenAI's TTS` options, making the interaction vocal and dynamic.
- **Live Chat Processing**: Reads and processes messages from YouTube livestreams.
- **Configurable TTS Options**: Choose between different TTS engines.

## Requirements
- **Python**: 3.x
- **API Key**: OpenAI API key (required for AI-driven responses)
- **FFmpeg**: Required for handling audio processing
- **Dependencies**: Install via `requirements.txt`

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
    - Replace `"YOUR_OpenAI_KEY"` with your actual OpenAI API key as shown below:
      ```json
      {
          "apikeys": [
              {
                  "OAI_key": "YOUR_OpenAI_KEY"
              }
          ]
      }
      ```

## Directory Tree

```plaintext
YouTuber-AI
├── main.py             # Main script to run the application
├── config.json         # Configuration file for storing API keys and settings
├── ffmpeg.exe          # FFmpeg executable for audio processing (Windows)
├── ffprobe.exe         # FFprobe executable for media information (Windows)
├── requirements.txt    # List of Python dependencies
└── README.md           # Project readme with usage instructions and details
```

## Usage

To start YouTuber-AI, open a terminal, navigate to the project directory, and run the following command:

```bash
python main.py -id <LIVE_STREAM_ID> -tts <TTS_TYPE>
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork** the repository.
2. **Create a new branch** for your feature or bug fix.
3. **Make your changes** and test them.
4. **Submit** a pull request describing your changes.
