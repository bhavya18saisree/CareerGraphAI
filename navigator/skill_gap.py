from .graph import graph_db


def get_skill_gap(user_skills, target_career):

    # Clean user skills
    user_skills = [
        str(skill).strip()
        for skill in (user_skills or [])
        if str(skill).strip()
    ]

    # Case-insensitive lookup
    user_skill_lookup = {
        skill.lower(): skill
        for skill in user_skills
    }

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

        print("Skill gap error:", e)

        return {
            "career": target_career,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    if not results:

        return {
            "career": target_career,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    result = results[0]

    career_name = result["career"]

    required_skills = result["required_skills"] or []

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill is None:
            continue

        skill_name = str(skill).strip()

        if skill_name.lower() in user_skill_lookup:

            matched_skills.append(skill_name)

        else:

            missing_skills.append(skill_name)

    return {
        "career": career_name,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }