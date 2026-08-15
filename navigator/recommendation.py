from .graph import graph_db


def get_career_recommendations(user_skills):

    query = """
    MATCH (c:Career)-[:REQUIRES]->(s:Skill)
    WITH c, collect(s.name) AS required_skills

    WITH c,
         required_skills,
         [skill IN required_skills
          WHERE skill IN $user_skills] AS matched_skills

    RETURN
        c.name AS career,
        required_skills,
        matched_skills,
        size(matched_skills) AS matched_count,
        size(required_skills) AS total_required
    ORDER BY matched_count DESC
    """

    results = graph_db.execute_query(
        query,
        {"user_skills": user_skills}
    )

    recommendations = []

    for result in results:

        total_required = result["total_required"]

        if total_required == 0:
            score = 0
        else:
            score = round(
                (result["matched_count"] / total_required) * 100
            )

        missing_skills = [
            skill
            for skill in result["required_skills"]
            if skill not in user_skills
        ]

        recommendations.append({
            "career": result["career"],
            "score": score,
            "matched_skills": result["matched_skills"],
            "missing_skills": missing_skills
        })

    return recommendations