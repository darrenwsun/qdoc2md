from enum import Enum


class Section(str, Enum):
    SUMMARY = ''
    PARAM = '@param'
    RETURN = '@return'
    THROWS = '@throws'
    DEPRECATED = '@deprecated'
    EXAMPLE = '@example'
    README = '@readme'
    NAMESPACE = '@namespace'
    LINK = '@link'
    SEE = '@see'
    DATATYPE = '@datatype'
