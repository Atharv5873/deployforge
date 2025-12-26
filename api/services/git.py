import subprocess
import tempfile

def validate_repo(git_url: str, branch: str):
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            ["git", "clone", "-b", branch, "--depth", "1", git_url, tmp],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
