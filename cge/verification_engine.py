import subprocess
import tempfile
import os
import shutil

def apply_patch(repo_path: str, changes: dict):
    for path, content in changes.items():
        full = os.path.join(repo_path, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(content)

def run_tests(repo_path: str) -> bool:
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "-q"],
            cwd=repo_path,
            capture_output=True
        )
        return result.returncode == 0
    except Exception:
        return False

def verify_proposal(base_repo: str, proposal: dict) -> dict:
    temp_dir = tempfile.mkdtemp()
    shutil.copytree(base_repo, temp_dir, dirs_exist_ok=True)

    apply_patch(temp_dir, proposal["files"])
    passed = run_tests(temp_dir)

    shutil.rmtree(temp_dir)

    return {
        "proposal": proposal,
        "test_passed": passed
    }
