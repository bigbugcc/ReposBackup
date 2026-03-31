import oss2

from .base import BaseStorage


class AliyunOSSStorage(BaseStorage):
    """Alibaba Cloud Object Storage Service (OSS) backend."""

    def __init__(
        self,
        access_key_id: str,
        access_key_secret: str,
        bucket_name: str,
        endpoint: str,
        bucket_path: str = "",
    ) -> None:
        self.bucket_path = bucket_path.strip("/")
        auth = oss2.Auth(access_key_id, access_key_secret)
        self._bucket = oss2.Bucket(auth, endpoint, bucket_name)

    def _key(self, remote_path: str) -> str:
        if self.bucket_path:
            return f"{self.bucket_path}/{remote_path}".lstrip("/")
        return remote_path.lstrip("/")

    def upload(self, local_path: str, remote_path: str) -> str:
        key = self._key(remote_path)
        self._bucket.put_object_from_file(key, local_path)
        return f"oss://{self._bucket.bucket_name}/{key}"

    def test_connection(self) -> bool:
        try:
            self._bucket.get_bucket_stat()
            return True
        except Exception:
            return False
