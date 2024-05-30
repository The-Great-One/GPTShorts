# YouTube Shorts Generator

Welcome to the YouTube Shorts Generator repository! This project leverages AI tools to automate the creation of YouTube Shorts, making it easy to produce engaging and high-quality short videos with minimal effort.

## Features

- **Script Processing:** Uses ChatGPT for processing the script of the video.
- **Video Download:** Download videos from various sources like YouTube, Rumble, etc.
- **Transcription:** Uses Whisper for transcribing since only YouTube provides transcripts.
- **Open Source:** This project is open source and welcomes contributions from the community.

## Getting Started

### Prerequisites

- Python 3.8 or later
- pip (Python package installer)
- Git
- OpenAI API Key (for ChatGPT and Whisper)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/YouTube-Shorts-Generator.git
    cd YouTube-Shorts-Generator
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set your OpenAI API Key:**

    Set the OpenAI API key in your environment variables:

    ```bash
    export OPENAI_API_KEY='your-openai-api-key'  # On Windows use `set OPENAI_API_KEY=your-openai-api-key`
    ```

### Usage

1. **Run the main script to generate YouTube Shorts:**

    ```bash
    python GenShorts.py
    ```
