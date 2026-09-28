from services.adaptive_engine import (
    AdaptiveCompetencyEngine
)


engine = AdaptiveCompetencyEngine()


print()
print("==============================")
print("NEXORA ADAPTIVE ENGINE")
print("==============================")
print()


result = engine.update_competency(
    competency="AI and Machine Learning",
    current_level=2,
    score=40
)


print(
    "Competency:",
    result["competency"]
)

print(
    "Assessment Score:",
    result["score"],
    "%"
)

print(
    "Previous Level:",
    result["old_level_name"]
)

print(
    "Updated Level:",
    result["new_level_name"]
)

print(
    "Message:",
    result["message"]
)

print()