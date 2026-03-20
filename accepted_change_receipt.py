import hashlib
import json
import time

def record_accepted_change(base_state_hash: str, accepted_patch: dict, final_state_hash: str) -> dict:
    receipt = {
        "timestamp": time.time(),
        "base_state_hash": base_state_hash,
        "accepted_patch": accepted_patch,
        "final_state_hash": final_state_hash,
    }
    receipt["receipt_hash"] = hashlib.sha256(
        json.dumps(receipt, sort_keys=True).encode()
    ).hexdigest()
    return receipt
