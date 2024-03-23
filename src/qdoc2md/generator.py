import os.path
import re
from glob import glob
from pathlib import Path

from qdoc2md.document import Document
from qdoc2md.parser import Parser
from qdoc2md.section import Section


class Generator(object):
    def __init__(self, source_suffix, doc_start="///", out_dir="docs"):
        self.source_suffix = source_suffix
        self.parser = Parser(doc_start, out_dir)
        self.out_dir = out_dir

    def generate(self, src):
        docs = []
        for filename in glob(src + '/**/*.' + self.source_suffix, recursive=True):
            doc = self.parser.parse(src, filename)
            docs.append(doc)

        Generator.resolve_links(docs)

        for doc in docs:
            Path(doc.path).parent.mkdir(parents=True, exist_ok=True)
            doc.md_doc.create_md_file()

    @staticmethod
    def resolve_links(docs):
        keyword_to_path = Generator.index_by_keyword(docs)
        for doc in docs:
            text: str = doc.md_doc.file_data_text
            pattern = re.compile(f'{Section.LINK.value}{{(.*?)}}')
            match = re.search(pattern, text)
            while match:
                keywords = set(match.groups())
                for keyword in keywords:
                    if keyword in keyword_to_path:
                        path = keyword_to_path[keyword]
                        text = text.replace(
                            f'{Section.LINK.value}{{{keyword}}}',
                            f'[{keyword}]({'' if path == doc.path else Path(os.path.relpath(path, start=doc.path)).as_posix()}#{keyword.replace('.', '')})')
                match = re.search(pattern, text)
            doc.md_doc.file_data_text = text


    @staticmethod
    def index_by_keyword(docs: list[Document]):
        keyword_to_path = {}
        for doc in docs:
            for keyword in doc.keywords:
                keyword_to_path[keyword] = doc.path
        return keyword_to_path
