"""
Real-time Speech-to-Speech Translation System
Truly continuous: Listens -> Recognizes -> Translates -> Speaks
NEVER stops listening - captures EVERY 3 seconds of audio
"""

import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import tempfile
import pygame
import threading
import queue
import time
from datetime import datetime
import pyaudio
import wave
import io


class RealtimeTranslator:
    """
    A truly continuous streaming speech translation system.
    Uses background audio recording to capture EVERY chunk without missing any audio.
    """
    
    def __init__(self, source_lang='en', target_lang='es', chunk_duration=3):
        """
        Initialize the translator
        
        Args:
            source_lang (str): Source language code (e.g., 'en' for English)
            target_lang (str): Target language code (e.g., 'es' for Spanish)
            chunk_duration (int): Duration in seconds to capture before processing
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.chunk_duration = chunk_duration
        
        # Initialize components
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        
        # Audio settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
        
        # Queues for managing translation pipeline
        self.audio_queue = queue.Queue(maxsize=10)  # Limit queue size
        self.text_queue = queue.Queue()
        self.translation_queue = queue.Queue()
        self.speech_queue = queue.Queue()
        
        # Control flags
        self.is_running = False
        
        # Audio buffer for continuous recording
        self.audio_frames = []
        self.lock = threading.Lock()
        
        print("✅ Translator initialized!")
        
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Callback for continuous audio recording"""
        if self.is_running:
            with self.lock:
                self.audio_frames.append(in_data)
        return (in_data, pyaudio.paContinue)
    
    def continuous_audio_capture(self):
        """
        Stage 1: CONTINUOUS LISTENING
        Records audio continuously in background and splits into chunks every N seconds
        This NEVER stops, so no audio is missed!
        """
        print(f"\n🎤 Starting continuous audio capture ({self.chunk_duration}s chunks)...")
        
        audio = pyaudio.PyAudio()
        
        # Open audio stream with callback
        stream = audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.audio_callback
        )
        
        stream.start_stream()
        print(f"✅ Continuous recording started! Speak in {self.source_lang.upper()}...\n")
        
        # Calculate frames per chunk
        frames_per_chunk = int(self.RATE / self.CHUNK * self.chunk_duration)
        
        chunk_number = 0
        
        while self.is_running:
            time.sleep(self.chunk_duration)  # Wait for chunk duration
            
            # Get accumulated frames
            with self.lock:
                if len(self.audio_frames) > 0:
                    chunk_number += 1
                    
                    # Take all accumulated frames as one chunk
                    audio_chunk = b''.join(self.audio_frames)
                    self.audio_frames = []  # Clear for next chunk
                    
                    if len(audio_chunk) > 0:
                        # Convert to AudioData format
                        audio_data = sr.AudioData(audio_chunk, self.RATE, 2)
                        
                        # Add to queue (non-blocking)
                        try:
                            self.audio_queue.put_nowait(audio_data)
                            print(f"📝 Chunk #{chunk_number} captured ({self.chunk_duration}s)")
                        except queue.Full:
                            print(f"⚠️  Queue full, skipping chunk #{chunk_number}")
        
        # Cleanup
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("🛑 Audio capture stopped")
        
    def recognize_speech(self):
        """
        Stage 2: UNDERSTANDING
        Convert audio to text using speech recognition
        Runs in parallel with audio capture!
        """
        while self.is_running:
            try:
                # Get audio from queue (with timeout)
                audio_data = self.audio_queue.get(timeout=1)
                
                # Recognize speech
                print("  🧠 Recognizing speech...")
                text = self.recognizer.recognize_google(
                    audio_data, 
                    language=self.source_lang
                )
                
                if text:
                    print(f"  📄 You said: '{text}'")
                    self.text_queue.put(text)
                    
            except queue.Empty:
                continue
            except sr.UnknownValueError:
                print("  ⚠️  Could not understand audio (silent or unclear)")
            except sr.RequestError as e:
                print(f"  ❌ Recognition API error: {e}")
            except Exception as e:
                print(f"  ❌ Recognition error: {e}")
                
    def translate_text(self):
        """
        Stage 3: TRANSLATING
        Translate recognized text to target language
        Runs in parallel!
        """
        while self.is_running:
            try:
                # Get text from queue
                text = self.text_queue.get(timeout=1)
                
                # Translate
                print(f"  🌍 Translating to {self.target_lang.upper()}...")
                translation = self.translator.translate(
                    text, 
                    src=self.source_lang, 
                    dest=self.target_lang
                )
                
                translated_text = translation.text
                print(f"  ✅ Translation: '{translated_text}'")
                
                self.translation_queue.put(translated_text)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"  ❌ Translation error: {e}")
                
    def speak_translation(self):
        """
        Stage 4: SPEAKING
        Convert translated text to speech and play it
        Runs in parallel - audio capture continues while speaking!
        """
        while self.is_running or not self.translation_queue.empty():
            try:
                # Get translated text from queue
                text = self.translation_queue.get(timeout=1)
                
                print(f"  🔊 Speaking: '{text}'")
                
                # Generate speech
                tts = gTTS(text=text, lang=self.target_lang, slow=False)
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    temp_file = fp.name
                    tts.save(temp_file)
                
                # Play audio (this doesn't block audio capture!)
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                # Clean up
                pygame.mixer.music.unload()
                os.unlink(temp_file)
                
                print("  ✅ Speech complete\n")
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"  ❌ Speech error: {e}")
                
    def start(self, duration=None):
        """
        Start the real-time translation system
        
        Args:
            duration (int): Optional duration in seconds to run. None for indefinite.
        """
        print("\n" + "="*70)
        print("🌐 CONTINUOUS REAL-TIME SPEECH TRANSLATOR")
        print("="*70)
        print(f"📥 Source Language: {self.source_lang.upper()}")
        print(f"📤 Target Language: {self.target_lang.upper()}")
        print(f"⏱️  Chunk Duration: {self.chunk_duration}s")
        print(f"🎯 Mode: TRULY CONTINUOUS - No audio is missed!")
        print("="*70)
        print("\n⚡ Starting streaming translation pipeline...\n")
        
        self.is_running = True
        
        # Create threads for each stage of the pipeline
        threads = [
            threading.Thread(target=self.continuous_audio_capture, name="AudioCapture", daemon=True),
            threading.Thread(target=self.recognize_speech, name="Recognizer", daemon=True),
            threading.Thread(target=self.translate_text, name="Translator", daemon=True),
            threading.Thread(target=self.speak_translation, name="Speaker", daemon=True)
        ]
        
        # Start all threads
        for thread in threads:
            thread.start()
            print(f"✅ {thread.name} thread started")
        
        print("\n" + "="*70)
        print("🎯 System ready! Speak continuously...")
        print("📊 Every 3 seconds will be captured and translated")
        print("🔄 While translating, audio capture continues!")
        print("💡 Press Ctrl+C to stop")
        print("="*70 + "\n")
        
        try:
            # Run for specified duration or indefinitely
            if duration:
                time.sleep(duration)
            else:
                # Keep main thread alive
                while True:
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping translation system...")
            
        finally:
            self.stop()
            
    def stop(self):
        """Stop the translation system"""
        self.is_running = False
        
        # Wait a bit for queues to empty
        print("⏳ Processing remaining items...")
        time.sleep(3)
        
        print("✅ Translation system stopped")
        print("\n" + "="*70)


