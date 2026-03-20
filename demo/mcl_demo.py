from cge.mcl_engine import compare_candidates
from cge.code_receipt import record_code_receipt


def main():
    candidates = [
        {"source": "gpt", "code": "print('hello world')"},
        {"source": "claude", "code": "print('hello world')"},
        {"source": "alt", "code": "print('hello_world')"},
    ]

    consensus = compare_candidates(candidates)
    receipt = record_code_receipt(consensus)

    print("\n=== CONSENSUS ===")
    print(consensus["selected_code"])

    print("\n=== RECEIPT ===")
    print(receipt)


if __name__ == "__main__":
    main()
