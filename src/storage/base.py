from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    def upload(self, local_path: str, remote_path: str) -> str:
        """Upload *local_path* to *remote_path* on the storage backend.

        Returns the remote URL or path of the uploaded object.
        """

    @abstractmethod
    def test_connection(self) -> bool:
        """Return ``True`` if the storage backend is reachable and credentials
        are valid, ``False`` otherwise."""
