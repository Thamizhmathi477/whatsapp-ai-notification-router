import pandas as pd


class HistorySearch:

    def __init__(self, message_history, message_events):

        self.message_history = message_history
        self.message_events = message_events

    def find_evidence(self, user_id, message_text):
        """
        Find similar historical messages for the same user.
        Returns a list of message IDs.
        """

        if self.message_history.empty:
            return []

        if pd.isna(message_text):
            return []

        message_text = str(message_text).lower().strip()

        if message_text == "":
            return []

        evidence = []

        try:

            # Messages received by this user
            history = self.message_history[
                self.message_history["user_id"] == user_id
            ]

            for _, row in history.iterrows():

                old_text = str(
                    row.get("message_text", "")
                ).lower()

                if old_text == "":
                    continue

                # Very simple similarity:
                # If either text contains the other.
                if (
                    message_text in old_text
                    or old_text in message_text
                ):

                    evidence.append(
                        str(row["message_id"])
                    )

            # Remove duplicates
            evidence = list(dict.fromkeys(evidence))

            return evidence[:3]

        except Exception:

            return []

    def get_user_history(self, user_id):
        """
        Return all historical messages for a user.
        """

        if self.message_history.empty:
            return pd.DataFrame()

        return self.message_history[
            self.message_history["user_id"] == user_id
        ]

    def get_message_events(self, message_id):
        """
        Return events related to a historical message.
        """

        if self.message_events.empty:
            return pd.DataFrame()

        return self.message_events[
            self.message_events["message_id"] == message_id
        ]

    def was_opened(self, message_id):

        events = self.get_message_events(message_id)

        if events.empty:
            return False

        return (
            events["message_opened"] == 1
        ).any()

    def was_replied(self, message_id):

        events = self.get_message_events(message_id)

        if events.empty:
            return False

        return (
            events["message_replied"] == 1
        ).any()

    def was_reported(self, message_id):

        events = self.get_message_events(message_id)

        if events.empty:
            return False

        return (
            events["message_reported"] == 1
        ).any()
