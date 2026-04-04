# Groq API Integration Guide

## Setup

### 1. Get Your Groq API Key
- Visit [https://console.groq.com](https://console.groq.com)
- Create an account and get your API key
- Keep it safe!

### 2. Set Environment Variable
```bash
# Windows (PowerShell)
$env:GROQ_API_KEY = "your_api_key_here"

# Windows (Command Prompt)
set GROQ_API_KEY=your_api_key_here

# Linux/Mac
export GROQ_API_KEY=your_api_key_here
```

Or create a `.env` file in your project root:
```
GROQ_API_KEY=your_api_key_here
```

### 3. Install Package
```bash
pip install -r requirements.txt
```

---

## Usage Examples

### Basic Usage
```python
from backend.utils import get_groq_client

# Create client (uses GROQ_API_KEY from environment)
groq = get_groq_client()

# Simple chat
response = groq.chat_with_system(
    user_message="Explain how to use Groq API",
    system_message="You are a helpful assistant"
)
print(response)
```

### In Code Agent
```python
from backend.utils import get_groq_client

class CodeAgent:
    def __init__(self, repo_path, use_groq=True, groq_api_key=None):
        self.repo_path = repo_path
        self.use_groq = use_groq
        
        if use_groq:
            self.groq = get_groq_client(api_key=groq_api_key)
    
    def modify_code(self, file_name, instruction):
        file_path = os.path.join(self.repo_path, file_name)
        
        with open(file_path, "r", encoding="utf-8") as f:
            original_code = f.read()
        
        prompt = f"""
Return ONLY valid Python code.

STRICT RULES:
- NO explanation
- NO markdown
- NO ``` 
- NO text before or after code
- ONLY raw Python code

INSTRUCTION:
{instruction}

FUNCTION:
{original_code}
"""
        
        if self.use_groq:
            response = self.groq.chat_with_system(
                user_message=prompt,
                system_message="You are a Python code expert. Return ONLY valid code."
            )
        else:
            import ollama
            res = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )
            response = res["message"]["content"]
        
        return response
```

### In Planner Agent
```python
from backend.utils import get_groq_client

class LLMPlanner:
    def __init__(self, use_groq=True, groq_api_key=None):
        self.use_groq = use_groq
        if use_groq:
            self.groq = get_groq_client(api_key=groq_api_key)
    
    def generate_plan(self, issue: str, context: List[Dict]) -> Dict:
        prompt = f"""
You are an expert software engineer.

ISSUE:
{issue}

Return ONLY JSON...
"""
        
        if self.use_groq:
            content = self.groq.chat_with_system(
                user_message=prompt,
                system_message="Return ONLY valid JSON, no explanation"
            )
        else:
            import ollama
            res = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )
            content = res["message"]["content"]
        
        return json.loads(content)
```

### In Critic Agent
```python
from backend.utils import get_groq_client

class CriticAgent:
    def __init__(self, use_groq=True, groq_api_key=None):
        self.use_groq = use_groq
        if use_groq:
            self.groq = get_groq_client(api_key=groq_api_key)
    
    def review(self, code):
        prompt = f"""
You are a code reviewer.

Check:
- syntax errors
- logical issues

Return:
- "valid" if correct
- otherwise explain issues

CODE:
{code}
"""
        
        if self.use_groq:
            return self.groq.chat_with_system(
                user_message=prompt,
                system_message="You are an expert code reviewer"
            )
        else:
            import ollama
            res = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )
            return res["message"]["content"]
```

---

## Available Models

Popular Groq models:
- `mixtral-8x7b-32768` (default) - Fast, powerful
- `llama2-70b-4096` - Good for reasoning
- `gemma-7b-it` - Efficient and fast

---

## Cost Optimization

- Groq API is **free** during beta
- Monitor your usage on console.groq.com
- Use `max_tokens` parameter to control response length
- Adjust `temperature` for different use cases (0=deterministic, 2=creative)

---

## Troubleshooting

### "GROQ_API_KEY not provided"
Make sure environment variable is set before running:
```bash
$env:GROQ_API_KEY = "your_key"
python your_script.py
```

### Rate Limiting
If you hit rate limits, Groq will return an error. Just retry after a short delay.

### Response Format
Some models may format responses differently. Adjust parsing as needed in your code.
