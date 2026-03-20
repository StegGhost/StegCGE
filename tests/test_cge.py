from demo.sample_repo.app import add

from cge.mcl_engine import compare_candidates
from cge.proposal_engine import enforce_candidate_consensus
from cge.replay_engine import replay_chain


def test_add():
    assert add(1, 2) == 3


def test_mcl_consensus():
    candidates = [
        {"source": "gpt", "code": "print('hello')"},
        {"source": "claude", "code": "print('hello')"},
        {"source": "other", "code": "print('hi')"},
    ]

    result = compare_candidates(candidates)

    assert result["agreement_ratio"] >= 2 / 3
    assert result["consensus_size"] == 2
    assert result["selected_code"] == "print('hello')"
    assert result["selected_sources"] == ["gpt", "claude"]


def test_proposal_consensus_gate_success():
    proposals = [
        {
            "model": "gpt",
            "files": {
                "app.py": "def add(a, b):\n    return a + b\n",
            },
        },
        {
            "model": "claude",
            "files": {
                "app.py": "def add(a, b):\n    return a + b\n",
            },
        },
        {
            "model": "other",
            "files": {
                "app.py": "def add(a, b):\n    return a + b + 1\n",
            },
        },
    ]

    result = enforce_candidate_consensus(proposals, min_agreement_ratio=0.66)

    assert result["selected_proposal"]["files"]["app.py"] == "def add(a, b):\n    return a + b\n"
    assert result["consensus"]["consensus_size"] == 2
    assert result["consensus"]["agreement_ratio"] >= 2 / 3


def test_proposal_consensus_gate_failure():
    proposals = [
        {
            "model": "gpt",
            "files": {
                "app.py": "def add(a, b):\n    return a + b\n",
            },
        },
        {
            "model": "claude",
            "files": {
                "app.py": "def add(a, b):\n    return a + b + 1\n",
            },
        },
        {
            "model": "other",
            "files": {
                "app.py": "def add(a, b):\n    return a + b + 2\n",
            },
        },
    ]

    try:
        enforce_candidate_consensus(proposals, min_agreement_ratio=0.66)
        assert False, "Expected insufficient consensus failure"
    except RuntimeError as e:
        assert "Insufficient LLM consensus" in str(e)


def test_replay_structure():
    receipts = []

    result = replay_chain("demo/sample_repo", receipts)

    assert result["status"] == "ok"
    assert "final_state_hash" in result
    assert isinstance(result["final_state_hash"], str)
    assert len(result["final_state_hash"]) > 0
