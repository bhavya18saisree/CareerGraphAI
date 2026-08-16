from .graph import graph_db


def get_skill_gap(user_skills, target_career):
    """
    Calculate the skill gap between the user's skills
    and the skills required for the selected career.

    Matching is case-insensitive and ignores extra spaces.
    """

    # -----------------------------------------
    # CLEAN USER SKILLS
    # -----------------------------------------

    if not user_skills:
        user_skills = []

    cleaned_user_skills = []

    for skill in user_skills:
        if skill is None:
            continue

        skill = str(skill).strip()

        if skill:
            cleaned_user_skills.append(skill)

    # Remove duplicates
    cleaned_user_skills = list(
        dict.fromkeys(cleaned_user_skills)
    )

    # -----------------------------------------
    # VALIDATE CAREER
    # -----------------------------------------

    if not target_career:
        return {
            "career": "",
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    # -----------------------------------------
    # GET CAREER SKILLS FROM NEO4J
    # -----------------------------------------

    query = """
    MATCH (c:Career)-[:REQUIRES]->(s:Skill)

    WHERE toLower(trim(c.name)) = toLower(trim($career))

    WITH
        c,
        collect(DISTINCT s.name) AS required_skills

    RETURN
        c.name AS career,
        required_skills
    """

    try:

        results = graph_db.execute_query(
            query,
            {
                "career": target_career
            }
        )

    except Exception as e:

        print("Skill gap Neo4j error:", str(e))

        return {
            "career": target_career,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    # -----------------------------------------
    # CAREER NOT FOUND
    # -----------------------------------------

    if not results:

        return {
            "career": target_career,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    result = results[0]

    career_name = result.get(
        "career",
        target_career
    )

    required_skills = result.get(
        "required_skills",
        []
    )

    # -----------------------------------------
    # CASE-INSENSITIVE SKILL MATCHING
    # -----------------------------------------

    user_skill_lookup = {
        str(skill).strip().lower(): skill
        for skill in cleaned_user_skills
    }

    matched_skills = []
    missing_skills = []

    for required_skill in required_skills:

        if required_skill is None:
            continue

        required_clean = (
            str(required_skill)
            .strip()
        )

        required_key = (
            required_clean.lower()
        )

        if required_key in user_skill_lookup:

            # Use the skill name from Neo4j
            # so the display is consistent.
            matched_skills.append(
                required_clean
            )

        else:

            missing_skills.append(
                required_clean
            )

    # -----------------------------------------
    # RETURN RESULT
    # -----------------------------------------

    return {
        "career": career_name,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }