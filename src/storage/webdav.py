from webdav3.client import Client

from .base import BaseStorage


class WebDAVStorage(BaseStorage):
    """WebDAV storage backend."""

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        path: str = "/",
    ) -> None:
        self.base_path = path.rstrip("/") or "/"
        options = {
            "webdav_hostname": url,
            "webdav_login": username,
            "webdav_password": password,
        }
        self._client = Client(options)

    def _full_remote(self, remote_path: str) -> str:
        return f"{self.base_path}/{remote_path}".replace("//", "/")

    def _ensure_dir(self, remote_dir: str) -> None:
        """Create the remote directory path if it does not already exist."""
        parts = [p for p in remote_dir.split("/") if p]
        current = ""
        for part in parts:
            current = f"{current}/{part}"
            if not self._client.check(current):
                self._client.mkdir(current)

    def upload(self, local_path: str, remote_path: str) -> str:
        full_remote = self._full_remote(remote_path)
        remote_dir = "/".join(full_remote.split("/")[:-1]) or "/"
        self._ensure_dir(remote_dir)
        self._client.upload_sync(remote_path=full_remote, local_path=local_path)
        return full_remote

    def test_connection(self) -> bool:
        try:
            self._client.list("/")
            return True
        except Exception:
            return False
