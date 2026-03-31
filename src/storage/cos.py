from qcloud_cos import CosConfig, CosS3Client

from .base import BaseStorage


class TencentCOSStorage(BaseStorage):
    """Tencent Cloud Object Storage (COS) backend."""

    def __init__(
        self,
        secret_id: str,
        secret_key: str,
        bucket_name: str,
        region: str,
        bucket_path: str = "",
    ) -> None:
        self.bucket_name = bucket_name
        self.bucket_path = bucket_path.strip("/")
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
        self._client = CosS3Client(config)

    def _key(self, remote_path: str) -> str:
        if self.bucket_path:
            return f"{self.bucket_path}/{remote_path}".lstrip("/")
        return remote_path.lstrip("/")

    def upload(self, local_path: str, remote_path: str) -> str:
        key = self._key(remote_path)
        with open(local_path, "rb") as fobj:
            self._client.put_object(
                Bucket=self.bucket_name,
                Body=fobj,
                Key=key,
            )
        return f"cos://{self.bucket_name}/{key}"

    def test_connection(self) -> bool:
        try:
            self._client.head_bucket(Bucket=self.bucket_name)
            return True
        except Exception:
            return False
