from .graph import graph_db


def get_skill_gap(user_skills, target_career):

    query = """
    MATCH (c:Career {name: $career})-[:REQUIRES]->(s:Skill)

    WITH c, collect(s.name) AS required_skills

    RETURN
        c.name AS career,
        required_skills
    """

    results = graph_db.execute_query(
        query,
        {
            "career": target_career
        }
    )

    if not results:
        return {
            "career": target_career,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    result = results[0]

    required_skills = result["required_skills"]

    matched_skills = [
        skill
        for skill in required_skills
        if skill in user_skills
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in user_skills
    ]

    return {
        "career": target_career,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }