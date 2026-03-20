from typing import List, Dict, Any


def link_receipts(receipts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Adds parent_hash linkage across receipts
    """
    prev_hash = None

    for r in receipts:
        r["parent_hash"] = prev_hash
        prev_hash = r.get("receipt_hash")

    return receipts


def verify_chain(receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validates parent_hash continuity
    """
    violations = []

    prev_hash = None

    for i, r in enumerate(receipts):
        if r.get("parent_hash") != prev_hash:
            violations.append({
                "index": i,
                "type": "chain_break",
                "expected": prev_hash,
                "found": r.get("parent_hash"),
            })

        prev_hash = r.get("receipt_hash")

    return {
        "valid": len(violations) == 0,
        "violations": violations,
    }
