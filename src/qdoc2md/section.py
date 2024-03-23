from enum import Enum


class DocCommentSection(str, Enum):
    SUMMARY = ''
    PARAM = '@param'
    RETURN = '@return'
    THROWS = '@throws'
    DEPRECATED = '@deprecated'
    EXAMPLE = '@example'
    README = '@readme'
    NAMESPACE = '@namespace'
