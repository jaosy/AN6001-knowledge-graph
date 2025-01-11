mock_data = [
    # Module A (Basic) - No prerequisites
    # Topic 1 (Q1-Q2)
    {"student_id": "S1", "module_id": "A", "module_prerequisite": None, "question_id": "Q1", "student_answer": "B", "correct_answer": "A", "topic": "Topic1"},
    {"student_id": "S2", "module_id": "A", "module_prerequisite": None, "question_id": "Q1", "student_answer": "B", "correct_answer": "A", "topic": "Topic1"},
    {"student_id": "S3", "module_id": "A", "module_prerequisite": None, "question_id": "Q1", "student_answer": "A", "correct_answer": "A", "topic": "Topic1"},

    {"student_id": "S1", "module_id": "A", "module_prerequisite": None, "question_id": "Q2", "student_answer": "C", "correct_answer": "C", "topic": "Topic1"},
    {"student_id": "S2", "module_id": "A", "module_prerequisite": None, "question_id": "Q2", "student_answer": "B", "correct_answer": "C", "topic": "Topic1"},
    {"student_id": "S3", "module_id": "A", "module_prerequisite": None, "question_id": "Q2", "student_answer": "C", "correct_answer": "C", "topic": "Topic1"},

    # Topic 2 (Q3-Q4)
    {"student_id": "S1", "module_id": "A", "module_prerequisite": None, "question_id": "Q3", "student_answer": "A", "correct_answer": "A", "topic": "Topic2"},
    {"student_id": "S2", "module_id": "A", "module_prerequisite": None, "question_id": "Q3", "student_answer": "B", "correct_answer": "A", "topic": "Topic2"},
    {"student_id": "S3", "module_id": "A", "module_prerequisite": None, "question_id": "Q3", "student_answer": "A", "correct_answer": "A", "topic": "Topic2"},

    {"student_id": "S1", "module_id": "A", "module_prerequisite": None, "question_id": "Q4", "student_answer": "B", "correct_answer": "B", "topic": "Topic2"},
    {"student_id": "S2", "module_id": "A", "module_prerequisite": None, "question_id": "Q4", "student_answer": "B", "correct_answer": "B", "topic": "Topic2"},
    {"student_id": "S3", "module_id": "A", "module_prerequisite": None, "question_id": "Q4", "student_answer": "C", "correct_answer": "B", "topic": "Topic2"},

    # Module B - Requires Module A
    # Topic 3 (Q5-Q6)
    {"student_id": "S1", "module_id": "B", "module_prerequisite": "A", "question_id": "Q5", "student_answer": "B", "correct_answer": "B", "topic": "Topic3"},
    {"student_id": "S2", "module_id": "B", "module_prerequisite": "A", "question_id": "Q5", "student_answer": "A", "correct_answer": "B", "topic": "Topic3"},
    {"student_id": "S3", "module_id": "B", "module_prerequisite": "A", "question_id": "Q5", "student_answer": "B", "correct_answer": "B", "topic": "Topic3"},

    {"student_id": "S1", "module_id": "B", "module_prerequisite": "A", "question_id": "Q6", "student_answer": "A", "correct_answer": "A", "topic": "Topic3"},
    {"student_id": "S2", "module_id": "B", "module_prerequisite": "A", "question_id": "Q6", "student_answer": "B", "correct_answer": "A", "topic": "Topic3"},
    {"student_id": "S3", "module_id": "B", "module_prerequisite": "A", "question_id": "Q6", "student_answer": "A", "correct_answer": "A", "topic": "Topic3"},

    # Topic 4 (Q7-Q8)
    {"student_id": "S1", "module_id": "B", "module_prerequisite": "A", "question_id": "Q7", "student_answer": "C", "correct_answer": "C", "topic": "Topic4"},
    {"student_id": "S2", "module_id": "B", "module_prerequisite": "A", "question_id": "Q7", "student_answer": "C", "correct_answer": "C", "topic": "Topic4"},
    {"student_id": "S3", "module_id": "B", "module_prerequisite": "A", "question_id": "Q7", "student_answer": "B", "correct_answer": "C", "topic": "Topic4"},

    {"student_id": "S1", "module_id": "B", "module_prerequisite": "A", "question_id": "Q8", "student_answer": "A", "correct_answer": "A", "topic": "Topic4"},
    {"student_id": "S2", "module_id": "B", "module_prerequisite": "A", "question_id": "Q8", "student_answer": "A", "correct_answer": "A", "topic": "Topic4"},
    {"student_id": "S3", "module_id": "B", "module_prerequisite": "A", "question_id": "Q8", "student_answer": "B", "correct_answer": "A", "topic": "Topic4"},

    # Module C - Requires Module B
    # Topic 5 (Q9-Q10)
    {"student_id": "S1", "module_id": "C", "module_prerequisite": "B", "question_id": "Q9", "student_answer": "B", "correct_answer": "B", "topic": "Topic5"},
    {"student_id": "S2", "module_id": "C", "module_prerequisite": "B", "question_id": "Q9", "student_answer": "B", "correct_answer": "B", "topic": "Topic5"},
    {"student_id": "S3", "module_id": "C", "module_prerequisite": "B", "question_id": "Q9", "student_answer": "C", "correct_answer": "B", "topic": "Topic5"},

    {"student_id": "S1", "module_id": "C", "module_prerequisite": "B", "question_id": "Q10", "student_answer": "A", "correct_answer": "A", "topic": "Topic5"},
    {"student_id": "S2", "module_id": "C", "module_prerequisite": "B", "question_id": "Q10", "student_answer": "C", "correct_answer": "A", "topic": "Topic5"},
    {"student_id": "S3", "module_id": "C", "module_prerequisite": "B", "question_id": "Q10", "student_answer": "A", "correct_answer": "A", "topic": "Topic5"},

    # Topic 6 (Q11-Q12)
    {"student_id": "S1", "module_id": "C", "module_prerequisite": "B", "question_id": "Q11", "student_answer": "D", "correct_answer": "D", "topic": "Topic6"},
    {"student_id": "S2", "module_id": "C", "module_prerequisite": "B", "question_id": "Q11", "student_answer": "D", "correct_answer": "D", "topic": "Topic6"},
    {"student_id": "S3", "module_id": "C", "module_prerequisite": "B", "question_id": "Q11", "student_answer": "B", "correct_answer": "D", "topic": "Topic6"},

    {"student_id": "S1", "module_id": "C", "module_prerequisite": "B", "question_id": "Q12", "student_answer": "A", "correct_answer": "A", "topic": "Topic6"},
    {"student_id": "S2", "module_id": "C", "module_prerequisite": "B", "question_id": "Q12", "student_answer": "B", "correct_answer": "A", "topic": "Topic6"},
    {"student_id": "S3", "module_id": "C", "module_prerequisite": "B", "question_id": "Q12", "student_answer": "A", "correct_answer": "A", "topic": "Topic6"},

    # Module D - Requires Module C
    # Topic 7 (Q13-Q14)
    {"student_id": "S1", "module_id": "D", "module_prerequisite": "C", "question_id": "Q13", "student_answer": "B", "correct_answer": "B", "topic": "Topic7"},
    {"student_id": "S2", "module_id": "D", "module_prerequisite": "C", "question_id": "Q13", "student_answer": "B", "correct_answer": "B", "topic": "Topic7"},
    {"student_id": "S3", "module_id": "D", "module_prerequisite": "C", "question_id": "Q13", "student_answer": "C", "correct_answer": "B", "topic": "Topic7"},

    {"student_id": "S1", "module_id": "D", "module_prerequisite": "C", "question_id": "Q14", "student_answer": "A", "correct_answer": "A", "topic": "Topic7"},
    {"student_id": "S2", "module_id": "D", "module_prerequisite": "C", "question_id": "Q14", "student_answer": "A", "correct_answer": "A", "topic": "Topic7"},
    {"student_id": "S3", "module_id": "D", "module_prerequisite": "C", "question_id": "Q14", "student_answer": "C", "correct_answer": "A", "topic": "Topic7"},

    # Topic 8 (Q15-Q16)
    {"student_id": "S1", "module_id": "D", "module_prerequisite": "C", "question_id": "Q15", "student_answer": "B", "correct_answer": "B", "topic": "Topic8"},
    {"student_id": "S2", "module_id": "D", "module_prerequisite": "C", "question_id": "Q15", "student_answer": "C", "correct_answer": "B", "topic": "Topic8"},
    {"student_id": "S3", "module_id": "D", "module_prerequisite": "C", "question_id": "Q15", "student_answer": "B", "correct_answer": "B", "topic": "Topic8"},

    {"student_id": "S1", "module_id": "D", "module_prerequisite": "C", "question_id": "Q16", "student_answer": "A", "correct_answer": "A", "topic": "Topic8"},
    {"student_id": "S2", "module_id": "D", "module_prerequisite": "C", "question_id": "Q16", "student_answer": "B", "correct_answer": "A", "topic": "Topic8"},
    {"student_id": "S3", "module_id": "D", "module_prerequisite": "C", "question_id": "Q16", "student_answer": "A", "correct_answer": "A", "topic": "Topic8"}
]