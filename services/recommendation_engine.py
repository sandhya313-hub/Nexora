import pandas as pd
import numpy as np

from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent
COURSE_FILE = BASE_DIR / "data" / "courses.csv"


class RecommendationEngine:

    def __init__(self):

        print("Loading Nexora recommendation model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.courses = pd.read_csv(
            COURSE_FILE
        )

        # Text used for semantic understanding
        self.courses["search_text"] = (
            self.courses["course_name"].fillna("")
            + ". "
            + self.courses["domain"].fillna("")
            + ". Skills: "
            + self.courses["skills"].fillna("")
            + ". "
            + self.courses["description"].fillna("")
        )

        print("Creating course embeddings...")

        self.course_embeddings = self.model.encode(
            self.courses["search_text"].tolist(),
            normalize_embeddings=True
        )

        print("Recommendation engine ready!")


    def calculate_level_score(
        self,
        course_level,
        current_level,
        required_level
    ):
        """
        Determine how appropriate the course level is
        for the learner's current competency.
        """

        level_map = {
            "Beginner": 1,
            "Intermediate": 2,
            "Advanced": 3
        }

        course_level_value = level_map.get(
            course_level,
            2
        )

        # Prefer courses slightly above current level
        target_level = min(
            current_level + 1,
            required_level
        )

        difference = abs(
            course_level_value - target_level
        )

        if difference == 0:
            return 1.0

        if difference == 1:
            return 0.75

        return 0.5


    def recommend_for_skill(
        self,
        skill,
        current_level,
        required_level,
        top_k=3
    ):

        gap = max(
            required_level - current_level,
            0
        )

        # ----------------------------------------
        # Semantic query
        # ----------------------------------------

        query = (
            f"Learning {skill}. "
            f"Training for {skill}. "
            f"Developing competency in {skill}. "
            f"Current level {current_level}. "
            f"Required level {required_level}."
        )

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        semantic_scores = cosine_similarity(
            query_embedding,
            self.course_embeddings
        )[0]


        results = self.courses.copy()

        results["semantic_score"] = semantic_scores


        # ----------------------------------------
        # Explicit skill matching
        # ----------------------------------------

        def skill_match(course_skills):

            available_skills = [
                s.strip().lower()
                for s in str(course_skills).split("|")
            ]

            return (
                1.0
                if skill.lower() in available_skills
                else 0.0
            )


        results["skill_match"] = (
            results["skills"]
            .apply(skill_match)
        )


        # ----------------------------------------
        # Level relevance
        # ----------------------------------------

        results["level_score"] = results.apply(
            lambda row: self.calculate_level_score(
                row["level"],
                current_level,
                required_level
            ),
            axis=1
        )


        # ----------------------------------------
        # Hybrid recommendation score
        # ----------------------------------------

        results["final_score"] = (

            results["semantic_score"] * 0.35

            + results["skill_match"] * 0.45

            + results["level_score"] * 0.20

        )


        # ----------------------------------------
        # Prioritize courses explicitly
        # associated with the skill
        # ----------------------------------------

        results = results.sort_values(
            by=[
                "skill_match",
                "final_score"
            ],
            ascending=False
        )


        return results.head(top_k)


    def recommend_for_gaps(
        self,
        gap_df,
        top_k_per_skill=2
    ):

        recommendations = []


        for _, row in gap_df.iterrows():

            if row["gap"] <= 0:
                continue


            skill = row["competency"]


            results = self.recommend_for_skill(

                skill=skill,

                current_level=row["current_level"],

                required_level=row["required_level"],

                top_k=top_k_per_skill

            )


            for _, course in results.iterrows():

                recommendations.append({

                    "skill": skill,

                    "course_id":
                        course["course_id"],

                    "course_name":
                        course["course_name"],

                    "domain":
                        course["domain"],

                    "level":
                        course["level"],

                    "duration_hours":
                        course["duration_hours"],

                    "match_score":
                        round(
                            float(
                                course["final_score"]
                            ) * 100,
                            2
                        )

                })


        return pd.DataFrame(
            recommendations
        )