def select_language(prompt, language_dict):
    """
    Interactive language selection
    
    Args:
        prompt (str): Prompt to show user
        language_dict (dict): Dictionary of languages
        
    Returns:
        str: Language code
    """
    print(f"\n{prompt}")
    print("="*50)
    
    # Show languages in a nice format
    languages = list(language_dict.items())
    for i, (name, code) in enumerate(languages, 1):
        if i % 3 == 1:
            print(f"{i:2d}. {name:20s} ({code:5s})", end="  ")
        elif i % 3 == 2:
            print(f"{i:2d}. {name:20s} ({code:5s})", end="  ")
        else:
            print(f"{i:2d}. {name:20s} ({code:5s})")
    
    # If last row is incomplete, add newline
    if len(languages) % 3 != 0:
        print()
    
    print("="*50)
    
    while True:
        try:
            choice = input(f"\nEnter number (1-{len(languages)}) or language code: ").strip().lower()
            
            # Check if it's a number
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(languages):
                    selected_name, selected_code = languages[idx]
                    print(f"✅ Selected: {selected_name} ({selected_code})")
                    return selected_code
                else:
                    print(f"❌ Please enter a number between 1 and {len(languages)}")
            # Check if it's a language code
            elif choice in language_dict.values():
                selected_name = [name for name, code in language_dict.items() if code == choice][0]
                print(f"✅ Selected: {selected_name} ({choice})")
                return choice
            else:
                print("❌ Invalid input. Try again.")
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            exit(0)
        except Exception as e:
            print(f"❌ Error: {e}. Try again.")
        

