import os
import ollama
import difflib


class CodeAgent:
    def __init__(self, repo_path, model="llama3"):
        self.repo_path = repo_path
        self.model = model

        

    def modify_code(self, file_name, instruction):
        file_path = os.path.join(self.repo_path, file_name)

        # 🔹 Step 1: Read original code
        with open(file_path, "r", encoding="utf-8") as f:
            original_code = f.read()

        # 🔹 Step 2: LLM prompt (VERY IMPORTANT)
        prompt = f"""
    Return ONLY valid Python code.

    STRICT RULES:
    - NO explanation
    - NO markdown
    - NO ``` 
    - NO text before or after code
    - ONLY raw Python code

    If you violate this, the output is invalid.

    ---

    INSTRUCTION:
    {instruction}

    ---

    FUNCTION:
    {original_code}
    """

        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        updated_code = response["message"]["content"]

        # 🔹 Step 3: Generate diff
        diff = list(
            difflib.unified_diff(
                original_code.splitlines(),
                updated_code.splitlines(),
                fromfile="before.py",
                tofile="after.py",
                lineterm=""
            )
        )

        # 🔹 Step 4: Save updated code
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_code)

        return {
            "file": file_name,
            "diff": "\n".join(diff),
            "updated_code": updated_code
        }
    

    
