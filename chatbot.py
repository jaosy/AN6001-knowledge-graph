from neo4j import GraphDatabase
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class EduChatbot:
    def __init__(self):
        # connect to neo4j database
        # replace with your own credentials - neo4j is locally hosted
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

        # Load NLP models
        self.nlp = spacy.load("en_core_web_sm")
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Define basic intents
        self.intents = [
            {
                "name": "performance",
                "patterns": [
                    "How are students performing?",
                    "Show performance",
                    "Student scores",
                    "Module performance"
                ],
                "handler": self._handle_performance
            },
            {
                "name": "topics",
                "patterns": [
                    "What topics are difficult?",
                    "Show topics",
                    "Topic analysis"
                ],
                "handler": self._handle_topics
            }
        ]

    def get_response(self, user_input: str) -> str:
        # Find the most similar intent
        intent = self._find_intent(user_input)
        if intent:
            return intent["handler"]()
        return "I'm not sure how to help with that. Try asking about student performance or topics."

    def _find_intent(self, user_input: str):
        # Encode user input
        input_embedding = self.sentence_model.encode([user_input])

        best_similarity = 0
        best_intent = None

        # Find most similar intent
        for intent in self.intents:
            pattern_embeddings = self.sentence_model.encode(intent["patterns"])
            similarity = cosine_similarity(input_embedding, pattern_embeddings)
            max_similarity = np.max(similarity)

            if max_similarity > best_similarity:
                best_similarity = max_similarity
                best_intent = intent

        return best_intent if best_similarity > 0.5 else None

    def _handle_performance(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (s:Student)-[a:ATTEMPTED]->(q:Question)
                WITH s.id as student,
                     avg(CASE WHEN a.is_correct THEN 1 ELSE 0 END) as score
                RETURN
                    avg(score) as avg_score,
                    count(student) as student_count
            """)
            data = result.single()

            if data:
                return f"Average student performance: {data['avg_score']*100:.1f}% "\
                       f"across {data['student_count']} students"
            return "No performance data available"

    def _handle_topics(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (q:Question)<-[a:ATTEMPTED]-()
                WITH q.topic as topic,
                     count(a) as attempts,
                     sum(CASE WHEN a.is_correct THEN 1 ELSE 0 END) as correct
                RETURN topic,
                       toFloat(correct)/attempts as success_rate
                ORDER BY success_rate ASC
                LIMIT 3
            """)

            topics = [f"- {record['topic']}: {record['success_rate']*100:.1f}% success rate"
                     for record in result]

            if topics:
                return "Most challenging topics:\n" + "\n".join(topics)
            return "No topic data available"

    def close(self):
        self.driver.close()