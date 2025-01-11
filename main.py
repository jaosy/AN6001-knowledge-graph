from knowledge_graph import ExamKnowledgeGraph
from data import mock_data
from pprint import pprint

def main():
    # connect to neo4j database
    # replace with your own credentials - neo4j is locally hosted
    graph = ExamKnowledgeGraph(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    # clear existing data
    graph.clear_database()

    # create the graph
    graph.create_graph(mock_data)

    # analyze patterns
    print("\nAnalyze students' performance by module:")
    pprint(graph.analyze_module_transitions())

    print("\nFind similar students:")
    pprint(graph.find_similar_students())

    # Close connection
    graph.close()

if __name__ == "__main__":
    main()