
---

# SpeechRecognitionLive

## Overview

SpeechRecognitionLive is a Python project that enables real-time speech recognition using the SpeechRecognition library. With this project, you can easily capture audio from your microphone, transcribe it into text, and even play back the recognized text as audio.

## Features

- Real-time speech recognition: Capture audio from the microphone and transcribe it into text in real-time.
- Pause detection: Automatically detects pauses in speech to improve transcription accuracy and efficiency.
- Adjustable silence threshold: Customize the duration of silence required to end speech input.
- Internet connection check: Ensures proper handling of errors when unable to connect to the internet for transcription.

## Installation

1. Clone the repository:

```
git clone https://github.com/mayurbt12/SpeechRecognitionLive.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Run the main script:

```
python main.py
```

## Usage

1. Run the `main.py` script to start the real-time speech recognition process.
2. Speak into your microphone to provide input. The program will transcribe your speech into text.
3. Adjust the silence threshold as needed to control when speech input ends.
4. Pause detection will automatically stop speech input after a period of silence.
5. Exit the program by saying "exit" or pressing `Ctrl + C`.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/improvement`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/improvement`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
