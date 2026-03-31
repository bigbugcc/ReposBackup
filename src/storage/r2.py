import boto3
from botocore.config import Config

from .base import BaseStorage


class R2Storage(BaseStorage):
    """Cloudflare R2 storage backend (S3-compatible API)."""

    def __init__(
        self,
        account_id: str,
        access_key_id: str,
        secret_access_key: str,
        bucket_name: str,
        bucket_path: str = "",
    ) -> None:
        self.bucket_name = bucket_name
        self.bucket_path = bucket_path.strip("/")
        endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"
        self._client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            config=Config(signature_version="s3v4"),
            region_name="auto",
        )

    def _key(self, remote_path: str) -> str:
        if self.bucket_path:
            return f"{self.bucket_path}/{remote_path}".lstrip("/")
        return remote_path.lstrip("/")

    def upload(self, local_path: str, remote_path: str) -> str:
        key = self._key(remote_path)
        self._client.upload_file(local_path, self.bucket_name, key)
        return f"r2://{self.bucket_name}/{key}"

    def test_connection(self) -> bool:
        try:
            self._client.head_bucket(Bucket=self.bucket_name)
            return True
        except Exception:
            return False
