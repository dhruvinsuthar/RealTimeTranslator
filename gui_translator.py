"""
GUI Real-time Speech Translator
Simple graphical interface for the translation system
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import threading
import queue
import tempfile
import os


class TranslatorGUI:
    """Graphical User Interface for Real-time Translator"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 Real-time Speech Translator")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Initialize components
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        pygame.mixer.init()
        
        # State
        self.is_running = False
        self.microphone = None
        
        # Queues
        self.text_queue = queue.Queue()
        
        # Setup GUI
        self.setup_ui()
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self.process_queue, daemon=True)
        self.processing_thread.start()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Title
        title_frame = tk.Frame(self.root, bg="#2C3E50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🌐 Real-time Speech Translator",
            font=("Arial", 18, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Control Panel
        control_frame = tk.Frame(self.root, bg="#ECF0F1", padx=20, pady=15)
        control_frame.pack(fill=tk.X)
        
        # Language Selection
        lang_frame = tk.Frame(control_frame, bg="#ECF0F1")
        lang_frame.pack(fill=tk.X, pady=5)
        
        # Source Language
        tk.Label(lang_frame, text="From:", bg="#ECF0F1", font=("Arial", 10)).grid(row=0, column=0, padx=5, sticky="w")
        self.source_lang = ttk.Combobox(lang_frame, width=15, state="readonly")
        self.source_lang['values'] = [
            'English (en)', 'Spanish (es)', 'French (fr)', 'German (de)',
            'Chinese (zh-CN)', 'Japanese (ja)', 'Arabic (ar)', 'Hindi (hi)',
            'Portuguese (pt)', 'Russian (ru)', 'Korean (ko)', 'Italian (it)'
        ]
        self.source_lang.current(0)  # Default: English
        self.source_lang.grid(row=0, column=1, padx=5)
        
        # Arrow
        tk.Label(lang_frame, text="→", bg="#ECF0F1", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=10)
        
        # Target Language
        tk.Label(lang_frame, text="To:", bg="#ECF0F1", font=("Arial", 10)).grid(row=0, column=3, padx=5, sticky="w")
        self.target_lang = ttk.Combobox(lang_frame, width=15, state="readonly")
        self.target_lang['values'] = self.source_lang['values']
        self.target_lang.current(1)  # Default: Spanish
        self.target_lang.grid(row=0, column=4, padx=5)
        
        # Buttons
        button_frame = tk.Frame(control_frame, bg="#ECF0F1")
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(
            button_frame,
            text="▶ Start Listening",
            font=("Arial", 11, "bold"),
            bg="#27AE60",
            fg="white",
            padx=20,
            pady=10,
            command=self.start_translation,
            cursor="hand2"
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="⏹ Stop",
            font=("Arial", 11, "bold"),
            bg="#E74C3C",
            fg="white",
            padx=20,
            pady=10,
            command=self.stop_translation,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = tk.Label(
            control_frame,
            text="⚪ Ready - Click 'Start Listening' to begin",
            bg="#ECF0F1",
            font=("Arial", 10, "italic")
        )
        self.status_label.pack(pady=5)
        
        # Output Area
        output_frame = tk.Frame(self.root, bg="#ECF0F1", padx=20, pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(output_frame, text="Translation Output:", bg="#ECF0F1", font=("Arial", 11, "bold")).pack(anchor="w")
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#FFFFFF",
            fg="#2C3E50",
            height=15
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Clear button
        clear_btn = tk.Button(
            output_frame,
            text="Clear Output",
            command=self.clear_output,
            bg="#95A5A6",
            fg="white",
            cursor="hand2"
        )
        clear_btn.pack(pady=5)
        
        # Footer
        footer = tk.Label(
            self.root,
            text="💡 Tip: Speak clearly and wait for the translation to complete",
            bg="#34495E",
            fg="white",
            pady=10,
            font=("Arial", 9)
        )
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
    def get_language_code(self, selection):
        """Extract language code from selection"""
        return selection.split('(')[1].rstrip(')')
    
    def log_message(self, message, tag="info"):
        """Add message to output area"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
    
    def update_status(self, message, color="#3498DB"):
        """Update status label"""
        self.status_label.config(text=message)
        self.root.update()
    
    def start_translation(self):
        """Start the translation process"""
        if self.is_running:
            return
        
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Get language codes
        source = self.get_language_code(self.source_lang.get())
        target = self.get_language_code(self.target_lang.get())
        
        self.log_message("\n" + "="*60)
        self.log_message(f"🎤 Started: {source.upper()} → {target.upper()}")
        self.log_message("="*60 + "\n")
        
        # Start listening thread
        listen_thread = threading.Thread(
            target=self.listen_and_translate,
            args=(source, target),
            daemon=True
        )
        listen_thread.start()
    
    def stop_translation(self):
        """Stop the translation process"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("⚪ Stopped")
        self.log_message("\n🛑 Translation stopped\n")
    
    def listen_and_translate(self, source_lang, target_lang):
        """Listen and translate in a loop"""
        
        try:
            # Initialize microphone
            self.microphone = sr.Microphone()
            
            with self.microphone as source:
                # Calibrate
                self.update_status("🎧 Calibrating microphone...")
                self.log_message("🎧 Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                self.log_message("✅ Calibration complete!\n")
                
                while self.is_running:
                    try:
                        # Listen
                        self.update_status("🎤 Listening... Speak now!")
                        self.log_message("🎤 Listening...")
                        
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)
                        
                        self.update_status("🧠 Recognizing...")
                        self.log_message("🧠 Recognizing speech...")
                        
                        # Recognize
                        text = self.recognizer.recognize_google(audio, language=source_lang)
                        self.log_message(f"📄 You said: '{text}'")
                        
                        # Translate
                        self.update_status("🌍 Translating...")
                        self.log_message(f"🌍 Translating...")
                        
                        translation = self.translator.translate(text, src=source_lang, dest=target_lang)
                        translated_text = translation.text
                        self.log_message(f"✅ Translation: '{translated_text}'")
                        
                        # Speak
                        self.update_status("🔊 Speaking...")
                        self.log_message("🔊 Speaking translation...")
                        
                        tts = gTTS(text=translated_text, lang=target_lang, slow=False)
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                            temp_file = fp.name
                            tts.save(temp_file)
                        
                        pygame.mixer.music.load(temp_file)
                        pygame.mixer.music.play()
                        
                        while pygame.mixer.music.get_busy():
                            if not self.is_running:
                                pygame.mixer.music.stop()
                                break
                        
                        pygame.mixer.music.unload()
                        os.unlink(temp_file)
                        
                        self.log_message("✅ Done!\n")
                        self.update_status("🎤 Ready - Speak again!")
                        
                    except sr.WaitTimeoutError:
                        self.update_status("⏳ Waiting for speech...")
                        continue
                    except sr.UnknownValueError:
                        self.log_message("⚠️  Could not understand audio\n")
                        self.update_status("⚠️  Couldn't understand - Try again")
                    except Exception as e:
                        self.log_message(f"❌ Error: {e}\n")
                        self.update_status("❌ Error occurred")
                        
        except Exception as e:
            self.log_message(f"❌ Fatal error: {e}\n")
            self.update_status("❌ Fatal error")
            self.stop_translation()
    
    def process_queue(self):
        """Process messages from queue"""
        while True:
            try:
                message = self.text_queue.get(timeout=0.1)
                self.log_message(message)
            except queue.Empty:
                pass


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = TranslatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
