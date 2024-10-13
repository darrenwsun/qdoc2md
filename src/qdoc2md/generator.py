import os.path
import re
from glob import glob
from pathlib import Path
from typing import List

from mdutils import MdUtils
from mdutils.tools.Header import Header

from qdoc2md.model import Param, SeeAlso, Document, Section

DOC_COMMENT_SIGNAL = '///'


def generate(sources, target):
    docs = []
    for src in sources:
        for src_file in glob(src + '/**/*.q', recursive=True):
            doc_file = Path(src_file.replace(src, target)).with_suffix('.md').as_posix()
            doc = parse(src_file, doc_file)
            docs.append(doc)

    resolve_links(docs)

    for doc in docs:
        Path(doc.path).parent.mkdir(parents=True, exist_ok=True)
        doc.md_doc.create_md_file()


def parse(src_file: str, target_file: str):
    md_doc = MdUtils(file_name=target_file, title=Path(src_file).stem)
    doc_comment = {}
    names = set()
    cur_section = Section.UNKNOWN
    in_doc_comment = False
    with open(src_file, mode="r") as f:
        for line in f:
            line = line.lstrip()
            if line.startswith(DOC_COMMENT_SIGNAL):
                in_doc_comment = True
                line = line[len(DOC_COMMENT_SIGNAL):]
                tag = ''
                if match := re.search(r'\s*(@\w+)', line):
                    tag = match.group(1)
                    line = line.lstrip()[len(tag)+1:].lstrip()

                if tag == Section.TITLE:
                    cur_section = Section.TITLE
                    doc_comment[cur_section] = line

                elif tag == Section.OVERVIEW:
                    cur_section = Section.OVERVIEW
                    doc_comment[cur_section] = line

                elif tag == Section.OWNER:
                    cur_section = Section.OWNER
                    doc_comment[cur_section] = line

                elif tag == Section.PARAM:
                    cur_section = Section.PARAM
                    if match := re.search(r'(\w+) +(?:(@atomic) +)?(?:\{(.*)\} +)?(?:(.*))?', line, re.DOTALL):
                        param = Param(match.group(1),
                                      True if match.group(2) else False,
                                      match.group(3) if match.group(3) else '',
                                      match.group(4))
                        if Section.PARAM not in doc_comment:
                            doc_comment[cur_section] = [param]
                        else:
                            doc_comment[cur_section].append(param)
                    else:
                        pass

                elif tag == Section.RETURN:
                    cur_section = Section.RETURN
                    if match := re.search(r'(?:(\w+) +)?(?:\{(.*)\} +)?(.+)', line, re.DOTALL):
                        param = Param(match.group(1) if match.group(1) else '',
                                      False,
                                      match.group(2) if match.group(2) else '',
                                      match.group(3))
                        doc_comment[cur_section] = param
                    else:
                        pass

                elif tag == Section.SIGNAL:
                    cur_section = Section.SIGNAL
                    if match := re.search(r'(?:\{(.*)\} +)?(.+)', line, re.DOTALL):
                        param = Param('',
                                      False,
                                      match.group(1) if match.group(1) else '',
                                      match.group(2))
                        if Section.SIGNAL not in doc_comment:
                            doc_comment[cur_section] = [param]
                        else:
                            doc_comment[cur_section].append(param)
                    else:
                        pass

                elif tag == Section.DEPRECATED:
                    cur_section = Section.DEPRECATED
                    doc_comment[cur_section] = True

                elif tag == Section.EXAMPLE:
                    cur_section = Section.EXAMPLE
                    doc_comment[cur_section] = ''

                elif tag == Section.SEE:
                    cur_section = Section.SEE
                    if match := re.search(r'(\{.*\})(?: +(.*))?', line, re.DOTALL):
                        seealso = SeeAlso(match.group(1),
                                          match.group(2) if match.group(2) else '')
                        if Section.SEE not in doc_comment:
                            doc_comment[cur_section] = [seealso]
                        else:
                            doc_comment[cur_section].append(seealso)

                elif cur_section == Section.UNKNOWN:    # Summary line
                    cur_section = Section.SUMMARY
                    if Section.SUMMARY not in doc_comment:
                        doc_comment[cur_section] = line
                    else:
                        doc_comment[cur_section] += line

                else:       # Continuation of the current section
                    if cur_section == Section.OVERVIEW or cur_section == Section.SUMMARY or cur_section == Section.EXAMPLE:
                        doc_comment[cur_section] += line
                    elif cur_section == Section.PARAM or cur_section == Section.SIGNAL or cur_section == Section.SEE:
                        doc_comment[cur_section][-1].description += line
                    elif cur_section == Section.RETURN:
                        doc_comment[cur_section].description += line
                    else:
                        pass
            elif line.startswith('/'):
                pass    # Ignore non-documentation comments
            else:   # End of documentation comments
                if in_doc_comment:
                    if cur_section == Section.TITLE or cur_section == Section.OVERVIEW or cur_section == Section.OWNER:
                        if Section.TITLE in doc_comment:
                            md_doc.title = ''
                            md_doc.new_header(1, doc_comment[Section.TITLE], add_table_of_contents="n")
                        if Section.OVERVIEW in doc_comment:
                            md_doc.write(doc_comment[Section.OVERVIEW] + '\n')
                        if Section.OWNER in doc_comment:
                            md_doc.write(f'This is owned by {doc_comment[Section.OWNER]}.' + '\n')
                    else:
                        index_colon = line.find(":")
                        name = line[:index_colon].strip()
                        names.add(name)
                        md_doc.new_header(2, name, add_table_of_contents="n")
                        md_doc.write('\n')
                        md_doc.write(('(DEPRECATED) ' if Section.DEPRECATED in doc_comment else '') + doc_comment[Section.SUMMARY])
                        if Section.PARAM in doc_comment:
                            params = doc_comment[Section.PARAM]
                            md_doc.write('\n')
                            md_doc.write('Parameters', bold_italics_code="b")
                            for param in params:
                                md_doc.new_paragraph(f'`{param.name}`' + ('⚛' if param.atomic else '') + f': {param.datatype}')
                                md_doc.new_line(f': {param.description}')
                        if Section.RETURN in doc_comment:
                            param = doc_comment[Section.RETURN]
                            md_doc.write('\n')
                            md_doc.write('Returns', bold_italics_code="b")
                            md_doc.new_paragraph(
                                (f'`{param.name}`: ' if param.name else '') + f'{doc_comment[Section.RETURN].datatype}')
                            md_doc.new_line(f': {doc_comment[Section.RETURN].description}')
                        if Section.SIGNAL in doc_comment:
                            md_doc.write('\n')
                            md_doc.write('Throws', bold_italics_code="b")
                            for throws in doc_comment[Section.SIGNAL]:
                                md_doc.new_paragraph(f'`{throws.datatype}`')
                                md_doc.new_line(f': {throws.description}')
                        if Section.EXAMPLE in doc_comment and doc_comment[Section.EXAMPLE]:
                            md_doc.write('\n')
                            md_doc.write('Example', bold_italics_code="b")
                            md_doc.insert_code(code=doc_comment[Section.EXAMPLE].rstrip(), language="q")
                            md_doc.write('\n')
                        if Section.SEE in doc_comment :
                            md_doc.write('\n')
                            md_doc.write('See Also', bold_italics_code="b")
                            for seealso in doc_comment[Section.SEE]:
                                md_doc.new_paragraph(f'{seealso.ref}')
                                md_doc.new_line(f': {seealso.description}')
                    cur_section = Section.UNKNOWN
                    doc_comment.clear()
                    in_doc_comment = False
                else:
                    pass
    return Document(target_file, md_doc, names)


def resolve_links(docs):
    keyword_to_path = index_by_keyword(docs)
    for doc in docs:
        text: str = doc.md_doc.file_data_text
        keywords = set(re.findall(f'{{{Section.LINK.value} +(.*?)}}', text))
        for keyword in keywords:
            if keyword in keyword_to_path:
                path = keyword_to_path[keyword]
                text = re.sub(f'{{{Section.LINK.value} +{keyword}}}',
                              f'[{keyword}]({"" if path == doc.path else Path(os.path.relpath(path, start=doc.path)).as_posix()}#{keyword.replace(".", "").lower()})',
                              text)
                # text = text.replace(
                #     f'{{{Section.LINK.value} {keyword}}}',
                #     f'[{keyword}]({"" if path == doc.path else Path(os.path.relpath(path, start=doc.path)).as_posix()}#{keyword.replace(".", "").lower()})')
            else:
                text = re.sub(f'{{{Section.LINK.value} +{keyword}}}',
                              keyword,
                              text)
        doc.md_doc.file_data_text = text


def index_by_keyword(docs: List[Document]):
    keyword_to_path = {}
    for doc in docs:
        for keyword in doc.keywords:
            keyword_to_path[keyword] = doc.path
    return keyword_to_path
