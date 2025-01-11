
from knowledge_graph import ExamKnowledgeGraph
from data import mock_data
from pprint import pprint

def main():
    graph = ExamKnowledgeGraph(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    # Clear existing data
    graph.clear_database()

    # Create the graph
    graph.create_graph(mock_data)

    # Analyze patterns
    print("\nCommon Mistakes by Module and Topic:")
    pprint(graph.analyze_common_mistakes())

    print("\nModule Performance Overview:")
    pprint(graph.analyze_question_difficulty())

    print("\nStudent Performance by Module:")
    pprint(graph.analyze_student_module_performance())

    print("\nTopic Correlations:")
    pprint(graph.find_topic_correlations())

    print("\nFind similar students:")
    pprint(graph.find_similar_students())

    # Close connection
    graph.close()

if __name__ == "__main__":
    main()