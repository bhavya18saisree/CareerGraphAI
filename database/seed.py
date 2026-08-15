import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from navigator.graph import graph_db


def create_constraints():
    queries = [
        """
        CREATE CONSTRAINT skill_name IF NOT EXISTS
        FOR (s:Skill)
        REQUIRE s.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT career_name IF NOT EXISTS
        FOR (c:Career)
        REQUIRE c.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT course_name IF NOT EXISTS
        FOR (c:Course)
        REQUIRE c.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT technology_name IF NOT EXISTS
        FOR (t:Technology)
        REQUIRE t.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT industry_name IF NOT EXISTS
        FOR (i:Industry)
        REQUIRE i.name IS UNIQUE
        """
    ]

    for query in queries:
        graph_db.execute_query(query)


def seed_graph():

    skills = [
        "Python",
        "SQL",
        "JavaScript",
        "React",
        "Django",
        "Machine Learning",
        "Statistics",
        "Data Analysis",
        "Git",
        "Docker",
        "AWS",
        "Neo4j",
        "REST API",
        "HTML",
        "CSS"
    ]

    careers = [
        "Data Scientist",
        "Data Engineer",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
        "Machine Learning Engineer",
        "Cloud Engineer",
        "Graph Database Developer"
    ]

    technologies = [
        "Python",
        "Django",
        "React",
        "Docker",
        "AWS",
        "Neo4j"
    ]

    industries = [
        "Technology",
        "Finance",
        "Healthcare",
        "E-Commerce",
        "Consulting"
    ]

    courses = [
        "Python for Data Science",
        "SQL Mastery",
        "Django Backend Development",
        "React Development",
        "Machine Learning Fundamentals",
        "Cloud Computing with AWS",
        "Docker Essentials",
        "Graph Databases with Neo4j"
    ]

    projects = [
        "Customer Churn Predictor",
        "Career Recommendation System",
        "E-Commerce Dashboard",
        "Banking API",
        "Healthcare Analytics Platform",
        "Cloud Monitoring System",
        "Movie Recommendation Engine",
        "Knowledge Graph Explorer"
    ]

    # Create skills
    for skill in skills:
        graph_db.execute_query(
            """
            MERGE (s:Skill {name: $name})
            """,
            {"name": skill}
        )

    # Create careers
    for career in careers:
        graph_db.execute_query(
            """
            MERGE (c:Career {name: $name})
            """,
            {"name": career}
        )

    # Create technologies
    for technology in technologies:
        graph_db.execute_query(
            """
            MERGE (t:Technology {name: $name})
            """,
            {"name": technology}
        )

    # Create industries
    for industry in industries:
        graph_db.execute_query(
            """
            MERGE (i:Industry {name: $name})
            """,
            {"name": industry}
        )

    # Create courses
    for course in courses:
        graph_db.execute_query(
            """
            MERGE (c:Course {name: $name})
            """,
            {"name": course}
        )

    # Create projects
    for project in projects:
        graph_db.execute_query(
            """
            MERGE (p:Project {name: $name})
            """,
            {"name": project}
        )

    print("✅ Graph data created successfully!")

