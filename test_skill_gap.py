from navigator.skill_gap import get_skill_gap


user_skills = [
    "Python",
    "SQL",
    "Git"
]


result = get_skill_gap(
    user_skills,
    "Data Scientist"
)


print("\n===== SKILL GAP ANALYSIS =====\n")

print("Career:", result["career"])

print("\nRequired Skills:")
print(", ".join(result["required_skills"]))

print("\nYou Have:")
print(", ".join(result["matched_skills"]))

print("\nYou Need:")
print(", ".join(result["missing_skills"]))