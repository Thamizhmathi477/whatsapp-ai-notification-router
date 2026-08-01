import os
import pandas as pd


class DataLoader:
    """
    Loads all datasets required for the WhatsApp Notification Router.
    """

    def __init__(self, dataset_path="dataset"):
        self.dataset_path = dataset_path

    def load_csv(self, filename):
        """
        Load a CSV file from the dataset folder.
        """

        file_path = os.path.join(self.dataset_path, filename)

        if not os.path.exists(file_path):
            print(f"❌ Missing: {filename}")
            return pd.DataFrame()

        try:
            df = pd.read_csv(file_path)
            print(f"✅ {filename:<35} {len(df)} rows")
            return df

        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")
            return pd.DataFrame()

    def load_all(self):
        """
        Load every required dataset.
        """

        datasets = {}

        csv_files = {
            "messages": "messages.csv",
            "users": "users.csv",
            "groups": "groups.csv",
            "group_members": "group_members.csv",
            "business_accounts": "business_accounts.csv",
            "user_business_history": "user_business_history.csv",
            "message_history": "message_history.csv",
            "message_events": "message_events.csv",
            "images": "images.csv",
            "voice_notes": "voice_notes.csv",
            "daily_notification_summary": "daily_notification_summary.csv"
        }

        print("\n📂 Loading datasets...\n")

        for key, filename in csv_files.items():
            datasets[key] = self.load_csv(filename)

        print("\n🎉 Dataset loading complete.\n")

        return datasets
