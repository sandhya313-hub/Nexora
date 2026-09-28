from services.analytics_engine import (
    AnalyticsEngine
)


engine = AnalyticsEngine()


competencies = {

    "Statistics": 2,

    "Python": 3,

    "SQL": 1,

    "GIS": 2,

    "AI and Machine Learning": 2,

    "Data Visualization": 3,

    "Survey Design": 2,

    "Sampling": 2
}


engine.add_assessment_score(85)

engine.add_assessment_score(75)

engine.add_learning_hours(12.5)


report = engine.generate_report(
    competency_levels=competencies,
    priority_gap_count=3
)


print()
print("==============================")
print("NEXORA ANALYTICS")
print("==============================")
print()

print(
    "Overall Competency:",
    report["overall_competency"],
    "%"
)

print(
    "Assessments:",
    report["assessment_count"]
)

print(
    "Average Assessment Score:",
    report["average_assessment_score"],
    "%"
)

print(
    "Skill Gaps:",
    report["skill_gaps"]
)

print(
    "Learning Hours:",
    report["learning_hours"]
)

print(
    "Learning Progress:",
    report["learning_progress"],
    "%"
)

print()

print(
    "Competency Percentages:"
)

for competency, percentage in (
    report[
        "competency_percentages"
    ].items()
):

    print(
        f"{competency}: {percentage}%"
    )

print()