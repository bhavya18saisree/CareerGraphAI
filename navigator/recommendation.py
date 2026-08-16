from .graph import graph_db


def normalize_skill(skill):
    """
    Normalize a skill so comparisons are consistent.

    Examples:
        'Python'      -> 'python'
        ' python '    -> 'python'
        'REST API'    -> 'rest api'
        'rest api'    -> 'rest api'
    """
    if skill is None:
        return ""

    return " ".join(
        str(skill).strip().lower().split()
    )


def get_career_recommendations(user_skills):
    """
    Generate career recommendations from the Neo4j
    Career -> REQUIRES -> Skill graph.

    Returns:
        [
            {
                "career": "...",
                "score": 80,
                "matched_skills": [...],
                "missing_skills": [...]
            }
        ]
    """

    # =========================================
    # 1. CLEAN USER SKILLS
    # =========================================

    if not user_skills:
        return []

    cleaned_skills = []
    seen_skills = set()

    for skill in user_skills:

        normalized = normalize_skill(skill)

        if not normalized:
            continue

        # Remove duplicate skills
        if normalized not in seen_skills:

            seen_skills.add(normalized)

            # Keep a clean display version
            cleaned_skills.append(
                str(skill).strip()
            )

    if not cleaned_skills:
        return []

    # =========================================
    # 2. NEO4J QUERY
    # =========================================

    query = """
    MATCH (c:Career)-[:REQUIRES]->(s:Skill)

    WITH
        c,
        collect(DISTINCT trim(s.name)) AS required_skills

    WITH
        c,
        required_skills,
        [
            skill IN required_skills
            WHERE any(
                userSkill IN $user_skills
                WHERE
                    toLower(trim(skill))
                    =
                    toLower(trim(userSkill))
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

    # =========================================
    # 3. EXECUTE NEO4J QUERY
    # =========================================

    try:

        results = graph_db.execute_query(
            query,
            {
                "user_skills": cleaned_skills
            }
        )

    except Exception as e:

        print(
            "Neo4j recommendation error:",
            str(e)
        )

        return []

    # =========================================
    # 4. PROCESS RESULTS
    # =========================================

    recommendations = []

    for result in results:

        career = result.get("career")

        if not career:
            continue

        required_skills = result.get(
            "required_skills",
            []
        )

        matched_skills = result.get(
            "matched_skills",
            []
        )

        # Make sure values are lists
        if not isinstance(required_skills, list):
            required_skills = []

        if not isinstance(matched_skills, list):
            matched_skills = []

        if not required_skills:
            continue

        # =========================================
        # 5. CLEAN REQUIRED SKILLS
        # =========================================

        required_skills = [
            str(skill).strip()
            for skill in required_skills
            if skill is not None
            and str(skill).strip()
        ]

        # =========================================
        # 6. CLEAN MATCHED SKILLS
        # =========================================

        matched_skills = [
            str(skill).strip()
            for skill in matched_skills
            if skill is not None
            and str(skill).strip()
        ]

        # =========================================
        # 7. FIND MISSING SKILLS
        # =========================================

        user_skill_set = {
            normalize_skill(skill)
            for skill in cleaned_skills
        }

        missing_skills = []

        for required_skill in required_skills:

            required_normalized = normalize_skill(
                required_skill
            )

            if required_normalized not in user_skill_set:

                missing_skills.append(
                    required_skill
                )

        # =========================================
        # 8. CALCULATE MATCH SCORE
        # =========================================

        total_required = len(
            required_skills
        )

        matched_count = len(
            matched_skills
        )

        if total_required > 0:

            score = round(
                (
                    matched_count
                    /
                    total_required
                ) * 100
            )

        else:

            score = 0

        # =========================================
        # 9. ADD CAREER
        # =========================================

        recommendations.append({

            "career": str(career).strip(),

            "score": score,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills

        })

    # =========================================
    # 10. SORT CAREERS
    # =========================================

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # =========================================
    # 11. RETURN TOP 10
    # =========================================

    return recommendations[:10]