from services.competency_engine import (
    analyze_skill_gaps,
    get_priority_gaps,
    calculate_competency_score
)


user_skills = {
    "Survey Design": 2,
    "Sampling": 2,
    "Python": 2,
    "SQL": 1,
    "Data Visualization": 2,
    "GIS": 1,
    "AI and Machine Learning": 1,
    "Statistics": 3
}


result = analyze_skill_gaps(
    "Statistical Officer",
    user_skills
)

score = calculate_competency_score(result)

print("\n=== NEXORA COMPETENCY ANALYSIS ===\n")

print(result.to_string(index=False))

print(f"\nOverall Competency Score: {score}%")

print("\n=== PRIORITY SKILL GAPS ===\n")

priority_gaps = get_priority_gaps(result)

print(priority_gaps.to_string(index=False))