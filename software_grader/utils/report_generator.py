import json
import os

def save_report(student_id, problem_id, score, feedback):
    os.makedirs("reports", exist_ok=True)
    report = {
        "student_id": student_id,
        "problem_id": problem_id,
        "score": score,
        "feedback": feedback
    }
    with open(f"reports/{student_id}_{problem_id}.json", "w") as f:
        json.dump(report, f, indent=4)
