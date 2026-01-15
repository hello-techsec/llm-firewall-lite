from typing import Dict, Any, List
from .detectors import run_regex_rules, topic_allowed
from .audit_log import write_event

def inspect_retrieval(chunks: List[str], policies: list[Dict[str, Any]]) -> Dict[str, Any]:
    topic_policy = next((p for p in policies if p.get("name") == "topic"), {"allowed_topics":[]})
    rule_policies = [p for p in policies if "rules" in p]

    kept = []
    blocked = 0
    redacted_count = 0

    for c in chunks:
        if not topic_allowed(c, topic_policy):
            blocked += 1
            continue

        findings = []
        for p in rule_policies:
            findings.extend(run_regex_rules(c, p))

        if any(f.action == "BLOCK" for f in findings):
            blocked += 1
            continue

        redacted = c
        for f in findings:
            if f.action == "REDACT":
                redacted = redacted.replace(f.match, "[REDACTED]")
        if redacted != c:
            redacted_count += 1
        kept.append(redacted)

    write_event({"stage":"retrieval","kept":len(kept),"blocked":blocked,"redacted":redacted_count})
    return {"kept":kept,"blocked":blocked,"redacted":redacted_count}
