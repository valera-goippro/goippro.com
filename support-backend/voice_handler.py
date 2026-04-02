"""GoIPPro Voice Support Handler
STT (Groq Whisper) → LLM (Claude) → TTS (OpenAI)
Auto-detects language from speech.
"""
import io
import os
import logging
import tempfile
from groq import Groq
from openai import OpenAI

logger = logging.getLogger("goippro-voice")

# TTS voice map — best voices per language
VOICE_MAP = {
    "en": "nova",
    "ru": "nova",
    "pt": "nova",
    "es": "nova",
    "ar": "nova",
    "tr": "nova",
    "fr": "nova",
    "zh": "nova",
    "ko": "nova",
    "fa": "nova",
    "ur": "nova",
    "de": "nova",
    "it": "nova",
    "hi": "nova",
}

# Language name map for system prompt context
LANG_NAMES = {
    "en": "English", "ru": "Russian", "pt": "Portuguese", "es": "Spanish",
    "ar": "Arabic", "tr": "Turkish", "fr": "French", "zh": "Chinese",
    "ko": "Korean", "fa": "Persian", "ur": "Urdu", "de": "German",
    "it": "Italian", "hi": "Hindi", "ja": "Japanese", "nl": "Dutch",
    "pl": "Polish", "vi": "Vietnamese", "th": "Thai", "id": "Indonesian",
}


class VoiceHandler:
    def __init__(self):
        self.groq = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        logger.info("VoiceHandler initialized (Groq STT + OpenAI TTS)")

    def speech_to_text(self, audio_bytes: bytes, filename: str = "audio.webm") -> dict:
        """Transcribe audio with Groq Whisper. Returns {text, language}."""
        try:
            # Write to temp file (Groq needs a file-like with name)
            suffix = "." + filename.rsplit(".", 1)[-1] if "." in filename else ".webm"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name

            with open(tmp_path, "rb") as audio_file:
                transcription = self.groq.audio.transcriptions.create(
                    model="whisper-large-v3-turbo",
                    file=audio_file,
                    response_format="verbose_json",
                )

            os.unlink(tmp_path)

            text = transcription.text.strip()
            language = getattr(transcription, "language", "en") or "en"

            # Normalize language code to 2-letter lowercase
            language = language.strip().lower()[:2]

            logger.info(f"STT: [{language}] {text[:80]}...")
            return {"text": text, "language": language}

        except Exception as e:
            logger.error(f"STT error: {e}")
            if 'tmp_path' in locals():
                try: os.unlink(tmp_path)
                except: pass
            raise

    def text_to_speech(self, text: str, language: str = "en") -> bytes:
        """Convert text to speech with OpenAI TTS. Returns MP3 bytes."""
        voice = VOICE_MAP.get(language, "nova")
        try:
            response = self.openai.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                response_format="mp3",
            )
            audio_bytes = response.content
            logger.info(f"TTS: {len(audio_bytes)} bytes, voice={voice}, lang={language}")
            return audio_bytes

        except Exception as e:
            logger.error(f"TTS error: {e}")
            raise
