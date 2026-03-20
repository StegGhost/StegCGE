from typing import List, Dict, Any

from cge.repo_state import snapshot_repo, hash_state
from cge.verification_engine import apply_patch


def replay_chain(base_path: str, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Replays execution deterministically from receipts
    """

    for r in receipts:
        proposal = r.get("selected", {}).get("proposal", {})
        files = proposal.get("files", {})

        if files:
            apply_patch(base_path, files)

    final_state = snapshot_repo(base_path)
    final_hash = hash_state(final_state)

    return {
        "status": "ok",
        "final_state_hash": final_hash,
    }
