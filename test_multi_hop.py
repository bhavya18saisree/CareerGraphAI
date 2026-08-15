from navigator.graph import graph_db

query = """
MATCH (c:Career)-[:REQUIRES]->(s:Skill)
      -[:RELATED_TO]->(related:Skill)
RETURN c.name AS career,
       s.name AS skill,
       related.name AS related_skill
LIMIT 20
"""

results = graph_db.execute_query(query)

if results:
    print("\nMULTI-HOP GRAPH RESULTS")
    print("=" * 50)

    for row in results:
        print(
            f"Career: {row['career']} | "
            f"Skill: {row['skill']} | "
            f"Related Skill: {row['related_skill']}"
        )
else:
    print("No multi-hop results found.")

graph_db.close()