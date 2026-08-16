from .graph import graph_db


def get_career_recommendations(user_skills):
    """
    Generate career recommendations from the Neo4j career-skill graph.

    The function:
    1. Cleans the user's selected skills.
    2. Finds all Career -> REQUIRES -> Skill relationships.
    3. Matches skills case-insensitively.
    4. Calculates a career match percentage.
    5. Returns missing skills.
    """

    # -----------------------------------------
    # CLEAN USER SKILLS
    # -----------------------------------------

    if not user_skills:
        return []

    cleaned_skills = []

    for skill in user_skills:
        if skill is None:
            continue

        skill = str(skill).strip()

        if skill:
            cleaned_skills.append(skill)

    if not cleaned_skills:
        return []

    # Remove duplicates while preserving order
    cleaned_skills = list(dict.fromkeys(cleaned_skills))

    # -----------------------------------------
    # NEO4J QUERY
    # -----------------------------------------

    query = """
    MATCH (c:Career)-[:REQUIRES]->(s:Skill)

    WITH
        c,
        collect(DISTINCT s.name) AS required_skills

    WITH
        c,
        required_skills,
        [
            skill IN required_skills
            WHERE any(
                userSkill IN $user_skills
                WHERE toLower(trim(skill)) = toLower(trim(userSkill))
            )
        ] AS matched_skills

    RETURN
        c.name AS career,
        required_skills,
        matched_skills,
        size(matched_skills) AS matched_count,
        size(required_skills) AS total_required

    ORDER BY matched_count DESC
    """

    try:

        results = graph_db.execute_query(
            query,
            {
                "user_skills": cleaned_skills
            }
        )

    except Exception as e:

        print("Neo4j recommendation error:", str(e))

        return []

    recommendations = []

    # -----------------------------------------
    # PROCESS RESULTS
    # -----------------------------------------

    for result in results:

        career = result.get("career")

        required_skills = result.get(
            "required_skills",
            []
        )

        matched_skills = result.get(
            "matched_skills",
            []
        )

        if not career:
            continue

        if not required_skills:
            continue

        total_required = len(required_skills)

        matched_count = len(matched_skills)

        # -----------------------------------------
        # CALCULATE SCORE
        # -----------------------------------------

        score = round(
            (matched_count / total_required) * 100
        )

        # -----------------------------------------
        # FIND MISSING SKILLS
        # -----------------------------------------

        missing_skills = []

        for required_skill in required_skills:

            found = False

            for user_skill in cleaned_skills:

                if (
                    str(required_skill).strip().lower()
                    ==
                    str(user_skill).strip().lower()
                ):
                    found = True
                    break

            if not found:
                missing_skills.append(
                    required_skill
                )

        # -----------------------------------------
        # ADD RECOMMENDATION
        # -----------------------------------------

        recommendations.append({

            "career": career,

            "score": score,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills

        })

    # -----------------------------------------
    # SORT RESULTS
    # -----------------------------------------

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Return maximum 10 careers
    return recommendations[:10]