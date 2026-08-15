from navigator.learning_path import get_learning_path


user_skills = [
    "Python",
    "SQL",
    "Git"
]


target_career = "Data Scientist"


results = get_learning_path(
    user_skills,
    target_career
)


print("\n===== PERSONALIZED LEARNING PATH =====\n")

print("Target Career:", target_career)

for item in results:

    print("\nMissing Skill:")
    print(item["skill"])

    print("Recommended Courses:")

    if item["courses"]:
        for course in item["courses"]:
            print("  →", course)
    else:
        print("  No course available")