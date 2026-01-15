import glob
import yaml

def load_policies(policy_dir: str = "policies"):
    policies = []
    for path in sorted(glob.glob(f"{policy_dir}/*.yml")):
        with open(path, "r", encoding="utf-8") as f:
            policies.append(yaml.safe_load(f))
    return policies
