from backend.services.execution_service import ExecutionService
from backend.agents.code_agent import CodeAgent


class SelfHealingAgent:
    def __init__(self, repo_path, model="llama3"):
        self.executor = ExecutionService(repo_path)
        self.code_agent = CodeAgent(repo_path, model)

    def fix_code(self, file_name, instruction, max_attempts=3):
        """
        Try fixing code until it works
        """

        for attempt in range(max_attempts):
            print(f"\n🔁 Attempt {attempt + 1}")

            # Step 1: Modify code
            result = self.code_agent.modify_code(file_name, instruction)

            if "error" in result:
                continue

            # Step 2: Execute
            exec_result = self.executor.run_python_file(file_name)

            if exec_result["success"]:
                print("✅ Code works!")
                return {
                    "status": "success",
                    "attempts": attempt + 1,
                    "output": exec_result["stdout"]
                }

            # Step 3: Feed error back to LLM
            error_msg = exec_result.get("stderr", "")

            print("❌ Error detected:")
            print(error_msg)

            instruction = f"""
Fix the following error:

{error_msg}

Original task:
{instruction}
"""

        return {
            "status": "failed",
            "attempts": max_attempts
        }