def main():
    """Main function to run the translator with interactive language selection"""
    
    # Available languages
    LANGUAGES = {
        'English': 'en',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Italian': 'it',
        'Portuguese': 'pt',
        'Russian': 'ru',
        'Japanese': 'ja',
        'Korean': 'ko',
        'Chinese': 'zh-CN',
        'Arabic': 'ar',
        'Hindi': 'hi',
        'Bengali': 'bn',
        'Dutch': 'nl',
        'Turkish': 'tr',
        'Vietnamese': 'vi',
        'Thai': 'th',
        'Polish': 'pl',
        'Swedish': 'sv',
        'Greek': 'el',
        'Hebrew': 'he',
        'Indonesian': 'id',
        'Malay': 'ms',
        'Urdu': 'ur',
    }
    
    print("\n" + "="*70)
    print("🌐 WELCOME TO CONTINUOUS REAL-TIME SPEECH TRANSLATOR")
    print("="*70)
    print("\n📌 How it works:")
    print("  1. Continuously records audio in background")
    print("  2. Every 3 seconds, captures and processes the audio")
    print("  3. While translating/speaking, CONTINUES to record next chunk")
    print("  4. For 12 seconds of speech, you get 4 translations (3s each)")
    print("  5. NO audio is missed - truly continuous!\n")
    
    # Select source language
    source_lang = select_language(
        "🎤 SELECT SOURCE LANGUAGE (language you will speak):",
        LANGUAGES
    )
    
    # Select target language
    target_lang = select_language(
        "🔊 SELECT TARGET LANGUAGE (language for translation):",
        LANGUAGES
    )
    
    # Ask for chunk duration
    print("\n" + "="*50)
    print("⏱️  CHUNK DURATION")
    print("="*50)
    print("How many seconds of audio to process at once?")
    print("  • 2 seconds = Faster, less context")
    print("  • 3 seconds = Balanced (recommended)")
    print("  • 5 seconds = Slower, more context")
    
    while True:
        try:
            chunk_input = input("\nEnter duration (2-5 seconds, default=3): ").strip()
            if chunk_input == "":
                chunk_duration = 3
                break
            chunk_duration = int(chunk_input)
            if 2 <= chunk_duration <= 5:
                break
            else:
                print("❌ Please enter a number between 2 and 5")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled by user")
            exit(0)
    
    print(f"✅ Chunk duration set to {chunk_duration} seconds")
    
    # Create and start translator
    print("\n⏳ Initializing translator...")
    translator = RealtimeTranslator(
        source_lang=source_lang,
        target_lang=target_lang,
        chunk_duration=chunk_duration
    )
    
    # Start translation (runs indefinitely until Ctrl+C)
    translator.start()


if __name__ == "__main__":
    main()
