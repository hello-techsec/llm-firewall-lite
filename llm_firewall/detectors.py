import re
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Finding(
    policy=policy_name,
    rule_id=rule["id"],
    action=rule["action"],
    severity=rule.get("severity", "MEDIUM"),
    confidence=0.9
)

def run_regex_rules(text: str, policy: Dict[str, Any]) -> List[Finding]:
    findings: List[Finding] = []
    rules = policy.get("rules", [])
    for r in rules:
        pattern = r.get("pattern")
        if not pattern:
            continue
        for m in re.finditer(pattern, text):
            findings.append(Finding(
                policy=policy.get("name", "unknown"),
                rule_id=r.get("id", "UNKNOWN_RULE"),
                action=r.get("action", "LOG_ONLY"),
                start=m.start(),
                end=m.end(),
                match=m.group(0),
            ))
    return findings

def topic_allowed(text: str, topic_policy: Dict[str, Any]) -> bool:
    allowed = [t.lower() for t in topic_policy.get("allowed_topics", [])]
    tl = text.lower()
    return any(t in tl for t in allowed) if allowed else True
