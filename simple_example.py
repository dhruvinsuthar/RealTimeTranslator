"""
Simple Example - Quick Start Real-time Translator
Minimal version for testing and learning
"""

import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import os
import tempfile


def simple_translate(source_lang='en', target_lang='es'):
    """
    Simplified one-shot translation
    Listen -> Recognize -> Translate -> Speak
    """
    
    # Initialize components
    recognizer = sr.Recognizer()
    translator = Translator()
    pygame.mixer.init()
    
    print("\n" + "="*50)
    print("🎤 SIMPLE SPEECH TRANSLATOR")
    print("="*50)
    print(f"Speak in {source_lang.upper()} - I'll translate to {target_lang.upper()}")
    print("="*50 + "\n")
    
    with sr.Microphone() as source:
        # Calibrate for ambient noise
        print("🎧 Adjusting for background noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("✅ Ready! Please speak now...\n")
        
        try:
            # Listen
            print("🎤 Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            print("✅ Audio captured!\n")
            
            # Recognize
            print("🧠 Recognizing speech...")
            text = recognizer.recognize_google(audio, language=source_lang)
            print(f"📄 You said: '{text}'\n")
            
            # Translate
            print(f"🌍 Translating to {target_lang.upper()}...")
            translation = translator.translate(text, src=source_lang, dest=target_lang)
            translated_text = translation.text
            print(f"✅ Translation: '{translated_text}'\n")
            
            # Speak
            print("🔊 Speaking translation...")
            tts = gTTS(text=translated_text, lang=target_lang, slow=False)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
                tts.save(temp_file)
            
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pass
            
            pygame.mixer.music.unload()
            os.unlink(temp_file)
            
            print("✅ Done!\n")
            print("="*50)
            
        except sr.WaitTimeoutError:
            print("❌ No speech detected. Please try again.")
        except sr.UnknownValueError:
            print("❌ Could not understand the audio. Please speak clearly.")
        except sr.RequestError as e:
            print(f"❌ Could not request results; {e}")
        except Exception as e:
            print(f"❌ Error: {e}")


def interactive_mode():
    """
    Interactive mode - keep translating until user quits
    """
    
    print("\n🌐 INTERACTIVE TRANSLATION MODE")
    print("Speak multiple times - Press Ctrl+C to quit\n")
    
    # Get language preferences
    print("Available languages:")
    print("  en = English, es = Spanish, fr = French, de = German")
    print("  ja = Japanese, zh-CN = Chinese, ar = Arabic, hi = Hindi")
    
    source = input("\nEnter source language code (default: en): ").strip() or 'en'
    target = input("Enter target language code (default: es): ").strip() or 'es'
    
    print(f"\n✅ Set up: {source.upper()} → {target.upper()}")
    print("Starting translations...\n")
    
    count = 0
    try:
        while True:
            count += 1
            print(f"\n--- Translation #{count} ---")
            simple_translate(source, target)
            
            print("\n💡 Speak again or press Ctrl+C to quit...")
            
    except KeyboardInterrupt:
        print(f"\n\n✅ Completed {count} translations. Goodbye! 👋")


if __name__ == "__main__":
    # Choose mode
    print("\n🎯 Choose mode:")
    print("1. Single translation (test)")
    print("2. Interactive mode (continuous)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '1':
        # Single translation with default languages
        simple_translate(source_lang='en', target_lang='es')
    else:
        # Interactive mode
        interactive_mode()
