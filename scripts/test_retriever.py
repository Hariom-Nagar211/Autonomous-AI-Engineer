import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag.parser import CodeParser
from backend.rag.vector_store import VectorStore
from backend.rag.retriever import CodeRetriever, LLMPlanner

if __name__ == "__main__":
    repo_path = "repos/Whatsapp-Chat-Analyzer"

    # Step 1: Parse
    parser = CodeParser(language="python")
    parsed_data = parser.parse_repository(repo_path)

    # Step 2: Vector store
    store = VectorStore()
    store.build_index(parsed_data)

    # Step 3: Retrieve
    retriever = CodeRetriever(store)

    query = "calculate statistics and message count"
    context = retriever.retrieve(query, top_k=3)

    # Step 4: LLM planning
    planner = LLMPlanner()

    issue = "Optimize message statistics calculation and fix inefficiency"

    plan = planner.generate_plan(issue, context)

    print("\n🔥 GENERATED PLAN:\n")
    print(plan)