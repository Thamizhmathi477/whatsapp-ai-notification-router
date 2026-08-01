import re


class TextClassifier:

    def __init__(self):

        self.urgent_keywords = {
            "urgent", "emergency", "help", "hospital",
            "accident", "ambulance", "blood",
            "asap", "immediately", "critical"
        }

        self.payment_keywords = {
            "payment", "paid", "invoice", "bill",
            "upi", "bank", "transaction",
            "salary", "refund"
        }

        self.promotion_keywords = {
            "offer", "sale", "discount",
            "cashback", "coupon", "deal",
            "buy now", "limited time"
        }

        self.greeting_keywords = {
            "hi", "hello", "hey",
            "good morning", "good evening",
            "good night"
        }

        self.scam_keywords = {
            "otp", "password", "verify",
            "click here", "lottery",
            "won", "claim prize",
            "free money", "loan approved",
            "kyc", "account blocked"
        }

        self.event_keywords = {
            "meeting", "seminar", "conference",
            "birthday", "wedding", "invitation",
            "event", "function"
        }

        self.business_keywords = {
            "order", "delivery", "shipment",
            "tracking", "booking",
            "confirmed", "dispatched"
        }

    def preprocess(self, text):

        if text is None:
            return ""

        text = str(text).lower()
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def contains(self, text, keywords):

        return any(keyword in text for keyword in keywords)

    def classify(self, text):

        text = self.preprocess(text)

        if text == "":
            return "unknown"

        if self.contains(text, self.scam_keywords):
            return "scam"

        if self.contains(text, self.urgent_keywords):
            return "urgent"

        if self.contains(text, self.payment_keywords):
            return "payment"

        if self.contains(text, self.business_keywords):
            return "business_update"

        if self.contains(text, self.promotion_keywords):
            return "promotion"

        if self.contains(text, self.event_keywords):
            return "event"

        if self.contains(text, self.greeting_keywords):
            return "greeting"

        if text.startswith("fwd") or text.startswith("fw:"):
            return "forward"

        return "personal"

    def is_scam(self, text):
        return self.classify(text) == "scam"

    def is_urgent(self, text):
        return self.classify(text) == "urgent"

    def is_payment(self, text):
        return self.classify(text) == "payment"

    def is_promotion(self, text):
        return self.classify(text) == "promotion"

    def is_event(self, text):
        return self.classify(text) == "event"

    def is_greeting(self, text):
        return self.classify(text) == "greeting"

    def is_forwarded(self, forwarded_count):
        return forwarded_count >= 3

    def is_mentioned(self, text, user_id):
        text = self.preprocess(text)
        return f"@{user_id}" in text
