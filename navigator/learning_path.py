from .graph import graph_db


def get_learning_path(user_skills, target_career):

    query = """
    MATCH (c:Career {name: $career})-[:REQUIRES]->(s:Skill)
    WHERE NOT s.name IN $user_skills

    OPTIONAL MATCH (course:Course)-[:TEACHES]->(s)

    RETURN
        s.name AS missing_skill,
        collect(DISTINCT course.name) AS courses
    ORDER BY missing_skill
    """

    results = graph_db.execute_query(
        query,
        {
            "career": target_career,
            "user_skills": user_skills
        }
    )

    learning_path = []

    for result in results:

        learning_path.append({
            "skill": result["missing_skill"],
            "courses": result["courses"]
        })

    return learning_path