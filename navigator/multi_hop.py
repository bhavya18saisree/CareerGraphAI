from .graph import graph_db


def get_multi_hop_recommendations(user_skills):

    query = """
    UNWIND $user_skills AS user_skill

    MATCH (s:Skill {name: user_skill})
    MATCH (s)-[:RELATED_TO]->(related:Skill)
    MATCH (c:Career)-[:REQUIRES]->(related)

    RETURN DISTINCT
        s.name AS current_skill,
        related.name AS related_skill,
        c.name AS career
    ORDER BY career
    """

    return graph_db.execute_query(
        query,
        {"user_skills": user_skills}
    )