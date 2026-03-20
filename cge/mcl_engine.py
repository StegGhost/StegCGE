import hashlib
from typing import List, Dict, Any


def normalize_code(code: str) -> str:
    return "\n".join(line.rstrip() for line in code.strip().splitlines())


def fingerprint_code(code: str) -> str:
    normalized = normalize_code(code)
    return hashlib.sha256(normalized.encode()).hexdigest()


def compare_candidates(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    candidates = [
        {"source": "gpt", "code": "...", "proposal": {...}},
        {"source": "claude", "code": "...", "proposal": {...}}
    ]
    """
    if not candidates:
        raise ValueError("No candidates provided")

    results = []

    for c in candidates:
        fp = fingerprint_code(c["code"])
        results.append({
            "source": c["source"],
            "fingerprint": fp,
            "code": c["code"],
            "proposal": c.get("proposal"),
        })

    groups = {}
    for r in results:
        groups.setdefault(r["fingerprint"], []).append(r)

    best_fp = max(groups, key=lambda k: len(groups[k]))
    consensus_group = groups[best_fp]

    return {
        "consensus_fingerprint": best_fp,
        "consensus_size": len(consensus_group),
        "total_candidates": len(candidates),
        "agreement_ratio": len(consensus_group) / len(candidates),
        "selected_code": consensus_group[0]["code"],
        "selected_sources": [x["source"] for x in consensus_group],
        "all_results": results,
    }
