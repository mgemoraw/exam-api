"""Utility functions"""
import re 

def clean_question(line:str) -> str:
    line = line.strip()  # removes \r, \n spaces
    return re.sub(r"^\d+\s*[\.\)-\:]\s*", "", line)


def parse_text_mcq(blocks:list[str]) -> str:
    questions = []

    for block in blocks:

        lines = block.splitlines()

        options = {}
        correct_answer = None
        question_text = None

        for line in lines:
            line = line.strip()

            if re.match(r'^\d+', line):
                line = clean_question(line)
                question_text = line
            elif re.match(r"^[A-D]\)", line):
                key = line[0]
                value = line[2:].strip()
                options[key] = value

            elif line.startswith('ANSWER'):
                correct_answer = line.replace('ANSWER:', "").strip()

        if not question_text or not options or not correct_answer:
            raise ValueError(
                f"Invalid MCQ format in block:\n {block}"
            )
            
        questions.append({
            "question": question_text,
            "options": options, 
            "answer": correct_answer,
        })
        

    return questions 


# def calculate_score(db: Session, attempt_id: str):
#     attempt = db.query(ExamAttempt).filter_by(id=attempt_id).first()
#     if not attempt:
#         raise ValueError("Attempt not found")

#     total_score = 0.0

#     # iterate through answers
#     for answer in attempt.answers:
#         if answer.selected_option_id:
#             choice = db.query(Choice).filter_by(id=answer.selected_option_id).first()
#             if choice and choice.is_correct:
#                 # award marks (could be per-question weight)
#                 total_score += 1  # or question.marks if you store marks per question

#     attempt.score = total_score
#     attempt.status = "COMPLETED"
#     attempt.completed_at = datetime.utcnow()

#     db.commit()
#     db.refresh(attempt)
#     return attempt