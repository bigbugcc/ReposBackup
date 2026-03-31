import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class StorageConfig:
    storage_type: str = ""

    # Cloudflare R2
    r2_account_id: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket_name: str = ""
    r2_bucket_path: str = ""

    # Tencent Cloud COS
    cos_secret_id: str = ""
    cos_secret_key: str = ""
    cos_bucket_name: str = ""
    cos_region: str = ""
    cos_bucket_path: str = ""

    # Alibaba Cloud OSS
    oss_access_key_id: str = ""
    oss_access_key_secret: str = ""
    oss_bucket_name: str = ""
    oss_endpoint: str = ""
    oss_bucket_path: str = ""

    # FTP
    ftp_host: str = ""
    ftp_port: int = 21
    ftp_username: str = ""
    ftp_password: str = ""
    ftp_path: str = "/"

    # WebDAV
    webdav_url: str = ""
    webdav_username: str = ""
    webdav_password: str = ""
    webdav_path: str = "/"


@dataclass
class BackupConfig:
    repos: List[str] = field(default_factory=list)
    backup_branch: str = "all"
    github_token: str = ""
    generate_report: bool = True
    current_repo: str = ""


def load_config():
    """Load configuration from environment variables."""
    storage = StorageConfig(
        storage_type=os.environ.get("STORAGE_TYPE", "").lower().strip(),
        r2_account_id=os.environ.get("R2_ACCOUNT_ID", ""),
        r2_access_key_id=os.environ.get("R2_ACCESS_KEY_ID", ""),
        r2_secret_access_key=os.environ.get("R2_SECRET_ACCESS_KEY", ""),
        r2_bucket_name=os.environ.get("R2_BUCKET_NAME", ""),
        r2_bucket_path=os.environ.get("R2_BUCKET_PATH", ""),
        cos_secret_id=os.environ.get("COS_SECRET_ID", ""),
        cos_secret_key=os.environ.get("COS_SECRET_KEY", ""),
        cos_bucket_name=os.environ.get("COS_BUCKET_NAME", ""),
        cos_region=os.environ.get("COS_REGION", ""),
        cos_bucket_path=os.environ.get("COS_BUCKET_PATH", ""),
        oss_access_key_id=os.environ.get("OSS_ACCESS_KEY_ID", ""),
        oss_access_key_secret=os.environ.get("OSS_ACCESS_KEY_SECRET", ""),
        oss_bucket_name=os.environ.get("OSS_BUCKET_NAME", ""),
        oss_endpoint=os.environ.get("OSS_ENDPOINT", ""),
        oss_bucket_path=os.environ.get("OSS_BUCKET_PATH", ""),
        ftp_host=os.environ.get("FTP_HOST", ""),
        ftp_port=int(os.environ.get("FTP_PORT", "21") or "21"),
        ftp_username=os.environ.get("FTP_USERNAME", ""),
        ftp_password=os.environ.get("FTP_PASSWORD", ""),
        ftp_path=os.environ.get("FTP_PATH", "/"),
        webdav_url=os.environ.get("WEBDAV_URL", ""),
        webdav_username=os.environ.get("WEBDAV_USERNAME", ""),
        webdav_password=os.environ.get("WEBDAV_PASSWORD", ""),
        webdav_path=os.environ.get("WEBDAV_PATH", "/"),
    )

    repos_raw = os.environ.get("BACKUP_REPOS", "").strip()
    repos = []
    if repos_raw:
        for line in repos_raw.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                repos.append(line)

    backup = BackupConfig(
        repos=repos,
        backup_branch=os.environ.get("BACKUP_BRANCH", "all").strip() or "all",
        github_token=os.environ.get("GITHUB_TOKEN", ""),
        generate_report=os.environ.get("GENERATE_REPORT", "true").lower() == "true",
        current_repo=os.environ.get("GITHUB_REPOSITORY", ""),
    )

    return storage, backup
