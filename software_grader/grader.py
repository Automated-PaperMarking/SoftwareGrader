import os
import json
from utils.sandbox import run_code
from utils.report_generator import save_report

PROBLEM_PATH = "problems/Q1.json"
SUBMISSIONS_PATH = "submissions"
REPORTS_PATH = "reports"

def grade_submission(student_id, problem):
    code_path = os.path.join(SUBMISSIONS_PATH, student_id, "solution.py")
    total = len(problem['test_cases'])
    passed = 0
    feedback = []

    for idx, case in enumerate(problem['test_cases']):
        result = run_code(code_path, case['input'], timeout=problem['timeout'])
        expected = case['output'].strip()
        output = result["output"].strip()

        if result["timeout"]:
            feedback.append(f"❌ Test {idx+1}: Timeout")
        elif output == expected:
            passed += 1
            feedback.append(f"✅ Test {idx+1}: Passed")
        else:
            feedback.append(f"❌ Test {idx+1}: Failed – Expected `{expected}`, Got `{output}`")

    score = round((passed / total) * problem['marks'])
    save_report(student_id, problem['problem_id'], score, feedback)
    print(f"{student_id}: {score}/{problem['marks']}")

def main():
    with open(PROBLEM_PATH) as f:
        problem = json.load(f)

    students = os.listdir(SUBMISSIONS_PATH)
    for student_id in students:
        grade_submission(student_id, problem)

if __name__ == "__main__":
    main()
