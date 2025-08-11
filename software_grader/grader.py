import os
import json
from utils.sandbox import find_submission_file, run_code
from utils.report_generator import save_report

PROBLEM_PATH = "problems/Q1.json"
SUBMISSIONS_PATH = "submissions"

def compare_output(actual, expected):
    # strip whitespace/newlines from ends, compare exact otherwise
    if actual is None:
        actual = ""
    if expected is None:
        expected = ""
    return actual.strip() == expected.strip()

def grade_submission(student_id, problem):
    student_folder = os.path.join(SUBMISSIONS_PATH, student_id)
    submission = find_submission_file(student_folder)
    feedback = []
    score = 0
    meta = {}

    if submission is None:
        feedback.append("❌ No supported submission file found (supported: .py, .java, .c, .cpp, .cs)")
        save_report(student_id, problem["problem_id"], 0, feedback, meta)
        print(f"{student_id}: 0/{problem['marks']}  (no file)")
        return

    # Run each test case
    total = len(problem["test_cases"])
    marks_per_case = problem["marks"] / total if total > 0 else 0
    passed = 0

    for idx, tc in enumerate(problem["test_cases"], start=1):
        inp = tc.get("input", "")
        expected = tc.get("output", "")

        result = run_code(submission, inp, timeout=problem.get("timeout", 2))

        if result.get("compile_error"):
            feedback.append(f"❌ Test {idx}: Compilation error: {result.get('error', '').strip()}")
            meta["compile_error"] = True
            # once compile failed, further tests will also fail; break to avoid repetitive errors
            break

        if result.get("timeout"):
            feedback.append(f"❌ Test {idx}: Timeout after {problem.get('timeout', 2)}s")
            continue

        stderr = result.get("error", "").strip()
        stdout = result.get("output", "")

        if stderr:
            # runtime warnings/errors but may still produce output; record them
            feedback.append(f"⚠ Test {idx}: Runtime stderr: {stderr}")

        if compare_output(stdout, expected):
            passed += 1
            feedback.append(f"✅ Test {idx}: Passed")
        else:
            feedback.append(f"❌ Test {idx}: Failed — Expected `{expected.strip()}`, Got `{stdout.strip()}`")

    score = round((passed / total) * problem["marks"]) if total > 0 else 0
    save_report(student_id, problem["problem_id"], score, feedback, meta)
    print(f"{student_id}: {score}/{problem['marks']}")

def main():
    with open(PROBLEM_PATH, "r", encoding="utf-8") as f:
        problem = json.load(f)

    if not os.path.isdir(SUBMISSIONS_PATH):
        print("No submissions folder found. Create `submissions/` with student folders.")
        return

    students = sorted([d for d in os.listdir(SUBMISSIONS_PATH) if os.path.isdir(os.path.join(SUBMISSIONS_PATH, d))])
    if not students:
        print("No student submission folders found inside `submissions/`.")
        return

    for student in students:
        grade_submission(student, problem)

if __name__ == "__main__":
    main()
