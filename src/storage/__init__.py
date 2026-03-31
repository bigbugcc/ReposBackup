from .base import BaseStorage
from .cos import TencentCOSStorage
from .ftp import FTPStorage
from .oss import AliyunOSSStorage
from .r2 import R2Storage
from .webdav import WebDAVStorage


def create_storage(config) -> BaseStorage:  # config: StorageConfig
    """Instantiate the correct storage backend from *config*.

    Raises ``ValueError`` for unknown storage types.
    """
    storage_type = config.storage_type.lower()

    if storage_type == "r2":
        return R2Storage(
            account_id=config.r2_account_id,
            access_key_id=config.r2_access_key_id,
            secret_access_key=config.r2_secret_access_key,
            bucket_name=config.r2_bucket_name,
            bucket_path=config.r2_bucket_path,
        )
    if storage_type == "tencent_cos":
        return TencentCOSStorage(
            secret_id=config.cos_secret_id,
            secret_key=config.cos_secret_key,
            bucket_name=config.cos_bucket_name,
            region=config.cos_region,
            bucket_path=config.cos_bucket_path,
        )
    if storage_type == "aliyun_oss":
        return AliyunOSSStorage(
            access_key_id=config.oss_access_key_id,
            access_key_secret=config.oss_access_key_secret,
            bucket_name=config.oss_bucket_name,
            endpoint=config.oss_endpoint,
            bucket_path=config.oss_bucket_path,
        )
    if storage_type == "ftp":
        return FTPStorage(
            host=config.ftp_host,
            port=config.ftp_port,
            username=config.ftp_username,
            password=config.ftp_password,
            path=config.ftp_path,
        )
    if storage_type == "webdav":
        return WebDAVStorage(
            url=config.webdav_url,
            username=config.webdav_username,
            password=config.webdav_password,
            path=config.webdav_path,
        )

    raise ValueError(
        f"Unknown storage type: '{storage_type}'. "
        "Supported values: r2, tencent_cos, aliyun_oss, ftp, webdav"
    )


__all__ = [
    "BaseStorage",
    "R2Storage",
    "TencentCOSStorage",
    "AliyunOSSStorage",
    "FTPStorage",
    "WebDAVStorage",
    "create_storage",
]
