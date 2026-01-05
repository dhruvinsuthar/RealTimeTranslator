# 🎤 Real-time Speech Translation System

A powerful real-time speech-to-speech translation system that listens to your voice, translates it to another language, and speaks it out loud. Built with Python and supports multiple languages.

## 🌟 Features

- 🎤 **Real-time speech recognition** using Google Speech Recognition
- 🌍 **Multi-language translation** with Google Translate
- 🔊 **Natural text-to-speech** output
- 🚀 **Multiple implementations** for different use cases
- 🖥️ **GUI interface** available
- 🎯 **Easy to configure** and customize

## 📋 System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Microphone**: Required for speech input
- **Internet Connection**: Required for translation services
- **Audio Output**: Speakers or headphones

## 🛠️ Installation

### Step 1: Clone or Download
```bash
git clone <your-repo-url>
cd "Gen ai translate"
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**For advanced Whisper version (best accuracy), also install:**
```bash
pip install openai-whisper sounddevice
```

### Step 3: Verify Installation
Run the simple example to test:
```bash
python simple_example.py
```

## 🚀 Usage

### Option 1: Simple Example (Recommended for Beginners)
Best for testing and learning. Single translation at a time.

```bash
python simple_example.py
```

**Features:**
- ✅ Easy to understand
- ✅ Interactive mode available
- ✅ Good for testing

### Option 2: Real-time Streaming (Recommended for Production)
Continuous real-time translation with minimal latency.

```bash
python realtime_translator.py
```

**Features:**
- ✅ Continuous streaming
- ✅ Multi-threaded pipeline
- ✅ Natural conversation flow
- ✅ Minimal latency

### Option 3: Advanced Whisper (Best Accuracy)
Uses OpenAI Whisper AI for superior speech recognition.

```bash
python advanced_whisper_translator.py
```

**Features:**
- ✅ State-of-the-art accuracy
- ✅ Better noise handling
- ✅ Multiple accents support
- ✅ Translation caching

**Note:** First run downloads the Whisper model (~140MB for 'base' model)

### Option 4: GUI Version
Graphical interface with buttons and visual feedback.

```bash
python gui_translator.py
```

**Features:**
- ✅ User-friendly interface
- ✅ Click to start/stop
- ✅ Visual status indicators

## ⚙️ Configuration

### Changing Languages

Edit `config.py` or modify the language settings in any Python file:

```python
SOURCE_LANGUAGE = 'en'  # Your spoken language
TARGET_LANGUAGE = 'es'  # Translation target language
```

### Supported Language Codes

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | `en` | Spanish | `es` |
| French | `fr` | German | `de` |
| Italian | `it` | Portuguese | `pt` |
| Russian | `ru` | Japanese | `ja` |
| Korean | `ko` | Chinese (Simplified) | `zh-CN` |
| Chinese (Traditional) | `zh-TW` | Arabic | `ar` |
| Hindi | `hi` | Bengali | `bn` |
| Dutch | `nl` | Turkish | `tr` |
| Vietnamese | `vi` | Thai | `th` |
| Polish | `pl` | Swedish | `sv` |

For more languages, check the `LANGUAGE_CODES` dictionary in `config.py`.

### Advanced Settings (in config.py)

```python
# Audio Settings
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
SILENCE_THRESHOLD = 3000

# Recognition Settings
ENERGY_THRESHOLD = 4000
DYNAMIC_ENERGY_THRESHOLD = True
PHRASE_TIME_LIMIT = 5

# Whisper Model (for advanced_whisper_translator.py)
MODEL_SIZE = 'base'  # Options: tiny, base, small, medium, large
```

## 📦 Dependencies

**Core dependencies:**
- `SpeechRecognition` - Speech-to-text
- `googletrans` - Translation service
- `gTTS` - Text-to-speech
- `PyAudio` - Audio capture
- `pygame` - Audio playback

**Optional (for Whisper version):**
- `openai-whisper` - Advanced speech recognition
- `torch` - Machine learning backend

## 🏗️ Architecture

### Simple Example Flow
```
[Microphone] → [Speech Recognition] → [Translation] → [Text-to-Speech] → [Speaker]
```

### Real-time Streaming Flow
```
[Microphone] → [Queue 1] → [Speech Recognition] → [Queue 2] 
→ [Translation] → [Queue 3] → [Text-to-Speech] → [Speaker]

All stages run in parallel for minimal latency!
```

### Advanced Whisper Flow
```
[Microphone] → [Whisper AI] → [Cache Check] → [Translation] 
→ [Text-to-Speech] → [Speaker]
```

## 🎯 Use Cases

- **Travel**: Communicate in foreign countries
- **Business**: International meetings and calls
- **Education**: Language learning assistant
- **Healthcare**: Patient communication
- **Customer Service**: Multilingual support
- **Accessibility**: Helping people with language barriers

## ⚠️ Troubleshooting

### Microphone not detected
```bash
# Test your microphone
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

### PyAudio installation fails (Windows)
Download the pre-built wheel from:
```
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```
Then install:
```bash
pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl
```

### "Could not understand audio"
- Speak clearly and close to the microphone
- Reduce background noise
- Adjust microphone sensitivity in system settings
- Try the Whisper version for better accuracy

### Internet connection required
All versions require internet for:
- Speech recognition (Google API)
- Translation (Google Translate)
- Text-to-speech (gTTS)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📝 License

This project is open source and available for educational and personal use.

## 🔗 Resources

- [Google Speech Recognition](https://cloud.google.com/speech-to-text)
- [Google Translate](https://translate.google.com/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [gTTS Documentation](https://gtts.readthedocs.io/)

## � Contributors

This project is built and maintained by:

- **Dhruvin Suthar** - [@dhruvinsuthar](https://github.com/dhruvinsuthar)
- **Prem Singh** - [@Prem4modsing](https://github.com/Prem4modsing)

Built with ❤️ for breaking down language barriers

---

**Questions or Issues?** Create an issue on GitHub or check the troubleshooting section above.
