"""
Advanced Real-time Speech-to-Speech Translation System
Uses OpenAI Whisper for improved accuracy and Deep Translator for better translations
"""

import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import tempfile
import pygame
import threading
import queue
import time
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from collections import deque


class WhisperRealtimeTranslator:
    """
    Advanced streaming speech translation using Whisper AI
    Better accuracy than Google Speech Recognition
    """
    
    def __init__(self, source_lang='en', target_lang='es', model_size='base', 
                 chunk_duration=5, sample_rate=16000):
        """
        Initialize the advanced translator
        
        Args:
            source_lang (str): Source language code
            target_lang (str): Target language code
            model_size (str): Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
                             - tiny: Fastest, least accurate
                             - base: Good balance (recommended)
                             - small: Better accuracy
                             - medium/large: Best accuracy, slower
            chunk_duration (int): Seconds of audio per chunk
            sample_rate (int): Audio sample rate (16000 recommended for Whisper)
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.chunk_duration = chunk_duration
        self.sample_rate = sample_rate
        
        # Load Whisper model
        print(f"🤖 Loading Whisper '{model_size}' model... (This may take a minute)")
        self.whisper_model = whisper.load_model(model_size)
        print("✅ Whisper model loaded!")
        
        # Initialize translator
        self.translator = GoogleTranslator(source=source_lang, target=target_lang)
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
        
        # Queues for pipeline stages
        self.audio_queue = queue.Queue()
        self.text_queue = queue.Queue()
        self.translation_queue = queue.Queue()
        
        # Translation cache to avoid re-translating same phrases
        self.translation_cache = {}
        
        # Control flags
        self.is_running = False
        self.is_recording = False
        
        # Audio buffer
        self.audio_buffer = deque(maxlen=int(sample_rate * chunk_duration))
        
    def record_audio_chunk(self):
        """
        Stage 1: LISTENING
        Record audio continuously in chunks using sounddevice
        """
        print(f"\n🎤 Listening in {self.source_lang.upper()}... Speak now!\n")
        
        def audio_callback(indata, frames, time_info, status):
            """Callback for audio stream"""
            if status:
                print(f"⚠️  Audio status: {status}")
            
            # Add audio to buffer
            self.audio_buffer.extend(indata[:, 0])
        
        # Start audio stream
        with sd.InputStream(samplerate=self.sample_rate, 
                           channels=1, 
                           callback=audio_callback,
                           dtype='float32'):
            
            while self.is_running:
                time.sleep(self.chunk_duration)
                
                if len(self.audio_buffer) > 0:
                    # Convert buffer to numpy array
                    audio_chunk = np.array(list(self.audio_buffer))
                    
                    # Check if there's actual speech (not just silence)
                    if np.abs(audio_chunk).max() > 0.01:  # Threshold for silence
                        print("📝 Audio chunk captured")
                        self.audio_queue.put(audio_chunk.copy())
                    
                    # Clear buffer for next chunk
                    self.audio_buffer.clear()
    
    def transcribe_audio(self):
        """
        Stage 2: UNDERSTANDING
        Transcribe audio to text using Whisper
        """
        while self.is_running:
            try:
                # Get audio chunk
                audio_chunk = self.audio_queue.get(timeout=1)
                
                print("🧠 Transcribing with Whisper...")
                
                # Transcribe using Whisper
                result = self.whisper_model.transcribe(
                    audio_chunk,
                    language=self.source_lang,
                    fp16=False,  # Use fp32 for CPU
                    verbose=False
                )
                
                text = result['text'].strip()
                
                if text:
                    print(f"📄 Transcribed: '{text}'")
                    self.text_queue.put(text)
                else:
                    print("⚠️  No speech detected in chunk")
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Transcription error: {e}")
    
    def translate_text(self):
        """
        Stage 3: TRANSLATING
        Translate text using Deep Translator with caching
        """
        while self.is_running:
            try:
                # Get text
                text = self.text_queue.get(timeout=1)
                
                # Check cache first
                if text in self.translation_cache:
                    translated_text = self.translation_cache[text]
                    print(f"💾 From cache: '{translated_text}'")
                else:
                    print(f"🌍 Translating to {self.target_lang.upper()}...")
                    
                    # Translate
                    translated_text = self.translator.translate(text)
                    
                    # Cache the translation
                    self.translation_cache[text] = translated_text
                    
                    print(f"✅ Translation: '{translated_text}'")
                
                self.translation_queue.put(translated_text)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Translation error: {e}")
    
    def speak_translation(self):
        """
        Stage 4: SPEAKING
        Convert translated text to speech and play it
        """
        while self.is_running or not self.translation_queue.empty():
            try:
                # Get translated text
                text = self.translation_queue.get(timeout=1)
                
                print(f"🔊 Speaking: '{text}'")
                
                # Generate speech
                tts = gTTS(text=text, lang=self.target_lang, slow=False)
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    temp_file = fp.name
                    tts.save(temp_file)
                
                # Play audio
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                # Clean up
                pygame.mixer.music.unload()
                os.unlink(temp_file)
                
                print("✅ Speech complete\n")
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Speech error: {e}")
    
    def start(self):
        """Start the advanced translation system"""
        print("\n" + "="*70)
        print("🚀 ADVANCED REAL-TIME SPEECH TRANSLATOR (Whisper AI)")
        print("="*70)
        print(f"Source Language: {self.source_lang.upper()}")
        print(f"Target Language: {self.target_lang.upper()}")
        print(f"Model: Whisper ({self.whisper_model.__class__.__name__})")
        print(f"Chunk Duration: {self.chunk_duration}s")
        print(f"Sample Rate: {self.sample_rate} Hz")
        print("="*70)
        print("\n⚡ Starting advanced translation pipeline...\n")
        
        self.is_running = True
        
        # Create pipeline threads
        threads = [
            threading.Thread(target=self.record_audio_chunk, name="Recorder", daemon=True),
            threading.Thread(target=self.transcribe_audio, name="Whisper", daemon=True),
            threading.Thread(target=self.translate_text, name="Translator", daemon=True),
            threading.Thread(target=self.speak_translation, name="Speaker", daemon=True)
        ]
        
        # Start all threads
        for thread in threads:
            thread.start()
            print(f"✅ {thread.name} thread started")
        
        print("\n🎯 System ready! Start speaking...\n")
        print("💡 Press Ctrl+C to stop\n")
        print(f"📊 Translation cache: {len(self.translation_cache)} entries\n")
        
        try:
            while True:
                time.sleep(5)
                # Periodically show cache size
                if len(self.translation_cache) > 0:
                    print(f"💾 Cache: {len(self.translation_cache)} translations stored")
                
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping translation system...")
            self.stop()
    
    def stop(self):
        """Stop the translation system"""
        self.is_running = False
        
        print("⏳ Processing remaining items...")
        time.sleep(2)
        
        print(f"✅ Translation system stopped")
        print(f"📊 Final cache size: {len(self.translation_cache)} translations")
        print("\n" + "="*70)


def main():
    """Main function to run the advanced translator"""
    
    # Configuration
    SOURCE_LANGUAGE = 'en'      # Your language
    TARGET_LANGUAGE = 'es'      # Target language
    
    # Model selection
    # 'tiny'   - Fastest, least accurate, ~1GB RAM
    # 'base'   - Good balance (RECOMMENDED), ~1GB RAM
    # 'small'  - Better accuracy, ~2GB RAM
    # 'medium' - Great accuracy, ~5GB RAM
    # 'large'  - Best accuracy, ~10GB RAM
    MODEL_SIZE = 'base'
    
    CHUNK_DURATION = 5          # Longer chunks = better context for Whisper
    
    # Create and start translator
    translator = WhisperRealtimeTranslator(
        source_lang=SOURCE_LANGUAGE,
        target_lang=TARGET_LANGUAGE,
        model_size=MODEL_SIZE,
        chunk_duration=CHUNK_DURATION
    )
    
    # Start translation
    translator.start()


if __name__ == "__main__":
    main()
