# import streamlit as st
# import os
# import json
# from pathlib import Path
# import subprocess

# PROBLEM_DIR = "problems"
# SUBMISSION_DIR = "submissions"

# st.title("AI Software Grader")

# # 1. Create new problem
# st.header("Add a Problem")
# problem_id = st.text_input("Problem ID (e.g., Q1)")
# language = st.selectbox("Language", ["auto", "python", "java", "c", "c++", "c#"])
# marks = st.number_input("Total Marks", min_value=1, value=10)
# timeout = st.number_input("Timeout (seconds)", min_value=1, value=5)

# test_cases = st.text_area("Test Cases (one per line, format: input|output)", 
#                           "5|25\n10|100\n0|0")

# if st.button("Save Problem"):
#     if problem_id:
#         problem_path = Path(PROBLEM_DIR) / problem_id
#         problem_path.mkdir(parents=True, exist_ok=True)

#         # Convert test cases to JSON
#         test_cases_json = []
#         for line in test_cases.splitlines():
#             if "|" in line:
#                 inp, out = line.split("|", 1)
#                 test_cases_json.append({"input": inp.strip(), "output": out.strip()})

#         problem_json = {
#             "problem_id": problem_id,
#             "language": language,
#             "marks": marks,
#             "timeout": timeout,
#             "test_cases": test_cases_json
#         }

#         with open(problem_path / "problem.json", "w") as f:
#             json.dump(problem_json, f, indent=4)

#         st.success(f"Problem {problem_id} saved!")

# # 2. Select problem for grading
# st.header("Evaluate Submissions")
# selected_problem = st.selectbox("Select Problem", os.listdir(PROBLEM_DIR))
# submission_folder = st.text_input("Submission Folder Path", value=SUBMISSION_DIR)

# if st.button("Evaluate"):
#     problem_json_path = Path(PROBLEM_DIR) / selected_problem / "problem.json"
#     if problem_json_path.exists():
#         # Call your grading script
#         cmd = ["python", "grader.py", str(problem_json_path), submission_folder]
#         try:
#             result = subprocess.run(cmd, capture_output=True, text=True)
#             st.text("Grading Output:")
#             st.code(result.stdout)
#             if result.stderr:
#                 st.error(result.stderr)
#         except Exception as e:
#             st.error(str(e))
#     else:
#         st.error("Problem JSON not found.")


import streamlit as st
import os
import json
from pathlib import Path
import subprocess

# Directories
PROBLEM_DIR = "problems"
SUBMISSION_DIR = "submissions"

st.set_page_config(page_title="AI Software Grader", layout="wide")
st.title("AI Software Grader - Multi-language")

# ================== Add a Problem ==================
st.header("Add a New Problem")

with st.form("add_problem_form"):
    problem_id = st.text_input("Problem ID (e.g., Q1)")
    language = st.selectbox("Language", ["auto", "python", "java", "c", "c++", "c#"])
    marks = st.number_input("Total Marks", min_value=1, value=10)
    timeout = st.number_input("Timeout (seconds)", min_value=1, value=5)
    test_cases_text = st.text_area(
        "Test Cases (one per line, format: input|output)",
        "5|25\n10|100\n0|0"
    )
    submit_button = st.form_submit_button("Save Problem")

    if submit_button:
        if problem_id.strip() == "":
            st.warning("Problem ID cannot be empty.")
        else:
            # Ensure problems folder exists
            Path(PROBLEM_DIR).mkdir(parents=True, exist_ok=True)

            # Parse test cases
            test_cases_json = []
            for line in test_cases_text.splitlines():
                if "|" in line:
                    inp, out = line.split("|", 1)
                    test_cases_json.append({"input": inp.strip(), "output": out.strip()})

            problem_json = {
                "problem_id": problem_id,
                "language": language,
                "marks": marks,
                "timeout": timeout,
                "test_cases": test_cases_json
            }

            # Save JSON directly in problems/ as <problem_id>.json
            problem_json_file = Path(PROBLEM_DIR) / f"{problem_id}.json"
            with open(problem_json_file, "w") as f:
                json.dump(problem_json, f, indent=4)
            st.success(f"Problem '{problem_id}' saved successfully at {problem_json_file}")

# ================== Evaluate Submissions ==================
st.header("Evaluate Submissions")

# List all problem JSON files
if os.path.exists(PROBLEM_DIR):
    problems_list = [f for f in os.listdir(PROBLEM_DIR) if f.endswith(".json")]
    if problems_list:
        selected_problem = st.selectbox("Select Problem", problems_list)
    else:
        st.warning("No problems found. Please add a problem first.")
        selected_problem = None
else:
    st.warning("No problems folder found. Please add a problem first.")
    selected_problem = None

# Submission folder selection
submission_folder = st.text_input("Submission Folder Path", value=SUBMISSION_DIR)

if st.button("Evaluate"):
    if selected_problem is None:
        st.warning("Select a problem first!")
    else:
        problem_json_path = Path(PROBLEM_DIR) / selected_problem
        if not problem_json_path.exists():
            st.error(f"Problem JSON not found at {problem_json_path}")
        elif not os.path.exists(submission_folder):
            st.error(f"Submission folder not found: {submission_folder}")
        else:
            # Run grading script
            cmd = ["python", "grader.py", str(problem_json_path), submission_folder]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                st.subheader("Grading Output")
                st.code(result.stdout)
                if result.stderr:
                    st.error(result.stderr)

                # Optionally display report.json if grader outputs it
                report_path = Path(submission_folder) / "report.json"
                if report_path.exists():
                    with open(report_path, "r", encoding="utf-8") as f:
                        report_data = json.load(f)
                    st.subheader("Results Table")
                    st.table([
                        {
                            "Student ID": r.get("student_id"),
                            "Problem": r.get("problem_id"),
                            "Score": r.get("score"),
                            "Feedback": "\n".join(r.get("feedback", []))
                        } for r in report_data
                    ])
            except Exception as e:
                st.error(f"Error running grader: {str(e)}")
