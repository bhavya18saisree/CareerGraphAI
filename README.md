**# 🚀 Career Graph AI**



**Career Graph AI is an intelligent career and skill navigation system that uses a graph database to recommend suitable career paths, identify skill gaps, and generate personalized learning paths.**



**## 🎯 Features**



**- Career recommendations based on user skills**

**- Skill gap analysis**

**- Personalized learning path**

**- Multi-hop graph-based recommendations**

**- Graph database powered career intelligence**

**- Loading, empty-state and error handling**

**- Relational + graph database architecture**



**## 🏗️ Technology Stack**



**- Django**

**- Python**

**- JavaScript**

**- HTML**

**- CSS**

**- SQLite**

**- CognoDB / Neo4j-compatible Graph Database**



**## 🧠 Graph Model**



**The core career knowledge graph is structured using nodes and relationships:**



**```text**

&#x20;                        **┌──────────────┐**

&#x20;                        **│    Career    │**

&#x20;                        **└──────┬───────┘**

&#x20;                               **│**

&#x20;                            **REQUIRES**

&#x20;                               **│**

&#x20;                               **▼**

&#x20;                        **┌──────────────┐**

&#x20;                        **│    Skill     │**

&#x20;                        **└──────┬───────┘**

&#x20;                               **│**

&#x20;                           **RELATED\_TO**

&#x20;                               **│**

&#x20;                               **▼**

&#x20;                        **┌──────────────┐**

&#x20;                        **│    Skill     │**

&#x20;                        **└──────┬───────┘**

&#x20;                               **│**

&#x20;                            **REQUIRES**

&#x20;                               **│**

&#x20;                               **▼**

&#x20;                        **┌──────────────┐**

&#x20;                        **│    Career    │**

&#x20;                        **└──────────────┘**





&#x20;       **┌──────────────┐**

&#x20;       **│    Course    │**

&#x20;       **└──────┬───────┘**

&#x20;              **│**

&#x20;            **TEACHES**

&#x20;              **│**

&#x20;              **▼**

&#x20;       **┌──────────────┐**

&#x20;       **│    Skill     │**

&#x20;       **└──────────────┘**





&#x20;       **┌──────────────┐**

&#x20;       **│   Project    │**

&#x20;       **└──────┬───────┘**

&#x20;              **│**

&#x20;             **USES**

&#x20;              **│**

&#x20;              **▼**

&#x20;       **┌──────────────┐**

&#x20;       **│ Technology   │**

&#x20;       **└──────────────┘**





&#x20;       **┌──────────────┐**

&#x20;       **│    Career    │**

&#x20;       **└──────┬───────┘**

&#x20;              **│**

&#x20;         **IN\_INDUSTRY**

&#x20;              **│**

&#x20;              **▼**

&#x20;       **┌──────────────┐**

&#x20;       **│   Industry   │**

&#x20;       **└──────────────┘**

