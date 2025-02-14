from knowledge_graph import ExamKnowledgeGraph
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Optional, Dict, List, Any
import pandas as pd


class EduChatbot:
    def __init__(self) -> None:
        self.graph = ExamKnowledgeGraph(
            uri="bolt://localhost:7687", user="neo4j", password="password"
        )

        # Load NLP models
        self.nlp = spacy.load("en_core_web_sm")
        self.sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

        # Define intents (question groups) using existing graph methods
        self.intents: List[Dict[str, Any]] = [
            {
                "name": "module_transitions",
                "patterns": [
                    "How are students performing between modules?",
                    "Show module transitions",
                    "Compare module performance",
                    "How do students progress between modules?",
                    "Module to module performance",
                ],
                "handler": self._handle_module_transitions,
            },
            {
                "name": "similar_students",
                "patterns": [
                    "Find similar students",
                    "Who makes similar mistakes?",
                    "Show student similarities",
                    "Which students have common mistakes?",
                    "Group similar students",
                ],
                "handler": self._handle_similar_students,
            },
            {
                "name": "prerequisites",
                "patterns": [
                    "Show module prerequisites",
                    "What are the prerequisite relationships?",
                    "Module dependencies",
                    "Which modules are connected?",
                    "Prerequisite structure",
                ],
                "handler": self._handle_prerequisites,
            },
        ]

    def generate_welcome_message(self) -> Dict[str, Any]:
        """Dynamically generate a personalized welcome message with relevant conversation starters"""

        # Get some stats from the knowledge graph
        with self.graph.driver.session() as session:
            module_count = session.run(
                "MATCH (m:Module) RETURN count(m) as count"
            ).single()["count"]
            student_count = session.run(
                "MATCH (s:Student) RETURN count(s) as count"
            ).single()["count"]

        # Generate dynamic example questions based on actual data
        example_questions = []
        if module_count > 0:
            example_questions.extend(
                [
                    "How are students performing between modules?",
                    "Show me the prerequisite structure for all modules",
                ]
            )
        if student_count > 0:
            example_questions.append("Find students with similar mistake patterns")

        # if no data is available, use generic questions
        if not example_questions:
            example_questions = [
                pattern for intent in self.intents for pattern in intent["patterns"][:1]
            ]

        # capabilities list (that the graph can handle) from intents
        capabilities = [
            f"• {intent['name'].replace('_', ' ').title()} \t"
            for intent in self.intents
        ]

        welcome_message = {
            "role": "assistant",
            "content": f"""
                👋 Hello! I'm your Educational Analytics Assistant.

                Currently analyzing data for:
                • {module_count} modules
                • {student_count} students

                I can help you with:
                {''.join(capabilities)}

                Try asking me questions like:
                {''.join(f"{i+1}. \"{q}\" \t" for i, q in enumerate(example_questions))}

                How can I assist you today?
            """,
        }

        return welcome_message

    def get_suggested_followup(self, last_intent: Optional[str]) -> List[str]:
        """Generate contextual follow-up questions based on the last interaction"""
        if not last_intent:
            return []

        followups = {
            "module_transitions": [
                "Would you like to see the performance breakdown by specific modules?",
                "Should we analyze which transitions show the most improvement?",
                "Would you like to see related prerequisite relationships?",
            ],
            "similar_students": [
                "Would you like to focus on specific topics where students share mistakes?",
                "Should we look at recommended study groups based on these patterns?",
                "Would you like to see the most common mistake patterns?",
            ],
            "prerequisites": [
                "Would you like to see how students perform across these prerequisites?",
                "Should we analyze which prerequisite relationships are most critical?",
                "Would you like to see the success rate for different module sequences?",
            ],
        }

        return followups.get(last_intent, [])

    def get_response(self, user_input: str) -> str:
        intent = self._find_intent(user_input)
        if intent:
            return intent["handler"]()
        return (
            "I'm not sure how to help with that. Try asking about:\n"
            "- Module transitions and performance\n"
            "- Similar students and common mistakes\n"
            "- Module prerequisites and relationships"
        )

    def _find_intent(self, user_input: str) -> Optional[Dict[str, Any]]:
        input_embedding = self.sentence_model.encode([user_input])

        best_similarity = 0
        best_intent = None

        for intent in self.intents:
            pattern_embeddings = self.sentence_model.encode(intent["patterns"])
            similarity = cosine_similarity(input_embedding, pattern_embeddings)
            max_similarity = np.max(similarity)

            if max_similarity > best_similarity:
                best_similarity = max_similarity
                best_intent = intent

        return best_intent if best_similarity > 0.5 else None

    def _handle_module_transitions(self) -> str:
        """Handle queries about module transitions using your existing method"""
        results = self.graph.analyze_module_transitions()

        if not results:
            return "No module transition data available."

        # convert to DataFrame for easier handling
        df = pd.DataFrame(results)

        insights = []
        avg_prereq = df["prerequisite_score"].mean()
        avg_next = df["next_module_score"].mean()
        improved = (df["next_module_score"] > df["prerequisite_score"]).mean() * 100

        insights.append(f"📊 Module Transition Analysis:")
        insights.append(f"\n• Average prerequisite module score: {avg_prereq:.1f}%")
        insights.append(f"\n• Average following module score: {avg_next:.1f}%")
        insights.append(
            f"\n• {improved:.1f}% of students improved their scores in subsequent modules"
        )

        best_improvement = df.loc[
            (df["next_module_score"] - df["prerequisite_score"]).idxmax()
        ]
        insights.append("\n🌟 Best Improvement Example:")
        insights.append(
            f"From "
            f"{best_improvement['prerequisite_score']:.1f}% to "
            f"{best_improvement['next_module_score']:.1f}% between modules "
            f"{best_improvement['prerequisite_module']} and {best_improvement['next_module']}"
        )

        return "\n".join(insights)

    def _handle_similar_students(self) -> str:
        """Handle queries about similar students using your existing method"""
        results = self.graph.find_similar_students()

        if not results:
            return "No similar student patterns found."

        insights = ["👥 Similar Student Groups:"]

        for r in results:
            # Group similar students by their common mistakes
            mistakes_by_topic = {}
            for mistake in r["shared_mistakes"]:
                topic = mistake["topic"]
                if topic not in mistakes_by_topic:
                    mistakes_by_topic[topic] = []
                mistakes_by_topic[topic].append(mistake)

            insights.append(
                f"\nStudents {r['student1']} and {r['student2']} share error patterns in answering questions:"
            )
            for topic, mistakes in mistakes_by_topic.items():
                insights.append(f"\n{topic}:")
                for m in mistakes:
                    insights.append(
                        f"\n• {m['question']}: "
                        f"answered '{m['s1_answer']}', correct answer '{m['correct_answer']}'"
                    )

            insights.append(
                f"\nIt might be helpful for {r['student1']} and {r['student2']} to work on their weaknesses together."
            )

        return "\n".join(insights)

    def _handle_prerequisites(self) -> str:
        """Handle queries about module prerequisites"""
        with self.graph.driver.session() as session:
            result = session.run(
                """
                MATCH (m1:Module)-[r:PREREQUISITE_OF]->(m2:Module)
                RETURN m1.id as prereq, m2.id as module
                ORDER BY m1.id, m2.id
            """
            )

            prereqs = [(r["prereq"], r["module"]) for r in result]

            if not prereqs:
                return "No prerequisite relationships found."

            insights = ["📚 Module Prerequisites:"]
            for prereq, module in prereqs:
                insights.append(f"• {prereq} ➔ {module}")

            return "\n".join(insights)

    def get_visualization_data(self, intent_name: str) -> Optional[pd.DataFrame]:
        """Get data for visualization based on intent"""
        if intent_name == "module_transitions":
            results = self.graph.analyze_module_transitions()
            if results:
                return pd.DataFrame(results)
        return None

    def close(self) -> None:
        self.graph.close()
