import hashlib
import json

def normalize_proposal(proposal: dict) -> dict:
    return {
        "model": proposal.get("model"),
        "files": proposal.get("files", {})
    }

def fingerprint_proposal(proposal: dict) -> str:
    return hashlib.sha256(
        json.dumps(proposal, sort_keys=True).encode()
    ).hexdigest()
