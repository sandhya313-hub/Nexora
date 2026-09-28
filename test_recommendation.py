from services.competency_engine import (
    analyze_skill_gaps,
    get_priority_gaps
)

from services.recommendation_engine import (
    RecommendationEngine
)


# --------------------------------
# DEMO USER
# --------------------------------

user_skills = {

    "Statistics": 2,

    "Python": 2,

    "SQL": 1,

    "GIS": 1,

    "AI and Machine Learning": 1,

    "Data Visualization": 2,

    "Survey Design": 2,

    "Sampling": 2
}


# --------------------------------
# FIND SKILL GAPS
# --------------------------------

gap_df = analyze_skill_gaps(
    "Statistical Officer",
    user_skills
)


priority_gaps = get_priority_gaps(
    gap_df
)


print("\n===================================")
print("       NEXORA SKILL GAPS")
print("===================================\n")

print(
    priority_gaps[
        [
            "competency",
            "current_level",
            "required_level",
            "gap",
            "status"
        ]
    ].to_string(index=False)
)


# --------------------------------
# LOAD RECOMMENDATION ENGINE
# --------------------------------

engine = RecommendationEngine()


# --------------------------------
# GENERATE RECOMMENDATIONS
# --------------------------------

recommendations = engine.recommend_for_gaps(
    priority_gaps,
    top_k_per_skill=2
)


print("\n===================================")
print("       NEXORA RECOMMENDATIONS")
print("===================================\n")


if recommendations.empty:

    print("No recommendations found.")

else:

    print(
        recommendations[
            [
                "skill",
                "course_name",
                "level",
                "duration_hours",
                "match_score"
            ]
        ].to_string(index=False)
    )