class ConfidenceCalculator:
    """
    Calculates confidence score for routing decisions.
    Final confidence is always between 0.30 and 0.99.
    """

    def __init__(self):
        self.base_scores = {
            "notify": 0.75,
            "digest": 0.65,
            "mute": 0.80
        }

    def calculate(
        self,
        action,
        evidence_count=0,
        trusted_sender=False,
        trusted_business=False,
        forwarded=0
    ):
        """
        Parameters
        ----------
        action : str
            notify / digest / mute

        evidence_count : int
            Number of similar historical messages

        trusted_sender : bool

        trusted_business : bool

        forwarded : int
            Forward count of message
        """

        score = self.base_scores.get(action, 0.50)

        # Historical evidence increases confidence
        score += min(evidence_count * 0.03, 0.12)

        # Trusted sender
        if trusted_sender:
            score += 0.08

        # Trusted business
        if trusted_business:
            score += 0.05

        # Highly forwarded messages are more suspicious
        if forwarded >= 5:
            score += 0.04

        # Keep score within range
        score = max(0.30, min(score, 0.99))

        return round(score, 2)

    def explain(
        self,
        action,
        confidence
    ):
        """
        Optional helper for debugging.
        """

        if confidence >= 0.90:
            return "Very High"

        elif confidence >= 0.75:
            return "High"

        elif confidence >= 0.60:
            return "Medium"

        return "Low"
