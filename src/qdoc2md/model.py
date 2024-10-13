from dataclasses import dataclass
from enum import Enum

from mdutils import MdUtils


class Section(str, Enum):
    ATOMIC = '@atomic'
    DEPRECATED = '@deprecated'
    EXAMPLE = '@example'
    LINK = '@link'
    OVERVIEW = '@overview'
    OWNER = '@owner'
    PARAM = '@param'
    RETURN = '@return'
    SIGNAL = '@signal'
    SEE = '@see'
    SUMMARY = '@summary'
    TITLE = '@title'
    UNKNOWN = ''


@dataclass
class Param:
    name: str
    atomic: bool
    datatype: str
    description: str


@dataclass
class SeeAlso:
    ref: str
    description: str


@dataclass
class Document:
    path: str
    md_doc: MdUtils
    keywords: set
