import subprocess

def run_code(code_path, input_data, timeout=2):
    try:
        result = subprocess.run(
            ["python", code_path],
            input=input_data.encode(),
            capture_output=True,
            timeout=timeout
        )
        return {
            "output": result.stdout.decode(),
            "error": result.stderr.decode(),
            "timeout": False
        }
    except subprocess.TimeoutExpired:
        return {
            "output": "",
            "error": "Execution timed out",
            "timeout": True
        }
