import pandas as pd

from text_classifier import TextClassifier
from personalization import Personalization
from history_search import HistorySearch
from confidence import ConfidenceCalculator


class MessageRouter:

    def __init__(self, data):

        self.data = data
        self.messages = data["messages"]

        self.text_classifier = TextClassifier()

        self.personalization = Personalization(
            data["users"],
            data["group_members"],
            data["business_accounts"],
            data["user_business_history"]
        )

        self.history_search = HistorySearch(
            data["message_history"],
            data["message_events"]
        )

        self.confidence = ConfidenceCalculator()

    def process_messages(self):

        predictions = []

        for _, row in self.messages.iterrows():

            decision = self.route_message(row)

            predictions.append({

                "message_id": row["message_id"],
                "action": decision["action"],
                "message_type": decision["message_type"],
                "reason": decision["reason"],
                "confidence": decision["confidence"],
                "evidence_message_ids": decision["evidence_message_ids"]

            })

        return pd.DataFrame(predictions)

    def route_message(self, row):

        text = str(row.get("message_text", ""))

        # -----------------------------
        # Classify Text
        # -----------------------------
        message_type = self.text_classifier.classify(text)

        # -----------------------------
        # Find Evidence
        # -----------------------------
        evidence = self.history_search.find_evidence(
            row["user_id"],
            text
        )

        # -----------------------------
        # Personalization
        # -----------------------------
        trusted_sender = self.personalization.is_trusted_user(
            row.get("sender_user_id")
        )

        trusted_business = self.personalization.is_trusted_business(
            row.get("business_id")
        )

        muted_group = self.personalization.is_muted_group(
            row.get("group_id")
        )

        # -----------------------------
        # Routing Decision
        # -----------------------------

        action = "digest"

        if message_type == "scam":

            action = "mute"

        elif message_type == "spam":

            action = "mute"

        elif message_type == "urgent":

            action = "notify"

        elif trusted_sender:

            action = "notify"

        elif trusted_business:

            action = "digest"

        elif muted_group:

            action = "mute"

        elif row.get("forwarded_count", 0) >= 5:

            action = "mute"

        # -----------------------------
        # Confidence
        # -----------------------------

        confidence = self.confidence.calculate(

            action=action,

            evidence_count=len(evidence),

            trusted_sender=trusted_sender,

            trusted_business=trusted_business,

            forwarded=row.get("forwarded_count", 0)

        )

        # -----------------------------
        # Reason
        # -----------------------------

        if action == "notify":

            reason = "High priority message."

        elif action == "mute":

            reason = "Low value or suspicious."

        else:

            reason = "Useful but not urgent."

        # -----------------------------
        # Evidence IDs
        # -----------------------------

        evidence_ids = "none"

        if len(evidence) > 0:

            evidence_ids = ";".join(
                [str(i) for i in evidence[:3]]
            )

        return {

            "action": action,

            "message_type": message_type,

            "reason": reason,

            "confidence": round(confidence, 2),

            "evidence_message_ids": evidence_ids

        }
