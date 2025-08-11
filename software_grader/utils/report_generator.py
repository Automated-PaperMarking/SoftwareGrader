import json
import os

def save_report(student_id, problem_id, score, feedback, meta=None):
    os.makedirs("reports", exist_ok=True)
    report = {
        "student_id": student_id,
        "problem_id": problem_id,
        "score": score,
        "feedback": feedback
    }
    if meta:
        report["meta"] = meta
    filename = f"reports/{student_id}_{problem_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
