import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")


class GraphDB:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            COGNODB_URI,
            auth=(COGNODB_USERNAME, COGNODB_PASSWORD)
        )

    def verify_connection(self):
        try:
            self.driver.verify_connectivity()
            return True
        except Exception as e:
            print(f"CognoDB connection failed: {e}")
            return False

    def execute_query(self, query, parameters=None):
        try:
            with self.driver.session() as session:
                result = session.run(
                    query,
                    parameters or {}
                )
                return result.data()

        except Exception as e:
            print(f"Query failed: {e}")
            return []

    def close(self):
        self.driver.close()


graph_db = GraphDB()