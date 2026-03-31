import ftplib
import os

from .base import BaseStorage


class FTPStorage(BaseStorage):
    """FTP storage backend."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        path: str = "/",
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.base_path = path.rstrip("/") or "/"

    def _connect(self) -> ftplib.FTP:
        ftp = ftplib.FTP()
        ftp.connect(self.host, self.port, timeout=30)
        ftp.login(self.username, self.password)
        return ftp

    @staticmethod
    def _makedirs(ftp: ftplib.FTP, path: str) -> None:
        """Recursively create directory tree on the FTP server."""
        parts = [p for p in path.split("/") if p]
        current = ""
        for part in parts:
            current = f"{current}/{part}"
            try:
                ftp.mkd(current)
            except ftplib.error_perm as exc:
                # 550 = directory already exists
                if "550" not in str(exc):
                    raise

    def upload(self, local_path: str, remote_path: str) -> str:
        full_remote = f"{self.base_path}/{remote_path}".replace("//", "/")
        remote_dir = "/".join(full_remote.split("/")[:-1]) or "/"
        filename = os.path.basename(full_remote)

        ftp = self._connect()
        try:
            self._makedirs(ftp, remote_dir)
            ftp.cwd(remote_dir)
            with open(local_path, "rb") as fobj:
                ftp.storbinary(f"STOR {filename}", fobj)
        finally:
            ftp.quit()

        return f"ftp://{self.host}{full_remote}"

    def test_connection(self) -> bool:
        try:
            ftp = self._connect()
            ftp.quit()
            return True
        except Exception:
            return False
