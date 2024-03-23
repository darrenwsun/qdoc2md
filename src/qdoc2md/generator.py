from glob import glob
from pathlib import Path

from qdoc2md.parser import Parser


class Generator(object):
    def __init__(self, source_suffix, doc_start="///"):
        self.source_suffix = source_suffix
        self.parser = Parser(doc_start)

    def generate(self, src, output="docs"):
        for filename in glob(src+'/**/*.'+self.source_suffix, recursive=True):
            md = self.parser.parse(filename)
            md.file_name = md.file_name.replace(src, output)
            Path(md.file_name).parent.mkdir(parents=True, exist_ok=True)
            md.create_md_file()
