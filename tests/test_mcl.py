from cge.mcl_engine import compare_candidates


def test_consensus():
    candidates = [
        {"source": "gpt", "code": "print('hello')"},
        {"source": "claude", "code": "print('hello')"},
        {"source": "other", "code": "print('hi')"},
    ]

    result = compare_candidates(candidates)

    assert result["agreement_ratio"] >= 2/3
    assert result["consensus_size"] == 2
