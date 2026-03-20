from cge.chain_engine import link_receipts, verify_chain


def test_chain_linking():
    receipts = [
        {"receipt_hash": "a"},
        {"receipt_hash": "b"},
        {"receipt_hash": "c"},
    ]

    linked = link_receipts(receipts)

    assert linked[0]["parent_hash"] is None
    assert linked[1]["parent_hash"] == "a"
    assert linked[2]["parent_hash"] == "b"


def test_chain_validation():
    receipts = [
        {"receipt_hash": "a", "parent_hash": None},
        {"receipt_hash": "b", "parent_hash": "a"},
    ]

    result = verify_chain(receipts)
    assert result["valid"] is True
