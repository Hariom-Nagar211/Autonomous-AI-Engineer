from backend.agents.planner import PlannerAgent
from backend.agents.retriever_agent import RetrieverAgent
from backend.agents.self_healing import SelfHealingAgent

class AIAgentSystem:
    def __init__(self, vector_store, repo_path):
        self.retriever = RetrieverAgent(vector_store)
        self.planner = PlannerAgent()
        self.healer = SelfHealingAgent(repo_path)

    def run(self, issue):
        context = self.retriever.run(issue)
        plan = self.planner.run(issue, context)

        # Handle error in plan generation
        if not isinstance(plan, dict) or "files_likely" not in plan:
            return {
                "plan": plan,
                "results": [],
                "error": plan.get("error", "Plan did not contain 'files_likely'") if isinstance(plan, dict) else "Plan is not a dict"
            }

        results = []

        for file in plan["files_likely"]:
            result = self.healer.fix_code(
                file,
                plan.get("problem", "")
            )

            results.append({
                "file": file,
                "result": result
            })

        return {
            "plan": plan,
            "results": results
        }