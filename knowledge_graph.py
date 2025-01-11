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

    def analyze_topic_relationships(self):
        """Identify conceptually related areas where students struggle"""
        with self.driver.session() as session:
            query = """
            MATCH (q1:Question)-[:BELONGS_TO]->(m1:Module)
            MATCH (q2:Question)-[:BELONGS_TO]->(m2:Module)
            WHERE q1.topic < q2.topic
            MATCH (s:Student)-[a1:ATTEMPTED]->(q1)
            MATCH (s:Student)-[a2:ATTEMPTED]->(q2)
            WHERE a1.is_correct = false AND a2.is_correct = false
            RETURN
                m1.id as module1,
                m2.id as module2,
                q1.topic as topic1,
                q2.topic as topic2,
                COUNT(*) as student_count,
                COLLECT(DISTINCT s.id) as struggling_students
            ORDER BY student_count DESC
            LIMIT 10
            """
            return session.run(query).data()
        
    def analyze_question_patterns(self):
        with self.driver.session() as session:
            query = """
            MATCH (q:Question)-[:BELONGS_TO]->(m:Module)
            MATCH (s:Student)-[a:ATTEMPTED]->(q)
            WITH q, m,
                COUNT(a) as total_attempts,
                SUM(CASE WHEN a.is_correct THEN 1 ELSE 0 END) as correct_answers,
                COLLECT(DISTINCT {
                    answer: a.student_answer,
                    correct: a.correct_answer,
                    student: s.id
                })[..5] as wrong_attempts
            WHERE total_attempts >= 3
            RETURN 
                m.id as module,
                q.topic as topic,
                total_attempts,
                correct_answers,
                ROUND(100.0 * correct_answers / total_attempts) as success_rate,
                [x IN wrong_attempts WHERE x.answer <> x.correct] as sample_wrong_answers
            ORDER BY success_rate ASC
            LIMIT 15
            """
            return session.run(query).data()
        
    def find_similar_students(self):
        with self.driver.session() as session:
            query = """
            MATCH (s1:Student)-[a1:ATTEMPTED]->(q:Question)<-[a2:ATTEMPTED]-(s2:Student)
            WHERE s1.id < s2.id 
            AND a1.is_correct = false AND a2.is_correct = false
            WITH s1, s2,
                COUNT(q) as common_wrong_questions
            WHERE common_wrong_questions >= 3
            RETURN
                [s1.id, s2.id] as student_pair, 
                common_wrong_questions
            ORDER BY common_wrong_questions DESC
            LIMIT 5
            """
            return session.run(query).data()