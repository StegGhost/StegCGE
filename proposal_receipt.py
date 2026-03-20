import hashlib
import json
import time

def record_proposal_receipt(model: str, base_state_hash: str, proposal: dict) -> dict:
    receipt = {
        "timestamp": time.time(),
        "model": model,
        "base_state_hash": base_state_hash,
        "proposal": proposal,
    }
    receipt["proposal_hash"] = hashlib.sha256(
        json.dumps(receipt, sort_keys=True).encode()
    ).hexdigest()
    return receipt
