from typing import Dict, Any
from .detectors import run_regex_rules
from .audit_log import write_event

def inspect_response(response: str, policies: list[Dict[str, Any]]) -> Dict[str, Any]:
    rule_policies = [p for p in policies if "rules" in p]
    findings = []
    for p in rule_policies:
        findings.extend(run_regex_rules(response, p))

    if any(f.action == "BLOCK" for f in findings):
        write_event({"stage":"response","decision":"BLOCK","findings":len(findings)})
        return {"decision":"BLOCK","text":"Response blocked by security policy.","findings":[f.__dict__ for f in findings]}

    redacted = response
    for f in findings:
        if f.action == "REDACT":
            redacted = redacted.replace(f.match, "[REDACTED]")

    decision = "ALLOW" if redacted == response else "REDACT"
    write_event({"stage":"response","decision":decision,"findings":len(findings)})
    return {"decision":decision,"text":redacted,"findings":[f.__dict__ for f in findings]}
