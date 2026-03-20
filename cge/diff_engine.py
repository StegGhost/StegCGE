def compute_diff(base_state: dict, proposal_files: dict) -> dict:
    changes = {}
    for path, content in proposal_files.items():
        changes[path] = content
    return changes

def detect_conflicts(proposals: list) -> bool:
    seen = {}
    for p in proposals:
        for k, v in p["files"].items():
            if k in seen and seen[k] != v:
                return True
            seen[k] = v
    return False
