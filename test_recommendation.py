from navigator.recommendation import get_career_recommendations


user_skills = [
    "Python",
    "SQL",
    "Git"
]


results = get_career_recommendations(user_skills)


print("\n===== CAREER RECOMMENDATIONS =====\n")


for result in results:

    print(
        f"{result['career']} "
        f"→ {result['score']}%"
    )

    print(
        "Missing:",
        ", ".join(result["missing_skills"])
        if result["missing_skills"]
        else "None"
    )

    print()