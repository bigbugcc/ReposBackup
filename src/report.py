from datetime import datetime
from typing import Dict, List, Tuple

from git_utils import format_size


def generate_markdown_report(
    backup_results: Dict[str, List[Tuple[str, str, int]]],
    storage_type: str,
    backup_branch: str,
) -> str:
    """Generate a Markdown backup report.

    Args:
        backup_results: ``{repo: [(branch, remote_url, size_bytes), …], …}``
        storage_type:   The storage backend identifier used for this run.
        backup_branch:  The branch filter setting (``"all"`` or a branch name).

    Returns:
        A Markdown-formatted string suitable for printing or saving.
    """
    now = datetime.utcnow()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S UTC")

    total_archives = sum(len(v) for v in backup_results.values())
    total_size = sum(
        size for archives in backup_results.values() for _, _, size in archives
    )

    storage_display = {
        "r2": "Cloudflare R2",
        "tencent_cos": "Tencent Cloud COS",
        "aliyun_oss": "Alibaba Cloud OSS",
        "ftp": "FTP",
        "webdav": "WebDAV",
    }.get(storage_type, storage_type)

    branch_display = (
        "All branches"
        if backup_branch.lower() == "all"
        else f"Branch: `{backup_branch}`"
    )

    lines = [
        "# 📦 Repository Backup Report",
        "",
        f"> Generated at: **{date_str}**",
        "",
        "## Summary",
        "",
        "| Item | Value |",
        "|------|-------|",
        f"| Storage Backend | {storage_display} |",
        f"| Backup Scope | {branch_display} |",
        f"| Repositories | {len(backup_results)} |",
        f"| Archives Created | {total_archives} |",
        f"| Total Size | {format_size(total_size)} |",
        "",
        "## Backup Details",
        "",
    ]

    for repo, archives in sorted(backup_results.items()):
        lines.append(f"### 📁 `{repo}`")
        lines.append("")
        lines.append("| Branch | Archive | Size |")
        lines.append("|--------|---------|------|")
        for branch, remote_url, size in sorted(archives, key=lambda x: x[0]):
            archive_name = remote_url.split("/")[-1]
            lines.append(f"| `{branch}` | `{archive_name}` | {format_size(size)} |")
        lines.append("")

    lines += [
        "---",
        "",
        "*Backup completed using [ReposBackup](https://github.com/bigbugcc/ReposBackup)*",
    ]

    return "\n".join(lines)
