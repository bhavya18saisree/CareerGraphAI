# 🚀 CareerGraph AI

### Intelligent Career & Skill Navigator

CareerGraph AI is a graph-powered career intelligence platform that helps users discover suitable career paths based on their existing skills, identify skill gaps, and generate personalized learning paths.

The system uses a graph database to model relationships between careers, skills, courses, technologies, projects, and industries. This enables the platform to provide career recommendations beyond simple keyword matching.

---

## 🎯 Problem Statement

Students and early-career professionals often struggle to understand:

- Which career paths match their current skills?
- Which skills are missing for a target career?
- What should they learn next?
- How are different skills, careers, courses, and technologies connected?

CareerGraph AI addresses these challenges through a structured career knowledge graph and intelligent recommendation system.

---

## ✨ Key Features

### 🎯 Career Recommendations
Recommends suitable career paths based on the skills selected by the user.

### 📊 Career Match Score
Calculates a match percentage based on the user's existing skills and the skills required for each career.

### 🔍 Skill Gap Analysis
Identifies the skills the user is missing for a selected career.

### 📚 Personalized Learning Path
Provides learning recommendations based on the identified skill gaps.

### 🔗 Multi-Hop Graph Recommendations
Uses relationships in the career knowledge graph to discover connected career, skill, course, technology, and industry information.

### 🧠 Graph-Powered Career Intelligence
Uses a Neo4j-compatible graph database through CognoDB to represent relationships between career entities.

### ⚡ Interactive Web Interface
Provides an interactive interface where users can select skills, analyze careers, view skill gaps, and explore learning paths.

### 🛡️ Error & Empty-State Handling
Handles invalid requests, empty selections, loading states, and unavailable recommendation results.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      User            │
                    │  Selects Skills      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   JavaScript UI      │
                    │   HTML + CSS         │
                    └──────────┬───────────┘
                               │
                         REST API Calls
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Django         │
                    │      Backend         │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       Career Engine      Skill Gap       Learning Path
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Graph Database     │
                    │ CognoDB / Neo4j      │
                    │    Compatible       │
                    └──────────────────────┘

