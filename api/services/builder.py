import subprocess
import tempfile
import os

def build_image(git_url: str, commit_sha: str, image_tag: str):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["git", "clone", git_url, tmp],
            check=True,
            capture_output=True,
            text=True
        )

        subprocess.run(
            ["git", "checkout", commit_sha],
            cwd=tmp,
            check=True,
            capture_output=True,
            text=True
        )

        build = subprocess.run(
            ["docker", "build", "-t", image_tag, "."],
            cwd=tmp,
            capture_output=True,
            text=True
        )

        return build.returncode, build.stdout + build.stderr
