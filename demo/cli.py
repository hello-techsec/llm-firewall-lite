import argparse
from llm_firewall.policy_loader import load_policies
from llm_firewall.prompt_firewall import inspect_prompt
from llm_firewall.retrieval_firewall import inspect_retrieval
from llm_firewall.response_firewall import inspect_response
from demo.sample_docs import SAMPLE_DOCS

def fake_llm(prompt: str, context: list[str]) -> str:
    # Demo only: echo back
    return f"Answer based on context: {context[:1]} | Prompt: {prompt}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    args = ap.parse_args()

    policies = load_policies()

    p = inspect_prompt(args.prompt, policies)
    if p["decision"] == "BLOCK":
        print(p["text"])
        return

    r = inspect_retrieval(SAMPLE_DOCS, policies)
    resp = fake_llm(p["text"], r["kept"])

    out = inspect_response(resp, policies)
    print(out["text"])

if __name__ == "__main__":
    main()
