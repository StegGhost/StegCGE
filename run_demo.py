import json

from cge.repo_state import snapshot_repo, hash_state
from cge.proposal_engine import (
    normalize_proposal,
    fingerprint_proposal,
    enforce_candidate_consensus,
)
from cge.verification_engine import verify_proposal, apply_patch
from cge.consensus_engine import select_patch
from cge.receipt_engine import record_receipt
from cge.code_receipt import record_code_receipt


BASE = "demo/sample_repo"
PROPOSALS = [
    "demo/proposals/proposal_a.json",
    "demo/proposals/proposal_b.json",
]


def main():
    base_state = snapshot_repo(BASE)
    base_hash = hash_state(base_state)

    raw_proposals = []
    results = []

    for p in PROPOSALS:
        with open(p, "r", encoding="utf-8") as f:
            raw = json.load(f)
        raw_proposals.append(raw)

    consensus_gate = enforce_candidate_consensus(raw_proposals, min_agreement_ratio=0.50)
    selected_consensus_proposal = consensus_gate["selected_proposal"]
    code_receipt = record_code_receipt(consensus_gate["consensus"])

    for raw in raw_proposals:
        proposal = normalize_proposal(raw)
        fp = fingerprint_proposal(proposal)

        res = verify_proposal(BASE, proposal)
        res["fp"] = fp
        res["source_model"] = proposal.get("model")
        results.append(res)

    filtered_results = []
    selected_files = selected_consensus_proposal["files"]

    for res in results:
        if res["proposal"]["files"] == selected_files:
            filtered_results.append(res)

    if not filtered_results:
        raise RuntimeError("Consensus-selected proposal was not present in verification results")

    selected = select_patch(filtered_results)

    apply_patch(BASE, selected["proposal"]["files"])

    final_state = snapshot_repo(BASE)
    final_hash = hash_state(final_state)

    if selected["proposal"]["files"] and base_hash == final_hash:
        raise RuntimeError("State did not change after applying patch")

    receipt = record_receipt(
        base_hash,
        selected["fp"],
        selected,
        final_hash,
    )

    output = {
        "code_receipt": code_receipt,
        "execution_receipt": receipt,
    }

    with open("cge_receipt.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
