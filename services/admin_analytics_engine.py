import pandas as pd


class AdminAnalyticsEngine:

    def __init__(self):

        # Demo workforce dataset
        # In the production system this would come
        # from the organization's learner database.

        self.learners = pd.DataFrame([

            {
                "name": "Learner 1",
                "role": "Statistical Officer",
                "statistics": 2,
                "python": 2,
                "sql": 1,
                "gis": 1,
                "ai_ml": 1,
                "assessment_score": 72
            },

            {
                "name": "Learner 2",
                "role": "Data Analyst",
                "statistics": 3,
                "python": 2,
                "sql": 2,
                "gis": 1,
                "ai_ml": 2,
                "assessment_score": 81
            },

            {
                "name": "Learner 3",
                "role": "GIS Analyst",
                "statistics": 2,
                "python": 1,
                "sql": 1,
                "gis": 3,
                "ai_ml": 1,
                "assessment_score": 68
            },

            {
                "name": "Learner 4",
                "role": "AI/ML Specialist",
                "statistics": 2,
                "python": 3,
                "sql": 2,
                "gis": 1,
                "ai_ml": 3,
                "assessment_score": 91
            },

            {
                "name": "Learner 5",
                "role": "Data Analyst",
                "statistics": 2,
                "python": 2,
                "sql": 3,
                "gis": 1,
                "ai_ml": 2,
                "assessment_score": 78
            }

        ])


    def get_workforce_data(self):

        return self.learners.copy()


    def calculate_average_competency(self):

        skills = [
            "statistics",
            "python",
            "sql",
            "gis",
            "ai_ml"
        ]

        total = 0
        count = 0

        for skill in skills:

            total += self.learners[skill].mean()

            count += 1

        average_level = total / count

        percentage = (
            average_level / 3
        ) * 100

        return round(
            percentage,
            1
        )


    def calculate_average_assessment(self):

        return round(
            self.learners[
                "assessment_score"
            ].mean(),
            1
        )


    def calculate_skill_distribution(self):

        skills = {

            "Statistics": "statistics",

            "Python": "python",

            "SQL": "sql",

            "GIS": "gis",

            "AI and Machine Learning": "ai_ml"

        }

        result = {}

        for display_name, column in skills.items():

            average = self.learners[
                column
            ].mean()

            percentage = (
                average / 3
            ) * 100

            result[
                display_name
            ] = round(
                percentage,
                1
            )

        return result


    def identify_priority_skills(self):

        distribution = (
            self.calculate_skill_distribution()
        )

        priority_skills = []

        for skill, percentage in distribution.items():

            if percentage < 70:

                priority_skills.append(
                    skill
                )

        return priority_skills


    def generate_report(self):

        return {

            "total_learners":
                len(self.learners),

            "average_competency":
                self.calculate_average_competency(),

            "average_assessment":
                self.calculate_average_assessment(),

            "skill_distribution":
                self.calculate_skill_distribution(),

            "priority_skills":
                self.identify_priority_skills()
        }