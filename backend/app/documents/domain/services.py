
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ParsedDocument:
    markdown: str


class DocumentParser(Protocol):
    def parse(
        self,
        file_path: str,
    ) -> ParsedDocument:
        ...
