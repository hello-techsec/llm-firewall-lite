from llm_firewall.policy_loader import load_policies
from llm_firewall.response_firewall import inspect_response

def test_redacts_secrets_in_response():
    policies = load_policies()
    res = inspect_response("Leaked token apiKey-sk_TEST1234567890", policies)
    assert "apiKey-sk_TEST1234567890" not in res["text"]
