import json
import time
import hashlib

def record_receipt(base_hash, proposal_fp, selected, final_hash):
    receipt = {
        "timestamp": time.time(),
        "base_state": base_hash,
        "selected_proposal": proposal_fp,
        "final_state": final_hash
    }

    receipt["receipt_hash"] = hashlib.sha256(
        json.dumps(receipt, sort_keys=True).encode()
    ).hexdigest()

    return receipt
