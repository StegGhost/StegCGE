import hashlib
import json
from typing import Dict, Any, List, Optional

from cge.mcl_engine import compare_candidates


DEFAULT_CONSENSUS_THRESHOLD = 0.66


def normalize_proposal(proposal: dict) -> dict:
    return {
        "model": proposal.get("model"),
        "files": proposal.get("files", {})
    }


def fingerprint_proposal(proposal: dict) -> str:
    return hashlib.sha256(
        json.dumps(proposal, sort_keys=True).encode()
    ).hexdigest()


def build_candidate_from_proposal(proposal: Dict[str, Any]) -> Dict[str, Any]:
    normalized = normalize_proposal(proposal)
    files_json = json.dumps(normalized.get("files", {}), sort_keys=True, indent=2)

    return {
        "source": normalized.get("model", "unknown"),
        "code": files_json,
        "proposal": normalized,
    }


def enforce_candidate_consensus(
    raw_proposals: List[Dict[str, Any]],
    min_agreement_ratio: float = DEFAULT_CONSENSUS_THRESHOLD,
) -> Dict[str, Any]:
    if not raw_proposals:
        raise ValueError("No proposals provided")

    candidates = [build_candidate_from_proposal(p) for p in raw_proposals]
    consensus = compare_candidates(candidates)

    if consensus["agreement_ratio"] < min_agreement_ratio:
        raise RuntimeError(
            f"Insufficient LLM consensus: "
            f"{consensus['agreement_ratio']:.2f} < {min_agreement_ratio:.2f}"
        )

    selected_code = consensus["selected_code"]
    selected_proposal: Optional[Dict[str, Any]] = None

    for candidate in candidates:
        files_json = json.dumps(candidate["proposal"]["files"], sort_keys=True, indent=2)
        if files_json == selected_code:
            selected_proposal = candidate["proposal"]
            break

    if selected_proposal is None:
        raise RuntimeError("Consensus selected code could not be mapped back to a proposal")

    return {
        "selected_proposal": selected_proposal,
        "consensus": consensus,
        "min_agreement_ratio": min_agreement_ratio,
    }
