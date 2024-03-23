from dataclasses import dataclass

from mdutils import MdUtils


@dataclass
class Document:
    path: str
    md_doc: MdUtils
    keywords: set
