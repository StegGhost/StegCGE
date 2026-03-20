def select_patch(results: list, mode="best_passing"):
    # results = [{proposal, test_passed}]
    if mode == "first_valid":
        for r in results:
            if r["test_passed"]:
                return r

    if mode == "best_passing":
        passed = [r for r in results if r["test_passed"]]
        return passed[0] if passed else results[0]

    return results[0]
