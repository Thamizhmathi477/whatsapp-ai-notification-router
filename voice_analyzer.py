import os
import pandas as pd

try:
    import whisper
except ImportError:
    whisper = None


class VoiceAnalyzer:

    def __init__(self,
                 voice_notes_df,
                 text_classifier,
                 dataset_path="dataset"):

        self.voice_notes = voice_notes_df
        self.dataset_path = dataset_path
        self.text_classifier = text_classifier

        if whisper is not None:
            self.model = whisper.load_model("base")
        else:
            self.model = None

    def get_audio_path(self, media_id):

        if self.voice_notes.empty:
            return None

        row = self.voice_notes[
            self.voice_notes["media_id"] == media_id
        ]

        if row.empty:
            return None

        return os.path.join(
            self.dataset_path,
            row.iloc[0]["file_path"]
        )

    def transcribe(self, audio_path):

        if self.model is None:
            return ""

        if audio_path is None:
            return ""

        if not os.path.exists(audio_path):
            return ""

        try:

            result = self.model.transcribe(audio_path)

            return result["text"].lower()

        except Exception:

            return ""

    def analyze(self, media_id):

        audio_path = self.get_audio_path(media_id)

        transcript = self.transcribe(audio_path)

        if transcript == "":

            return {
                "action": "digest",
                "message_type": "unknown",
                "reason": "Unable to understand voice note",
                "confidence": 0.50
            }

        message_type = self.text_classifier.classify(transcript)

        if message_type == "urgent":

            return {
                "action": "notify",
                "message_type": "urgent",
                "reason": "Urgent voice note detected",
                "confidence": 0.95
            }

        elif message_type == "payment":

            return {
                "action": "notify",
                "message_type": "payment",
                "reason": "Payment-related voice note",
                "confidence": 0.90
            }

        elif message_type == "scam":

            return {
                "action": "mute",
                "message_type": "scam",
                "reason": "Possible scam in voice note",
                "confidence": 0.95
            }

        elif message_type == "promotion":

            return {
                "action": "digest",
                "message_type": "promotion",
                "reason": "Promotional voice message",
                "confidence": 0.80
            }

        return {
            "action": "digest",
            "message_type": "personal",
            "reason": "General voice message",
            "confidence": 0.75
        }
