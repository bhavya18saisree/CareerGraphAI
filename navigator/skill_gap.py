from .graph import graph_db


def get_skill_gap(user_skills, target_career):

    # =========================================================
    # CLEAN USER SKILLS
    # =========================================================

    user_skills = [
        str(skill).strip()
        for skill in (user_skills or [])
        if str(skill).strip()
    ]

    # Remove duplicates
    user_skills = list(
        dict.fromkeys(user_skills)
    )

    target_career = str(
        target_career or ""
    ).strip()

    # =========================================================
    # VALIDATION
    # =========================================================

    if not target_career:

        return {
            "career": "",
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    # =========================================================
    # DIRECT NEO4J QUERY
    #
    # Do NOT call recommendation.py here.
    # Directly get the skills required by the selected career.
    # =========================================================

    query = """
    MATCH (c:Career)-[:REQUIRES]->(s:Skill)

    WHERE toLower(trim(c.name)) = toLower(trim($career))

    RETURN
        c.name AS career,
        collect(DISTINCT s.name) AS required_skills
    """

    try:

        results = graph_db.execute_query(
            query,
            {
                "career": target_career
            }
        )

    except Exception as e:

        print(
            "Skill gap Neo4j error:",
            str(e)
        )

        return {
            "career": target_career,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    # =========================================================
    # FIND CAREER
    # =========================================================

    selected_result = None

    for result in results:

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
    # REQUIRED SKILLS
    # =========================================================

    required_skills = selected_result.get(
        "required_skills",
        []
    )

    if not isinstance(required_skills, list):

        required_skills = []

    # Remove empty values
    required_skills = [
        str(skill).strip()
        for skill in required_skills
        if str(skill).strip()
    ]

    # =========================================================
    # CASE-INSENSITIVE MATCHING
    # =========================================================

    normalized_user_skills = {
        str(skill).strip().lower()
        for skill in user_skills
    }

    matched_skills = []

    missing_skills = []

    for required_skill in required_skills:

        normalized_required = (
            str(required_skill)
            .strip()
            .lower()
        )

        if normalized_required in normalized_user_skills:

            matched_skills.append(
                required_skill
            )

        else:

            missing_skills.append(
                required_skill
            )

    # =========================================================
    # FINAL RESULT
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