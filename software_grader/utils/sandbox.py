import os
import re
import shutil
import subprocess
import tempfile

SUPPORTED_EXT = {
    ".py": "python",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cs": "csharp"
}

def detect_language(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return SUPPORTED_EXT.get(ext)

def find_submission_file(student_folder):
    # returns the first supported file found, or None
    for fname in os.listdir(student_folder):
        path = os.path.join(student_folder, fname)
        if os.path.isfile(path):
            if detect_language(path):
                return path
    return None

def get_java_class_name(file_path):
    """Return public class name if present, else first class name, else None"""
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    m = re.search(r"public\s+class\s+([A-Za-z_]\w*)", code)
    if m:
        return m.group(1)
    m = re.search(r"class\s+([A-Za-z_]\w*)", code)
    return m.group(1) if m else None

def run_code(file_path, input_data, timeout=2):
    """
    Returns dict: { output, error, timeout (bool), compile_error (bool) }
    """
    lang = detect_language(file_path)
    if not lang:
        return {"output": "", "error": "Unsupported language/extension", "timeout": False, "compile_error": True}

    # Ensure input ends with newline (helps Scanner/cin)
    if input_data is None:
        input_data = ""
    if not input_data.endswith("\n"):
        input_data = input_data + "\n"

    tmpdir = None
    try:
        if lang == "python":
            proc = subprocess.run(
                ["python", file_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {"output": proc.stdout, "error": proc.stderr, "timeout": False, "compile_error": False}

        elif lang == "java":
            tmpdir = tempfile.mkdtemp()
            fname = os.path.basename(file_path)
            dst = os.path.join(tmpdir, fname)
            shutil.copy(file_path, dst)

            class_name = get_java_class_name(dst)
            if not class_name:
                return {"output": "", "error": "No class found in Java file", "timeout": False, "compile_error": True}

            # Compile
            compile_proc = subprocess.run(
                ["javac", fname],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if compile_proc.returncode != 0:
                return {"output": "", "error": compile_proc.stderr, "timeout": False, "compile_error": True}

            # Run using classpath of tmpdir
            run_proc = subprocess.run(
                ["java", "-cp", tmpdir, class_name],
                cwd=tmpdir,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {"output": run_proc.stdout, "error": run_proc.stderr, "timeout": False, "compile_error": False}

        elif lang in ("c", "cpp"):
            tmpdir = tempfile.mkdtemp()
            fname = os.path.basename(file_path)
            dst = os.path.join(tmpdir, fname)
            shutil.copy(file_path, dst)
            exe_path = os.path.join(tmpdir, "a.out")

            compiler = "gcc" if lang == "c" else "g++"
            compile_proc = subprocess.run(
                [compiler, dst, "-o", exe_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if compile_proc.returncode != 0:
                return {"output": "", "error": compile_proc.stderr, "timeout": False, "compile_error": True}

            run_proc = subprocess.run(
                [exe_path],
                cwd=tmpdir,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {"output": run_proc.stdout, "error": run_proc.stderr, "timeout": False, "compile_error": False}

        elif lang == "csharp":
            tmpdir = tempfile.mkdtemp()
            fname = os.path.basename(file_path)
            dst = os.path.join(tmpdir, fname)
            shutil.copy(file_path, dst)
            exe_path = os.path.join(tmpdir, "Program.exe")  # mcs supports any name

            compile_proc = subprocess.run(
                ["mcs", "-out:" + exe_path, dst],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if compile_proc.returncode != 0:
                return {"output": "", "error": compile_proc.stderr, "timeout": False, "compile_error": True}

            run_proc = subprocess.run(
                ["mono", exe_path],
                cwd=tmpdir,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {"output": run_proc.stdout, "error": run_proc.stderr, "timeout": False, "compile_error": False}

        else:
            return {"output": "", "error": "Language handler not implemented", "timeout": False, "compile_error": True}

    except subprocess.TimeoutExpired:
        return {"output": "", "error": "Execution timed out", "timeout": True, "compile_error": False}
    except Exception as e:
        return {"output": "", "error": f"Unexpected error: {e}", "timeout": False, "compile_error": True}
    finally:
        if tmpdir and os.path.isdir(tmpdir):
            try:
                shutil.rmtree(tmpdir)
            except Exception:
                pass
