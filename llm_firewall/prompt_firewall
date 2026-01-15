from typing import Dict, Any
from .detectors import run_regex_rules
from .audit_log import write_event

def inspect_prompt(prompt: str, policies: list[Dict[str, Any]]) -> Dict[str, Any]:
    text = prompt
    all_findings = []

    for p in policies:
        if "rules" not in p:
            continue
        findings = run_regex_rules(text, p)
        all_findings.extend(findings)

    # BLOCK takes precedence
    for f in all_findings:
        if f.action == "BLOCK":
            write_event({"stage":"prompt","decision":"BLOCK","rule":f.rule_id,"match":f.match})
            return {"decision":"BLOCK","text":"This request was blocked by security policy.","findings":[f.__dict__ for f in all_findings]}

    # Apply redactions (simple approach: replace matched strings)
    redacted = text
    for f in all_findings:
        if f.action == "REDACT":
            redacted = redacted.replace(f.match, "[REDACTED]")

    decision = "ALLOW" if redacted == text else "REDACT"
    write_event({"stage":"prompt","decision":decision,"findings":len(all_findings)})
    return {"decision":decision,"text":redacted,"findings":[f.__dict__ for f in all_findings]}
