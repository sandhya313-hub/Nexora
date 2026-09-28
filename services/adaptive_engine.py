class AdaptiveCompetencyEngine:
    """
    Updates learner competency based on assessment performance.
    Prototype implementation for Nexora.
    """

    def __init__(self):
        self.level_names = {
            1: "Beginner",
            2: "Intermediate",
            3: "Advanced"
        }

    def calculate_new_level(
        self,
        current_level,
        score
    ):
        """
        Determine updated competency level
        using assessment score.
        """

        if score >= 80:

            new_level = min(
                current_level + 1,
                3
            )

        elif score < 50:

            new_level = max(
                current_level - 1,
                1
            )

        else:

            new_level = current_level

        return new_level

    def get_level_name(
        self,
        level
    ):
        return self.level_names.get(
            level,
            "Unknown"
        )

    def update_competency(
        self,
        competency,
        current_level,
        score
    ):
        """
        Update one competency based on assessment score.
        """

        new_level = self.calculate_new_level(
            current_level,
            score
        )

        old_name = self.get_level_name(
            current_level
        )

        new_name = self.get_level_name(
            new_level
        )

        if new_level > current_level:

            message = (
                f"Excellent performance! "
                f"{competency} has progressed from "
                f"{old_name} to {new_name}."
            )

        elif new_level < current_level:

            message = (
                f"{competency} needs additional practice. "
                f"The competency level has been adjusted "
                f"from {old_name} to {new_name}."
            )

        else:

            message = (
                f"{competency} remains at the "
                f"{old_name} level."
            )

        return {
            "competency": competency,
            "old_level": current_level,
            "new_level": new_level,
            "old_level_name": old_name,
            "new_level_name": new_name,
            "score": score,
            "message": message
        }