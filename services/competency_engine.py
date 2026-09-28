import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
COMPETENCY_FILE = BASE_DIR / "data" / "competencies.csv"
ROLE_FILE = BASE_DIR / "data" / "role_requirements.csv"


def load_competencies():
    """Load the official competency framework."""
    return pd.read_csv(COMPETENCY_FILE)


def load_role_requirements():
    """Load required competency levels for each role."""
    return pd.read_csv(ROLE_FILE)


def analyze_skill_gaps(role, user_skills):
    """
    Compare the user's current competency levels
    against the competency requirements of their role.

    user_skills format:
    {
        "Python": 2,
        "SQL": 1,
        "GIS": 1
    }
    """

    roles = load_role_requirements()

    role_data = roles[
        roles["role"].str.lower() == role.lower()
    ]

    if role_data.empty:
        return {
            "error": f"No competency framework found for role: {role}"
        }

    results = []

    for _, requirement in role_data.iterrows():

        competency = requirement["competency"]
        required_level = int(requirement["required_level"])

        current_level = int(user_skills.get(competency, 0))

        gap = max(required_level - current_level, 0)

        if gap == 0:
            status = "No Gap"
        elif gap == 1:
            status = "Low"
        elif gap == 2:
            status = "Medium"
        else:
            status = "High"

        results.append({
            "competency": competency,
            "required_level": required_level,
            "current_level": current_level,
            "gap": gap,
            "status": status
        })

    return pd.DataFrame(results)


def get_priority_gaps(gap_df):
    """Return competencies with the largest skill gaps."""

    if gap_df.empty:
        return gap_df

    return gap_df[
        gap_df["gap"] > 0
    ].sort_values(
        by="gap",
        ascending=False
    )
def calculate_competency_score(gap_df):
    """
    Calculate overall competency percentage
    based on current level vs required level.
    """

    if gap_df.empty:
        return 0

    total_required = gap_df["required_level"].sum()
    total_current = gap_df["current_level"].sum()

    score = (total_current / total_required) * 100

    return round(min(score, 100), 2)