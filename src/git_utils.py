import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


def run_cmd(
    cmd: List[str],
    cwd: Optional[str] = None,
    check: bool = True,
) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )
    return result


def get_clone_url(repo: str, token: str) -> str:
    """Build a GitHub clone URL, embedding token authentication when provided."""
    if token:
        return f"https://x-access-token:{token}@github.com/{repo}.git"
    return f"https://github.com/{repo}.git"


def get_remote_branches(clone_dir: str) -> List[str]:
    """Return all remote branch names from a cloned repository."""
    result = run_cmd(["git", "branch", "-r"], cwd=clone_dir)
    branches = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("origin/") and "->" not in line:
            branches.append(line[len("origin/"):])
    return branches


def clone_repo(repo: str, token: str, work_dir: str) -> str:
    """Clone *repo* into *work_dir* and return the clone directory path."""
    url = get_clone_url(repo, token)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", repo)
    clone_dir = os.path.join(work_dir, safe_name)
    print(f"  Cloning {repo} …")
    run_cmd(["git", "clone", "--no-single-branch", url, clone_dir])
    return clone_dir


def create_zip_from_branch(clone_dir: str, branch: str, output_path: str) -> None:
    """Create a zip archive of *branch* in *clone_dir* at *output_path*.

    Uses ``git archive`` which is fast and avoids working-tree checkout.
    """
    run_cmd(
        ["git", "archive", "--format=zip", f"--output={output_path}", f"origin/{branch}"],
        cwd=clone_dir,
    )


def backup_repo_branches(
    repo: str,
    token: str,
    backup_branch: str,
    work_dir: str,
) -> List[Tuple[str, str, int]]:
    """Clone *repo* and create zip archives for the requested branch(es).

    Returns a list of ``(branch, archive_path, size_bytes)`` tuples for each
    successfully archived branch.
    """
    clone_dir = clone_repo(repo, token, work_dir)

    if backup_branch.lower() == "all":
        branches = get_remote_branches(clone_dir)
        if not branches:
            branches = ["main"]
    else:
        branches = [backup_branch]

    owner, repo_name = (repo.split("/", 1) + [""])[:2]
    if not repo_name:
        repo_name, owner = owner, "unknown"

    date_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    results = []

    for branch in branches:
        safe_branch = re.sub(r"[^A-Za-z0-9_.-]", "_", branch)
        archive_name = f"{owner}_{repo_name}_{safe_branch}_{date_str}.zip"
        archive_path = os.path.join(work_dir, archive_name)
        print(f"  Archiving branch '{branch}' …")
        try:
            create_zip_from_branch(clone_dir, branch, archive_path)
            size = os.path.getsize(archive_path)
            results.append((branch, archive_path, size))
            print(f"  ✓ {archive_name} ({format_size(size)})")
        except Exception as exc:
            print(f"  ✗ Failed to archive '{branch}': {exc}")

    return results


def format_size(size_bytes: int) -> str:
    """Return a human-readable file size string."""
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
