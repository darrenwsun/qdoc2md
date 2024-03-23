import os

from mdutils import MdUtils

from qdoc2md.parser import Parser


def test_parser():
    parser = Parser()
    md = parser.parse(os.path.join(os.path.dirname(__file__), 'resources', 'test.q'))
    assert md.file_data_text == MdUtils(file_name='test.md').read_md_file(os.path.join(os.path.dirname(__file__), 'resources', 'test.md'))
