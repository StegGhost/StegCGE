import hashlib
import json
from typing import List, Dict, Any


def normalize_code(code: str) -> str:
    return "\n".join(line.rstrip() for line in code.strip().splitlines())


def fingerprint_code(code: str) -> str:
    normalized = normalize_code(code)
    return hashlib.sha256(normalized.encode()).hexdigest()


def compare_candidates(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    candidates = [
        {"source": "gpt", "code": "..."},
        {"source": "claude", "code": "..."}
    ]
    """

    results = []

    for c in candidates:
        fp = fingerprint_code(c["code"])
        results.append({
            "source": c["source"],
            "fingerprint": fp,
            "code": c["code"]
        })

    groups = {}

    for r in results:
        groups.setdefault(r["fingerprint"], []).append(r)

    # Consensus = largest group
    best_fp = max(groups, key=lambda k: len(groups[k]))
    consensus_group = groups[best_fp]

    return {
        "consensus_fingerprint": best_fp,
        "consensus_size": len(consensus_group),
        "total_candidates": len(candidates),
        "agreement_ratio": len(consensus_group) / len(candidates),
        "selected_code": consensus_group[0]["code"],
        "all_results": results,
    }
