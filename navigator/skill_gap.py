from .recommendation import get_career_recommendations


def get_skill_gap(user_skills, target_career):

    # Clean user skills
    user_skills = [
        str(skill).strip()
        for skill in (user_skills or [])
        if str(skill).strip()
    ]

    # Clean career name
    target_career = str(target_career or "").strip()

    # If no career is selected
    if not target_career:
        return {
            "career": "",
            "user_skills": user_skills,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    # Get career recommendations
    recommendations = get_career_recommendations(
        user_skills
    )

    # Find the selected career
    selected_result = None

    for result in recommendations:

        career_name = str(
            result.get("career", "")
        ).strip()

        if career_name.lower() == target_career.lower():

            selected_result = result
            break

    # Career was not found
    if selected_result is None:
        return {
            "career": target_career,
            "user_skills": user_skills,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    # Get matched skills
    matched_skills = selected_result.get(
        "matched_skills",
        []
    )

    # Get missing skills
    missing_skills = selected_result.get(
        "missing_skills",
        []
    )

    # Make sure both are lists
    if not isinstance(matched_skills, list):
        matched_skills = []

    if not isinstance(missing_skills, list):
        missing_skills = []

    # Required skills
    required_skills = (
        matched_skills +
        missing_skills
    )

    return {
        "career": selected_result.get(
            "career",
            target_career
        ),

        "user_skills": user_skills,

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills
    }