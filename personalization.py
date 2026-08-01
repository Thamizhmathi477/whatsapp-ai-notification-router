import pandas as pd


class Personalization:

    def __init__(self,
                 users,
                 group_members,
                 business_accounts,
                 user_business_history):

        self.users = users
        self.group_members = group_members
        self.business_accounts = business_accounts
        self.user_business_history = user_business_history

        self.trusted_users = set()
        self.muted_groups = set()
        self.trusted_businesses = set()
        self.opted_in = set()

        self._build_indexes()

    def _build_indexes(self):

        # -----------------------------
        # Trusted Users
        # -----------------------------
        if not self.users.empty:

            for _, row in self.users.iterrows():

                opens = row.get("recent_opens", 0)
                replies = row.get("recent_replies", 0)
                dismissals = row.get("recent_dismissals", 0)

                score = opens + replies - dismissals

                if score >= 10:
                    self.trusted_users.add(row["user_id"])

        # -----------------------------
        # Muted Groups
        # -----------------------------
        if not self.group_members.empty:

            for _, row in self.group_members.iterrows():

                muted = row.get("group_muted_by_user", False)

                if muted in [True, 1, "true", "TRUE"]:
                    self.muted_groups.add(row["group_id"])

        # -----------------------------
        # Trusted Businesses
        # -----------------------------
        if not self.business_accounts.empty:

            for _, row in self.business_accounts.iterrows():

                verified = row.get("verified", False)
                reports = row.get("user_reports_30d", 999)

                if verified and reports < 5:
                    self.trusted_businesses.add(row["business_id"])

        # -----------------------------
        # Opted-in Businesses
        # -----------------------------
        if not self.user_business_history.empty:

            for _, row in self.user_business_history.iterrows():

                if row.get("opt_in", False):

                    self.opted_in.add(

                        (
                            row["user_id"],
                            row["business_id"]
                        )

                    )

    # ----------------------------------
    # Trusted User
    # ----------------------------------

    def is_trusted_user(self, user_id):

        if pd.isna(user_id):
            return False

        return user_id in self.trusted_users

    # ----------------------------------
    # Muted Group
    # ----------------------------------

    def is_muted_group(self, group_id):

        if pd.isna(group_id):
            return False

        return group_id in self.muted_groups

    # ----------------------------------
    # Trusted Business
    # ----------------------------------

    def is_trusted_business(self, business_id):

        if pd.isna(business_id):
            return False

        return business_id in self.trusted_businesses

    # ----------------------------------
    # Business Opt-in
    # ----------------------------------

    def is_opted_in(self,
                    user_id,
                    business_id):

        return (user_id, business_id) in self.opted_in

    # ----------------------------------
    # User Engagement Score
    # ----------------------------------

    def get_open_rate(self,
                      user_id):

        if self.users.empty:
            return 0

        row = self.users[
            self.users["user_id"] == user_id
        ]

        if row.empty:
            return 0

        return int(
            row.iloc[0].get("recent_opens", 0)
        )
