import hashlib
import json
import time
from typing import Dict, Any


def record_receipt(
    base_hash: str,
    proposal_fp: str,
    selected: Dict[str, Any],
    final_hash: str,
    parent_hash: str = None,
) -> Dict[str, Any]:

    payload = {
        "timestamp": time.time(),
        "base_state": base_hash,
        "selected_proposal": proposal_fp,
        "final_state": final_hash,
        "selected": selected,
        "parent_hash": parent_hash,
    }

    payload_str = json.dumps(payload, sort_keys=True)
    receipt_hash = hashlib.sha256(payload_str.encode()).hexdigest()

    payload["receipt_hash"] = receipt_hash
    return payload
