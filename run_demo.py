import json

from cge.repo_state import snapshot_repo, hash_state
from cge.proposal_engine import normalize_proposal, fingerprint_proposal
from cge.verification_engine import verify_proposal, apply_patch
from cge.consensus_engine import select_patch
from cge.receipt_engine import record_receipt


BASE = "demo/sample_repo"
PROPOSALS = [
    "demo/proposals/proposal_a.json",
    "demo/proposals/proposal_b.json",
]


def main():
    base_state = snapshot_repo(BASE)
    base_hash = hash_state(base_state)

    results = []

    for p in PROPOSALS:
        with open(p, "r", encoding="utf-8") as f:
            raw = json.load(f)

        proposal = normalize_proposal(raw)
        fp = fingerprint_proposal(proposal)

        res = verify_proposal(BASE, proposal)
        res["fp"] = fp
        results.append(res)

    selected = select_patch(results)

    # Apply selected patch BEFORE recomputing state
    apply_patch(BASE, selected["proposal"]["files"])

    # Recompute state AFTER mutation
    final_state = snapshot_repo(BASE)
    final_hash = hash_state(final_state)

    # Enforce invariant: state must change if patch is non-empty
    if selected["proposal"]["files"] and base_hash == final_hash:
        raise RuntimeError("State did not change after applying patch")

    receipt = record_receipt(
        base_hash,
        selected["fp"],
        selected,
        final_hash,
    )

    with open("cge_receipt.json", "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
