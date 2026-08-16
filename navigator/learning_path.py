from .graph import graph_db


def get_learning_path(user_skills, target_career):

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
        return []

    # Neo4j query
    query = """
    MATCH (c:Career)
    WHERE toLower(trim(c.name)) = toLower(trim($career))

    MATCH (c)-[:REQUIRES]->(s:Skill)

    WHERE NOT any(
        userSkill IN $user_skills
        WHERE toLower(trim(userSkill)) = toLower(trim(s.name))
    )

    OPTIONAL MATCH (course:Course)-[:TEACHES]->(s)

    RETURN
        s.name AS missing_skill,
        collect(DISTINCT course.name) AS courses

    ORDER BY missing_skill
    """

    # Execute query
    results = graph_db.execute_query(
        query,
        {
            "career": target_career,
            "user_skills": user_skills
        }
    )

    # Build learning path
    learning_path = []

    for result in results:

        learning_path.append({
            "skill": result.get("missing_skill"),
            "courses": [
                course
                for course in result.get("courses", [])
                if course
            ]
        })

    return learning_path