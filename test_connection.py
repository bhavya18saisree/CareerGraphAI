from navigator.graph import graph_db


if graph_db.verify_connection():
    print("✅ CognoDB connection successful!")
else:
    print("❌ CognoDB connection failed.")


graph_db.close()