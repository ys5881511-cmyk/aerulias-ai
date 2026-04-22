from agents.pipeline import run_pipeline
import json


query = "Explain machine learning in simple terms"

result = run_pipeline(query, max_rounds=2, target_score=90)

print("\nPIPELINE OUTPUT:\n")
print(json.dumps(result, indent=2))
