class AnalyticsEngine:
    """
    Generates learner analytics for Nexora.
    """

    def __init__(self):
        self.assessment_scores = []
        self.learning_hours = 0.0

    # -------------------------------------------------
    # ADD ASSESSMENT SCORE
    # -------------------------------------------------

    def add_assessment_score(self, score):

        self.assessment_scores.append(
            float(score)
        )

    # -------------------------------------------------
    # ADD LEARNING HOURS
    # -------------------------------------------------

    def add_learning_hours(self, hours):

        self.learning_hours += float(hours)

    # -------------------------------------------------
    # AVERAGE ASSESSMENT SCORE
    # -------------------------------------------------

    def get_average_score(self):

        if not self.assessment_scores:

            return 0.0

        return round(
            sum(self.assessment_scores)
            / len(self.assessment_scores),
            2
        )

    # -------------------------------------------------
    # NUMBER OF ASSESSMENTS
    # -------------------------------------------------

    def get_assessment_count(self):

        return len(
            self.assessment_scores
        )

    # -------------------------------------------------
    # OVERALL COMPETENCY
    # -------------------------------------------------

    def calculate_overall_competency(
        self,
        competency_levels
    ):

        if not competency_levels:

            return 0.0

        total = sum(
            competency_levels.values()
        )

        maximum = (
            len(competency_levels) * 3
        )

        return round(
            (total / maximum) * 100,
            2
        )

    # -------------------------------------------------
    # COMPETENCY PERCENTAGES
    # -------------------------------------------------

    def competency_percentages(
        self,
        competency_levels
    ):

        percentages = {}

        for competency, level in (
            competency_levels.items()
        ):

            percentages[competency] = round(
                (level / 3) * 100,
                2
            )

        return percentages

    # -------------------------------------------------
    # LEARNING PROGRESS
    # -------------------------------------------------

    def calculate_learning_progress(
        self,
        competency_levels
    ):

        if not competency_levels:

            return 0.0

        total = sum(
            competency_levels.values()
        )

        maximum = (
            len(competency_levels) * 3
        )

        return round(
            (total / maximum) * 100,
            2
        )

    # -------------------------------------------------
    # COMPLETE ANALYTICS
    # -------------------------------------------------

    def generate_report(
        self,
        competency_levels,
        priority_gap_count
    ):

        overall_competency = (
            self.calculate_overall_competency(
                competency_levels
            )
        )

        competency_percentages = (
            self.competency_percentages(
                competency_levels
            )
        )

        learning_progress = (
            self.calculate_learning_progress(
                competency_levels
            )
        )

        return {

            "overall_competency":
                overall_competency,

            "assessment_count":
                self.get_assessment_count(),

            "average_assessment_score":
                self.get_average_score(),

            "skill_gaps":
                priority_gap_count,

            "learning_hours":
                round(
                    self.learning_hours,
                    1
                ),

            "learning_progress":
                learning_progress,

            "competency_percentages":
                competency_percentages
        }