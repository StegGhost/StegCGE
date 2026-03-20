import hashlib
import json
import time
from typing import Dict, Any


def record_code_receipt(consensus_result: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "timestamp": time.time(),
        "consensus_fingerprint": consensus_result["consensus_fingerprint"],
        "consensus_size": consensus_result["consensus_size"],
        "agreement_ratio": consensus_result["agreement_ratio"],
        "selected_sources": consensus_result.get("selected_sources", []),
        "total_candidates": consensus_result["total_candidates"],
    }

    payload_str = json.dumps(payload, sort_keys=True)
    payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()

    payload["receipt_hash"] = payload_hash
    return payload
