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
        # This query remains the same as it already handles modules
        query = """
        MERGE (s:Student {id: $student_id})
        MERGE (q:Question {id: $question_id, topic: $topic})
        MERGE (m:Module {id: $module_id})
        CREATE (s)-[:ATTEMPTED {
            student_answer: $student_answer,
            correct_answer: $correct_answer,
            is_correct: $student_answer = $correct_answer
        }]->(q)
        MERGE (q)-[:BELONGS_TO]->(m)
        """
        tx.run(query, **record)

    def analyze_common_mistakes(self):
        with self.driver.session() as session:
            # Enhanced to include module information
            query = """
            MATCH (s:Student)-[a:ATTEMPTED]->(q:Question)-[:BELONGS_TO]->(m:Module)
            WHERE a.student_answer <> a.correct_answer
            RETURN m.id as module,
                   q.topic as topic, 
                   q.id as question,
                   a.student_answer as wrong_answer,
                   COUNT(*) as frequency
            ORDER BY frequency DESC
            """
            return session.run(query).data()

    def find_related_questions(self):
        with self.driver.session() as session:
            query = """
            MATCH (s:Student)-[a1:ATTEMPTED]->(q1:Question)-[:BELONGS_TO]->(m1:Module)
            MATCH (s:Student)-[a2:ATTEMPTED]->(q2:Question)-[:BELONGS_TO]->(m2:Module)
            WHERE q1.id < q2.id 
            AND a1.is_correct = false 
            AND a2.is_correct = false
            RETURN m1.id as module1,
                   m2.id as module2,
                   q1.topic as topic1,
                   q2.topic as topic2,
                   COUNT(*) as correlation
            ORDER BY correlation DESC
            """
            return session.run(query).data()

    # New methods to analyze module-specific patterns
    def analyze_question_difficulty(self):
        with self.driver.session() as session:
            query = """
            MATCH (q:Question)-[:BELONGS_TO]->(m:Module)
            MATCH (s:Student)-[a:ATTEMPTED]->(q)
            WITH q, m,
                COUNT(a) as total_attempts,
                SUM(CASE WHEN a.is_correct THEN 1 ELSE 0 END) as correct_answers
            WHERE total_attempts >= 5  // Only consider questions with meaningful sample size
            RETURN 
                q.topic as topic,
                m.id as module,
                total_attempts as number_of_students,
                correct_answers as students_correct,
                total_attempts - correct_answers as students_wrong,
                ROUND(100.0 * correct_answers / total_attempts) as success_rate
            ORDER BY success_rate ASC
            LIMIT 10
            """
            return session.run(query).data()

    def analyze_student_module_performance(self):
        with self.driver.session() as session:
            query = """
            MATCH (s:Student)-[a:ATTEMPTED]->(q:Question)-[:BELONGS_TO]->(m:Module)
            RETURN s.id as student,
                   m.id as module,
                   COUNT(a) as questions_attempted,
                   SUM(CASE WHEN a.is_correct THEN 1 ELSE 0 END) as correct_answers
            ORDER BY student, module
            """
            return session.run(query).data()

    def find_topic_correlations(self):
        with self.driver.session() as session:
            query = """
            MATCH (q1:Question)-[:BELONGS_TO]->(m1:Module)
            MATCH (q2:Question)-[:BELONGS_TO]->(m2:Module)
            WHERE q1.topic < q2.topic
            MATCH (s:Student)-[a1:ATTEMPTED]->(q1)
            MATCH (s:Student)-[a2:ATTEMPTED]->(q2)
            WHERE a1.is_correct = false AND a2.is_correct = false
            RETURN q1.topic as topic1,
                   q2.topic as topic2,
                   COUNT(*) as correlation,
                   COLLECT(DISTINCT s.id) as students
            ORDER BY correlation DESC
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