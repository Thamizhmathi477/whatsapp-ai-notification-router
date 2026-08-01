"""
evaluation.py
Evaluate Notification Router Predictions
"""

import pandas as pd


class Evaluator:

    def __init__(self, sample_file="dataset/sample_messages.csv"):

        self.sample_file = sample_file

        try:
            self.sample = pd.read_csv(sample_file)
        except Exception:
            self.sample = pd.DataFrame()

    def evaluate(self, predictions):

        if self.sample.empty:

            print("❌ sample_messages.csv not found")
            return

        required = [
            "message_id",
            "action",
            "message_type"
        ]

        for col in required:

            if col not in predictions.columns:

                print(f"Missing column: {col}")
                return

        merged = self.sample.merge(
            predictions,
            on="message_id",
            suffixes=("_true", "_pred")
        )

        if merged.empty:

            print("No matching message IDs.")
            return

        # -----------------------------
        # Action Accuracy
        # -----------------------------
        action_acc = (
            merged["action_true"] ==
            merged["action_pred"]
        ).mean()

        # -----------------------------
        # Message Type Accuracy
        # -----------------------------
        type_acc = (
            merged["message_type_true"] ==
            merged["message_type_pred"]
        ).mean()

        # -----------------------------
        # Overall Accuracy
        # -----------------------------
        overall = (
            (
                merged["action_true"] ==
                merged["action_pred"]
            )
            &
            (
                merged["message_type_true"] ==
                merged["message_type_pred"]
            )
        ).mean()

        print("=" * 50)
        print("Evaluation Results")
        print("=" * 50)

        print(f"Messages Evaluated : {len(merged)}")
        print(f"Action Accuracy    : {action_acc:.2%}")
        print(f"Type Accuracy      : {type_acc:.2%}")
        print(f"Overall Accuracy   : {overall:.2%}")

        print("=" * 50)

        incorrect = merged[
            (
                merged["action_true"] !=
                merged["action_pred"]
            )
            |
            (
                merged["message_type_true"] !=
                merged["message_type_pred"]
            )
        ]

        if not incorrect.empty:

            print("\nIncorrect Predictions\n")

            cols = [
                "message_id",
                "action_true",
                "action_pred",
                "message_type_true",
                "message_type_pred"
            ]

            print(incorrect[cols])

        else:

            print("\n🎉 Perfect Match!")

    def summary(self):

        if self.sample.empty:
            return

        print("\nSample Dataset Summary\n")

        print(
            self.sample["action"].value_counts()
        )

        print()

        print(
            self.sample["message_type"].value_counts()
        )
