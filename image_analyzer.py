import os
import pandas as pd

try:
    import easyocr
except ImportError:
    easyocr = None


class ImageAnalyzer:

    def __init__(self, images_df, dataset_path="dataset"):

        self.images = images_df
        self.dataset_path = dataset_path

        if easyocr is not None:
            self.reader = easyocr.Reader(['en'], gpu=False)
        else:
            self.reader = None

    def get_image_path(self, media_id):

        if self.images.empty:
            return None

        row = self.images[
            self.images["media_id"] == media_id
        ]

        if row.empty:
            return None

        relative_path = row.iloc[0]["file_path"]

        return os.path.join(
            self.dataset_path,
            relative_path
        )

    def extract_text(self, image_path):

        if self.reader is None:
            return ""

        if image_path is None:
            return ""

        if not os.path.exists(image_path):
            return ""

        try:

            result = self.reader.readtext(
                image_path,
                detail=0
            )

            return " ".join(result).lower()

        except Exception:
            return ""

    def analyze(self, media_id):

        image_path = self.get_image_path(media_id)

        text = self.extract_text(image_path)

        if text == "":

            return {
                "action": "digest",
                "message_type": "unknown",
                "reason": "Unable to read image",
                "confidence": 0.50
            }

        if any(word in text for word in
               ["urgent", "emergency", "hospital", "blood"]):

            return {
                "action": "notify",
                "message_type": "urgent",
                "reason": "Urgent information detected in image",
                "confidence": 0.95
            }

        if any(word in text for word in
               ["offer", "sale", "discount", "buy"]):

            return {
                "action": "digest",
                "message_type": "promotion",
                "reason": "Promotional poster detected",
                "confidence": 0.85
            }

        if any(word in text for word in
               ["meeting", "event", "seminar", "workshop"]):

            return {
                "action": "digest",
                "message_type": "event",
                "reason": "Event poster detected",
                "confidence": 0.88
            }

        if any(word in text for word in
               ["otp", "password", "bank", "verify", "click"]):

            return {
                "action": "mute",
                "message_type": "scam",
                "reason": "Possible scam poster",
                "confidence": 0.95
            }

        return {
            "action": "digest",
            "message_type": "personal",
            "reason": "General image message",
            "confidence": 0.70
        }
