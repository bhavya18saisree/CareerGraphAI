from .recommendation import get_career_recommendations


def get_skill_gap(user_skills, target_career):

    # Clean user skills
    user_skills = [
        str(skill).strip()
        for skill in (user_skills or [])
        if str(skill).strip()
    ]

    # Clean target career
    target_career = str(target_career or "").strip()

    if not target_career:
        return {
            "career": "",
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    try:

        # IMPORTANT:
        # Use the SAME recommendation engine that already
        # works correctly in Step 02.
        recommendations = get_career_recommendations(
            user_skills
        )

    except Exception as e:

        print("Skill gap recommendation error:", e)

        return {
            "career": target_career,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    # Find the selected career
    selected_result = None

    for result in recommendations:

        career_name = str(
            result.get("career", "")
        ).strip()

        if career_name.lower() == target_career.lower():

            selected_result = result
            break

    # Career not found
    if selected_result is None:

        return {
            "career": target_career,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    matched_skills = selected_result.get(
        "matched_skills",
        []
    )

    missing_skills = selected_result.get(
        "missing_skills",
        []
    )

    # Make sure they are always lists
    if not isinstance(matched_skills, list):
        matched_skills = []

    if not isinstance(missing_skills, list):
        missing_skills = []

    required_skills = (
        matched_skills +
        missing_skills
    )

    return {
        "career": selected_result.get(
            "career",
            target_career
        ),

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills
    }