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

from cge.chain_engine import link_receipts, verify_chain
from cge.replay_engine import replay_chain


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

    # 🔥 Consensus Gate
    consensus_gate = enforce_candidate_consensus(raw_proposals, min_agreement_ratio=0.50)
    selected_consensus_proposal = consensus_gate["selected_proposal"]
    code_receipt = record_code_receipt(consensus_gate["consensus"])

    # Verification phase
    for raw in raw_proposals:
        proposal = normalize_proposal(raw)
        fp = fingerprint_proposal(proposal)

        res = verify_proposal(BASE, proposal)
        res["fp"] = fp
        results.append(res)

    # Filter to consensus-aligned proposals
    filtered = [
        r for r in results
        if r["proposal"]["files"] == selected_consensus_proposal["files"]
    ]

    selected = select_patch(filtered)

    # Apply patch
    apply_patch(BASE, selected["proposal"]["files"])

    final_state = snapshot_repo(BASE)
    final_hash = hash_state(final_state)

    if selected["proposal"]["files"] and base_hash == final_hash:
        raise RuntimeError("State did not change after applying patch")

    # 🔗 Build receipt chain
    execution_receipt = record_receipt(
        base_hash,
        selected["fp"],
        selected,
        final_hash,
        parent_hash=None,
    )

    chain = link_receipts([execution_receipt])

    # 🔁 Replay verification
    replay_result = replay_chain(BASE, chain)

    # 🔍 Chain verification
    chain_result = verify_chain(chain)

    output = {
        "code_receipt": code_receipt,
        "execution_chain": chain,
        "chain_valid": chain_result,
        "replay_result": replay_result,
    }

    with open("cge_receipt.json", "w") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