def create_relationships():

    # Career -> Required Skills
    career_skills = {
        "Data Scientist": [
            "Python",
            "SQL",
            "Machine Learning",
            "Statistics",
            "Data Analysis"
        ],

        "Data Engineer": [
            "Python",
            "SQL",
            "Docker",
            "AWS",
            "Git"
        ],

        "Backend Developer": [
            "Python",
            "Django",
            "SQL",
            "REST API",
            "Git"
        ],

        "Frontend Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Git"
        ],

        "Full Stack Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Python",
            "Django",
            "SQL",
            "Git"
        ],

        "Machine Learning Engineer": [
            "Python",
            "Machine Learning",
            "Statistics",
            "Docker",
            "AWS"
        ],

        "Cloud Engineer": [
            "AWS",
            "Docker",
            "Python",
            "Git"
        ],

        "Graph Database Developer": [
            "Python",
            "Neo4j",
            "SQL",
            "REST API",
            "Docker"
        ]
    }

    for career, skills in career_skills.items():

        for skill in skills:

            graph_db.execute_query(
                """
                MATCH (c:Career {name: $career})
                MATCH (s:Skill {name: $skill})
                MERGE (c)-[:REQUIRES]->(s)
                """,
                {
                    "career": career,
                    "skill": skill
                }
            )


    # Course -> Skills
    course_skills = {
        "Python for Data Science": [
            "Python",
            "Data Analysis",
            "Statistics"
        ],

        "SQL Mastery": [
            "SQL"
        ],

        "Django Backend Development": [
            "Python",
            "Django",
            "REST API"
        ],

        "React Development": [
            "JavaScript",
            "React",
            "HTML",
            "CSS"
        ],

        "Machine Learning Fundamentals": [
            "Python",
            "Machine Learning",
            "Statistics"
        ],

        "Cloud Computing with AWS": [
            "AWS",
            "Python"
        ],

        "Docker Essentials": [
            "Docker"
        ],

        "Graph Databases with Neo4j": [
            "Neo4j",
            "Python"
        ]
    }

    for course, skills in course_skills.items():

        for skill in skills:

            graph_db.execute_query(
                """
                MATCH (c:Course {name: $course})
                MATCH (s:Skill {name: $skill})
                MERGE (c)-[:TEACHES]->(s)
                """,
                {
                    "course": course,
                    "skill": skill
                }
            )


    # Project -> Technology
    project_technologies = {
        "Customer Churn Predictor": [
            "Python"
        ],

        "Career Recommendation System": [
            "Python",
            "Django",
            "Neo4j"
        ],

        "E-Commerce Dashboard": [
            "React",
            "JavaScript"
        ],

        "Banking API": [
            "Python",
            "Django"
        ],

        "Healthcare Analytics Platform": [
            "Python"
        ],

        "Cloud Monitoring System": [
            "Python",
            "Docker",
            "AWS"
        ],

        "Movie Recommendation Engine": [
            "Python",
            "Neo4j"
        ],

        "Knowledge Graph Explorer": [
            "Python",
            "Neo4j",
            "Django"
        ]
    }

    for project, technologies in project_technologies.items():

        for technology in technologies:

            graph_db.execute_query(
                """
                MATCH (p:Project {name: $project})
                MATCH (t:Technology {name: $technology})
                MERGE (p)-[:USES]->(t)
                """,
                {
                    "project": project,
                    "technology": technology
                }
            )


    # Career -> Industry
    career_industries = {
        "Data Scientist": "Technology",
        "Data Engineer": "Technology",
        "Backend Developer": "Technology",
        "Frontend Developer": "Technology",
        "Full Stack Developer": "Technology",
        "Machine Learning Engineer": "Healthcare",
        "Cloud Engineer": "Finance",
        "Graph Database Developer": "Consulting"
    }

    for career, industry in career_industries.items():

        graph_db.execute_query(
            """
            MATCH (c:Career {name: $career})
            MATCH (i:Industry {name: $industry})
            MERGE (c)-[:IN_INDUSTRY]->(i)
            """,
            {
                "career": career,
                "industry": industry
            }
        )


    # Skill -> Related Skill
    related_skills = [
        ("Python", "Machine Learning"),
        ("Python", "Django"),
        ("Python", "Data Analysis"),
        ("JavaScript", "React"),
        ("HTML", "CSS"),
        ("SQL", "Data Analysis"),
        ("AWS", "Docker"),
        ("Neo4j", "Python"),
        ("Machine Learning", "Statistics"),
        ("Django", "REST API")
    ]

    for skill1, skill2 in related_skills:

        graph_db.execute_query(
            """
            MATCH (s1:Skill {name: $skill1})
            MATCH (s2:Skill {name: $skill2})
            MERGE (s1)-[:RELATED_TO]->(s2)
            """,
            {
                "skill1": skill1,
                "skill2": skill2
            }
        )

    print("✅ Relationships created successfully!")

if __name__ == "__main__":
    create_constraints()
    seed_graph()
    create_relationships()
    graph_db.close()