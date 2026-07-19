from abc import ABC, abstractmethod
from pathlib import Path

from project_atlantis.core.models import Invoice


class BaseParser(ABC):
    """Base contract for all invoice parsers."""

    @abstractmethod
    def parse(self, file_path: str | Path) -> Invoice:
        """Parse a document into the canonical Invoice model."""
        raise NotImplementedError