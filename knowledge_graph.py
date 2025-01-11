from calendar import MARCH
from neo4j import GraphDatabase
from typing import List, Dict
from data import mock_data

class ExamKnowledgeGraph:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def create_graph(self, data: List[Dict]):
        with self.driver.session() as session:
            for record in data:
                session.execute_write(self._create_nodes_and_relationships, record)

    @staticmethod
    def _create_nodes_and_relationships(tx, record):
        query = """
        MERGE (s:Student {id: $student_id})
        MERGE (q:Question {id: $question_id, topic: $topic})
        MERGE (m:Module {id: $module_id})

        WITH s, q, m
        OPTIONAL MATCH (prev:Module {id: $module_prerequisite})
        FOREACH (x IN CASE WHEN prev IS NOT NULL THEN [1] ELSE [] END |
            MERGE (prev)-[:PREREQUISITE_OF]->(m)
        )

        CREATE (s)-[:ATTEMPTED {
            student_answer: $student_answer,
            correct_answer: $correct_answer,
            is_correct: $student_answer = $correct_answer
        }]->(q)
        MERGE (q)-[:BELONGS_TO]->(m)
        """

        # Ensure record contains all required fields
        required_fields = {
            'student_id',
            'question_id',
            'topic',
            'module_id',
            'module_prerequisite',
            'student_answer',
            'correct_answer'
        }

        # Validate record has all required fields
        if not all(field in record for field in required_fields):
            missing_fields = required_fields - record.keys()
            raise ValueError(f"Missing required fields: {missing_fields}")

        tx.run(query, **record)

    def analyze_module_transitions(self):
        """Analyze how students perform between directly connected modules"""
        with self.driver.session() as session:
            query = """
            MATCH (m1:Module)-[:PREREQUISITE_OF]->(m2:Module)
            MATCH (s:Student)-[a1:ATTEMPTED]->(q1:Question)-[:BELONGS_TO]->(m1)
            MATCH (s)-[a2:ATTEMPTED]->(q2:Question)-[:BELONGS_TO]->(m2)
            WITH s, m1, m2,
                AVG(CASE WHEN a1.is_correct THEN 1 ELSE 0 END) as m1_score,
                AVG(CASE WHEN a2.is_correct THEN 1 ELSE 0 END) as m2_score
            RETURN
                s.id as student,
                m1.id as prerequisite_module,
                m2.id as next_module,
                ROUND(m1_score * 100) as prerequisite_score,
                ROUND(m2_score * 100) as next_module_score
            ORDER BY student
            """
            return session.run(query).data()
    
    def find_similar_students(self):
        with self.driver.session() as session:
            query = """
            MATCH (s1:Student)-[a1:ATTEMPTED]->(q:Question)<-[a2:ATTEMPTED]-(s2:Student)
            WHERE s1.id < s2.id
            AND a1.is_correct = false AND a2.is_correct = false
            WITH s1, s2,
                COUNT(q) as common_wrong_questions,
                COLLECT(DISTINCT {
                    question: q.id,
                    topic: q.topic,
                    s1_answer: a1.student_answer,
                    s2_answer: a2.student_answer
                }) as shared_mistakes,
                COUNT(DISTINCT q.topic) as common_wrong_topics
            WHERE common_wrong_questions >= 1
            RETURN
                s1.id as student1,
                s2.id as student2,
                shared_mistakes
            ORDER BY common_wrong_questions DESC, common_wrong_topics DESC
            """
            return session.run(query).data()