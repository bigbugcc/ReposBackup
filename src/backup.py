#!/usr/bin/env python3
"""ReposBackup – Back up GitHub repositories to cloud / FTP / WebDAV storage."""

import os
import sys
import tempfile

# Ensure src/ directory is on the path so sibling modules are importable
# when this script is invoked directly (e.g. ``python src/backup.py``).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config  # noqa: E402
from git_utils import backup_repo_branches  # noqa: E402
from report import generate_markdown_report  # noqa: E402
from storage import create_storage  # noqa: E402


def main() -> None:
    print("🚀 ReposBackup – Starting backup process …")

    storage_config, backup_config = load_config()

    if not storage_config.storage_type:
        print("❌ Error: STORAGE_TYPE is not set.")
        sys.exit(1)

    # Resolve repository list
    repos = backup_config.repos
    if not repos:
        current = backup_config.current_repo
        if not current:
            print(
                "❌ Error: No repositories specified and "
                "GITHUB_REPOSITORY is not set."
            )
            sys.exit(1)
        repos = [current]
        print(f"📌 Backing up current repository: {current}")
    else:
        plural = "y" if len(repos) == 1 else "ies"
        print(f"📋 Backing up {len(repos)} repositor{plural}:")
        for repo in repos:
            print(f"   • {repo}")

    # Initialise storage backend
    print(f"\n📦 Storage backend: {storage_config.storage_type}")
    try:
        storage = create_storage(storage_config)
    except Exception as exc:
        print(f"❌ Failed to initialise storage: {exc}")
        sys.exit(1)

    # Process repositories
    all_results: dict[str, list[tuple[str, str, int]]] = {}

    with tempfile.TemporaryDirectory() as work_dir:
        for repo in repos:
            print(f"\n🔄 Processing: {repo}")
            try:
                archives = backup_repo_branches(
                    repo=repo,
                    token=backup_config.github_token,
                    backup_branch=backup_config.backup_branch,
                    work_dir=work_dir,
                )
            except Exception as exc:
                print(f"  ❌ Clone/archive failed for {repo}: {exc}")
                continue

            if not archives:
                print(f"  ⚠️  No archives produced for {repo}")
                continue

            repo_results = []
            owner, repo_name = (repo.split("/", 1) + [""])[:2]
            if not repo_name:
                repo_name, owner = owner, "unknown"

            for branch, archive_path, size in archives:
                archive_filename = os.path.basename(archive_path)
                remote_path = f"{owner}/{repo_name}/{archive_filename}"
                print(f"  ⬆️  Uploading {archive_filename} …")
                try:
                    remote_url = storage.upload(archive_path, remote_path)
                    print(f"  ✅ Uploaded → {remote_url}")
                    repo_results.append((branch, remote_url, size))
                except Exception as exc:
                    print(f"  ❌ Upload failed: {exc}")

            if repo_results:
                all_results[repo] = repo_results

    # Summary
    print(f"\n{'=' * 50}")
    print("📊 Backup Summary:")
    print(f"   Repositories requested : {len(repos)}")
    print(f"   Successful             : {len(all_results)}")
    print(f"   Failed                 : {len(repos) - len(all_results)}")

    # Markdown report
    if backup_config.generate_report and all_results:
        print("\n📝 Backup Report:")
        report = generate_markdown_report(
            backup_results=all_results,
            storage_type=storage_config.storage_type,
            backup_branch=backup_config.backup_branch,
        )
        print(f"\n{'=' * 50}")
        print(report)
        print("=" * 50)

    if not all_results and repos:
        print("\n❌ All backups failed.")
        sys.exit(1)

    print("\n✨ Backup completed successfully!")


if __name__ == "__main__":
    main()
