from .recommendation import get_career_recommendations


def get_skill_gap(user_skills, target_career):

    # =========================================================
    # CLEAN USER SKILLS
    # =========================================================

    user_skills = [
        str(skill).strip()
        for skill in (user_skills or [])
        if str(skill).strip()
    ]

    user_skills = list(
        dict.fromkeys(user_skills)
    )

    target_career = str(
        target_career or ""
    ).strip()

    if not target_career:
        return {
            "career": "",
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    # =========================================================
    # USE THE SAME ENGINE AS STEP 02
    # =========================================================

    try:

        recommendations = get_career_recommendations(
            user_skills
        )

    except Exception as e:

        print(
            "Skill gap error:",
            str(e)
        )

        return {
            "career": target_career,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    # =========================================================
    # FIND SELECTED CAREER
    # =========================================================

    selected_result = None

    for result in recommendations:

        career_name = str(
            result.get("career", "")
        ).strip()

        if career_name.lower() == target_career.lower():

            selected_result = result
            break

    # =========================================================
    # CAREER NOT FOUND
    # =========================================================

    if selected_result is None:

        return {
            "career": target_career,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    # =========================================================
    # GET MATCHED + MISSING SKILLS
    # =========================================================

    matched_skills = selected_result.get(
        "matched_skills",
        []
    )

    missing_skills = selected_result.get(
        "missing_skills",
        []
    )

    if not isinstance(matched_skills, list):
        matched_skills = []

    if not isinstance(missing_skills, list):
        missing_skills = []

    # =========================================================
    # REQUIRED SKILLS
    # =========================================================

    required_skills = (
        matched_skills +
        missing_skills
    )

    # Remove duplicates
    required_skills = list(
        dict.fromkeys(required_skills)
    )

    # =========================================================
    # RETURN
    # =========================================================

    return {

        "career":
            selected_result.get(
                "career",
                target_career
            ),

        "required_skills":
            required_skills,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills

    }