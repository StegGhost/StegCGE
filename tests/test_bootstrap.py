from cge.repo_state import snapshot_repo, hash_state

def test_repo_state_snapshot_smoke():
    state = snapshot_repo("cge")
    assert isinstance(state, dict)
    assert isinstance(hash_state(state), str)
