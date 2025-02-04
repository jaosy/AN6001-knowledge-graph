# 🎓 Knowledge Graph and NLP-Powered Educational Analytics Chatbot 🎓
## AN6001 AI & Big Data in Business ● Proof of Concept 

# ✨ Features
- 📊 Module Performance Analysis: Track students' progress between different modules
- 👥 Student Pattern Recognition: Identify similar students based on their common mistakes
- 🔄 Prerequisite Relationships: Understand module dependencies and educational pathways

# 🛠️ Tech Stack
- Backend: Python, Neo4j
- NLP: spaCy, Sentence Transformers
- Frontend: Streamlit
- Data Analysis: Pandas

# 🚀 Quick Start
1. Clone the repository
2. Install dependencies
```pip install -r requirements.txt```
```python -m spacy download en_core_web_sm```
3. Set up Neo4j
4. Ensure Neo4j is running locally on port 7687
5. Run `python main.py` to create the knowledge graph
6. Update credentials in `chatbot.py` if needed
7. Run the application
```python -m streamlit run app.py```

![Knowledge graph preview](https://github.com/jaosy/AN6001-knowledge-graph/blob/main/graph.png?raw=true)

