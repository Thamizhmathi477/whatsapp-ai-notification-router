"""
main.py
WhatsApp AI Notification Router
HackerRank Orchestrate 2026
"""

import os
import logging
import pandas as pd

from data_loader import DataLoader
from router import MessageRouter


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def validate_dataset(dataset_path):
    """
    Check whether required dataset files exist.
    """

    required_files = [
        "messages.csv",
        "users.csv",
        "groups.csv",
        "group_members.csv",
        "business_accounts.csv",
        "user_business_history.csv",
        "message_history.csv",
        "message_events.csv",
        "images.csv",
        "voice_notes.csv",
        "daily_notification_summary.csv"
    ]

    missing = []

    for file in required_files:

        if not os.path.exists(os.path.join(dataset_path, file)):
            missing.append(file)

    return missing


def main():

    print("=" * 70)
    print("📱 WhatsApp AI Notification Router")
    print("HackerRank Orchestrate Challenge")
    print("=" * 70)

    dataset_path = "dataset"

    logging.info("Checking dataset...")

    missing = validate_dataset(dataset_path)

    if len(missing) > 0:

        print("\nMissing dataset files:")

        for f in missing:
            print("-", f)

        return

    logging.info("Loading datasets...")

    loader = DataLoader(dataset_path)

    data = loader.load_all()

    logging.info("Datasets loaded successfully")

    logging.info("Initializing AI Router...")

    router = MessageRouter(data)

    logging.info("Generating predictions...")

    output = router.process_messages()

    output_path = os.path.join(dataset_path, "output.csv")

    output.to_csv(output_path, index=False)

    logging.info("Predictions saved")

    print("\nPrediction Summary")
    print("-" * 40)

    print(output["action"].value_counts())

    print("\nMessage Types")
    print("-" * 40)

    print(output["message_type"].value_counts())

    print("\nOutput saved to:")
    print(output_path)

    print("\nFirst five predictions:\n")

    print(output.head())

    print("\nDone.")


if __name__ == "__main__":
    main()
