from fastapi import FastAPI
from pydantic import BaseModel

from llm_firewall.policy_loader import load_policies
from llm_firewall.prompt_firewall import inspect_prompt
from llm_firewall.retrieval_firewall import inspect_retrieval
from llm_firewall.response_firewall import inspect_response
from demo.sample_docs import SAMPLE_DOCS

app = FastAPI(title="LLM Firewall Lite")

class ChatRequest(BaseModel):
    prompt: str

def fake_llm(prompt: str, context: list[str]) -> str:
    return f"Answer based on context: {context[:1]} | Prompt: {prompt}"

@app.post("/chat")
def chat(req: ChatRequest):
    policies = load_policies()

    p = inspect_prompt(req.prompt, policies)
    if p["decision"] == "BLOCK":
        return {"decision":"BLOCK","output":p["text"],"findings":p["findings"]}

    r = inspect_retrieval(SAMPLE_DOCS, policies)
    resp = fake_llm(p["text"], r["kept"])

    out = inspect_response(resp, policies)
    return {"decision":out["decision"],"output":out["text"],"findings":out["findings"]}
