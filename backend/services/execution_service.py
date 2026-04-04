import subprocess
import os

class ExecutionService:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def run_python_file(self, file_name):
        """
        Run a Python file safely
        """
        file_path = os.path.join(self.repo_path, file_name)

        try:
            result = subprocess.run(
                ["python", file_path],
                capture_output=True,
                text=True,
                timeout=10
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Execution timed out"
            }