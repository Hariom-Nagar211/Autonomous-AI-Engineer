import ollama


class CriticAgent:
    def __init__(self, model="llama3"):
        self.model = model

    def review(self, code):
        prompt = f"""
You are a code reviewer.

Check:
- syntax errors
- logical issues

Return:
- "valid" if correct
- otherwise explain issues

---

CODE:
{code}
"""

        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]