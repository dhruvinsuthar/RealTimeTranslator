"""
Configuration file for Real-time Speech Translator
Modify these settings to change languages and behavior
"""

# ==================== LANGUAGE SETTINGS ====================

# Language codes reference:
LANGUAGE_CODES = {
    'english': 'en',
    'spanish': 'es',
    'french': 'fr',
    'german': 'de',
    'italian': 'it',
    'portuguese': 'pt',
    'russian': 'ru',
    'japanese': 'ja',
    'korean': 'ko',
    'chinese_simplified': 'zh-CN',
    'chinese_traditional': 'zh-TW',
    'arabic': 'ar',
    'hindi': 'hi',
    'bengali': 'bn',
    'dutch': 'nl',
    'turkish': 'tr',
    'vietnamese': 'vi',
    'thai': 'th',
    'polish': 'pl',
    'swedish': 'sv',
    'norwegian': 'no',
    'danish': 'da',
    'finnish': 'fi',
    'greek': 'el',
    'hebrew': 'he',
    'indonesian': 'id',
    'malay': 'ms',
    'filipino': 'fil',
    'urdu': 'ur',
    'persian': 'fa',
    'ukrainian': 'uk',
    'czech': 'cs',
    'romanian': 'ro',
    'hungarian': 'hu',
}

# ==================== DEFAULT CONFIGURATION ====================

class TranslatorConfig:
    """Configuration for the translator"""
    
    # Primary language settings
    SOURCE_LANGUAGE = 'en'      # Your spoken language
    TARGET_LANGUAGE = 'es'      # Language to translate to
    
    # Audio processing settings
    CHUNK_DURATION = 3          # Seconds of audio per chunk (2-5 recommended)
    PHRASE_TIME_LIMIT = 5       # Max seconds for a phrase
    PAUSE_THRESHOLD = 0.8       # Seconds of silence to detect end of phrase
    
    # Recognition settings
    ENERGY_THRESHOLD = 300      # Minimum audio energy to start recording
    DYNAMIC_ENERGY = True       # Automatically adjust energy threshold
    
    # Speech settings
    SPEECH_SPEED = False        # False = normal speed, True = slower
    
    # System settings
    TIMEOUT = 1                 # Seconds to wait for speech before giving up
    CALIBRATION_DURATION = 2    # Seconds to calibrate for ambient noise
    
    # Display settings
    SHOW_TIMESTAMPS = True      # Show timestamps in output
    VERBOSE = True              # Show detailed processing info


# ==================== PRESET CONFIGURATIONS ====================

class PresetConfigs:
    """Pre-configured setups for common use cases"""
    
    # English to Spanish
    EN_TO_ES = {
        'source_lang': 'en',
        'target_lang': 'es',
        'chunk_duration': 3
    }
    
    # Spanish to English
    ES_TO_EN = {
        'source_lang': 'es',
        'target_lang': 'en',
        'chunk_duration': 3
    }
    
    # English to French
    EN_TO_FR = {
        'source_lang': 'en',
        'target_lang': 'fr',
        'chunk_duration': 3
    }
    
    # English to Chinese (Simplified)
    EN_TO_ZH = {
        'source_lang': 'en',
        'target_lang': 'zh-CN',
        'chunk_duration': 3
    }
    
    # English to Japanese
    EN_TO_JA = {
        'source_lang': 'en',
        'target_lang': 'ja',
        'chunk_duration': 3
    }
    
    # English to Hindi
    EN_TO_HI = {
        'source_lang': 'en',
        'target_lang': 'hi',
        'chunk_duration': 3
    }
    
    # English to Arabic
    EN_TO_AR = {
        'source_lang': 'en',
        'target_lang': 'ar',
        'chunk_duration': 3
    }


# ==================== ADVANCED SETTINGS ====================

class AdvancedConfig:
    """Advanced configuration options"""
    
    # Queue settings
    MAX_QUEUE_SIZE = 10         # Maximum items in processing queue
    QUEUE_TIMEOUT = 1           # Seconds to wait for queue items
    
    # Thread settings
    THREAD_PRIORITY = 'normal'  # Thread priority level
    
    # Error handling
    MAX_RETRIES = 3             # Max retries for failed operations
    RETRY_DELAY = 1             # Seconds between retries
    
    # Performance
    ENABLE_CACHING = True       # Cache translations for repeated phrases
    CACHE_SIZE = 100            # Number of translations to cache
    
    # Audio quality
    SAMPLE_RATE = 16000         # Audio sample rate (Hz)
    CHUNK_SIZE = 1024           # Audio buffer size
