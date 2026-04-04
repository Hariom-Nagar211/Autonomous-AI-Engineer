import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag.parser import CodeParser
from backend.rag.vector_store import VectorStore
from backend.agents.graph import AIAgentSystem

if __name__ == "__main__":
    repo_path = "repos/Whatsapp-Chat-Analyzer"

    parser = CodeParser(language="python")
    parsed = parser.parse_repository(repo_path)

    store = VectorStore()
    store.build_index(parsed)

    agent = AIAgentSystem(store, repo_path)

    issue = "fix errors in helper.py file"

    result = agent.run(issue)

    print("\n🔥 DIFF:\n")
    for r in result["results"]:
        print("=" * 50)
        print("File:", r["file"])
        print(r["diff"])