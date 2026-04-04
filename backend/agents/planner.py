from typing import List, Dict
import ollama
import os
import json
import re


class LLMPlanner:
    def __init__(self, model: str = "llama3"):
        self.model = model

    def generate_plan(self, issue: str, context: List[Dict]) -> Dict:

        files = list(set([
            os.path.basename(c["file"]) for c in context
        ]))

        code_context = "\n\n".join(
            [f"FILE: {os.path.basename(c['file'])}\n{c['code'][:500]}" for c in context]
        )

        prompt = f"""
You are an expert software engineer.

IMPORTANT RULES:
- ONLY use files from the provided context
- DO NOT invent new file names

Available files:
{files}

---

ISSUE:
{issue}

---

CODE CONTEXT:
{code_context}

---

Return ONLY JSON:

{{
  "problem": "...",
  "files_likely": ["choose only from available files"],
  "steps": ["analyze", "fix", "test"]
}}
"""

        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response["message"]["content"]

        def extract_json(text):
            match = re.search(r"\{.*\}", text, re.DOTALL)
            return match.group() if match else text

        cleaned = extract_json(content)

        try:
            parsed = json.loads(cleaned)

            valid_files = set(files)
            parsed["files_likely"] = [
                f for f in parsed.get("files_likely", [])
                if f in valid_files
            ]

            if not parsed["files_likely"]:
                parsed["files_likely"] = list(valid_files)[:1]

            return parsed

        except:
            return {"error": cleaned}


class PlannerAgent:
    def __init__(self):
        self.planner = LLMPlanner()

    def run(self, issue, context):
        return self.planner.generate_plan(issue, context)