import itertools
from pathlib import Path

from mdutils import MdUtils
from mdutils.tools.Header import Header

from qdoc2md.document import Document
from qdoc2md.param import Param
from qdoc2md.section import Section


class Parser(object):
    def __init__(self, doc_start, out_dir):
        self.doc_start = doc_start
        self.out_dir = out_dir

    def parse(self, src_root, source):
        doc_start = False
        path = Path(source.replace(src_root, self.out_dir)).with_suffix('.md').as_posix()
        md_doc = MdUtils(file_name=path, title=Path(source).stem)
        doc_comment = {}
        keywords = set()
        with open(source, mode="r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(self.doc_start):
                    doc_start = True
                    current_section = Section.SUMMARY
                    doc_comment[current_section] = []
                    continue
                if not doc_start:
                    continue
                if line.startswith("/"):
                    line = line.lstrip("/")
                    if line.startswith(" "):
                        line = line[1:]
                    if line.startswith(Section.NAMESPACE):
                        current_section = Section.README
                        line = line.removeprefix(Section.NAMESPACE).lstrip()
                        doc_comment[Section.NAMESPACE] = line

                    elif line.startswith(Section.README):
                        current_section = Section.README
                        line = line.removeprefix(Section.README).lstrip()
                        doc_comment[Section.README] = line

                    elif line.startswith(Section.PARAM):
                        current_section = Section.PARAM
                        line = line.removeprefix(Section.PARAM).lstrip()
                        tokens = line.split(' ', 1)
                        param_name = tokens[0]
                        index_left_brace, index_right_brace = line.find("{"), line.find("}")
                        param_type = line[index_left_brace+1:index_right_brace]
                        param_desc = line[index_right_brace+1:]
                        if Section.PARAM not in doc_comment:
                            doc_comment[Section.PARAM] = [Param(param_name, param_type, param_desc)]
                        else:
                            doc_comment[Section.PARAM].append(Param(param_name, param_type, param_desc))

                    elif line.startswith(Section.RETURN):
                        current_section = Section.RETURN
                        line = line.removeprefix(Section.RETURN).lstrip()
                        index_left_brace, index_right_brace = line.find("{"), line.find("}")
                        datatype = line[index_left_brace+1:index_right_brace]
                        desc = line[index_right_brace+1:]
                        doc_comment[Section.RETURN] = Param("", datatype, desc)

                    elif line.startswith(Section.THROWS):
                        current_section = Section.THROWS
                        line = line.removeprefix(Section.THROWS).lstrip()
                        index_left_brace, index_right_brace = line.find("{"), line.find("}")
                        datatype = line[index_left_brace+1:index_right_brace]
                        desc = line[index_right_brace+1:]
                        doc_comment[Section.THROWS] = Param("", datatype, desc)

                    elif line.startswith(Section.DEPRECATED):
                        doc_comment[Section.DEPRECATED] = True

                    elif line.startswith(Section.EXAMPLE):
                        current_section = Section.EXAMPLE
                        doc_comment[Section.EXAMPLE] = []

                    elif line.startswith(Section.SEE):
                        current_section = Section.SEE
                        line = line.removeprefix(Section.SEE).lstrip()
                        doc_comment[Section.SEE] = [line]
                    else:       # Continuation of the current section
                        match current_section:
                            case Section.README:
                                doc_comment[current_section] += line
                            case Section.SUMMARY:
                                doc_comment[current_section].append(line if not line.isspace() and line else "\n")
                            case Section.PARAM:
                                doc_comment[current_section][-1].description += line
                            case Section.RETURN:
                                doc_comment[current_section].description += line
                            case Section.THROWS:
                                doc_comment[current_section].description += line
                            case Section.EXAMPLE:
                                doc_comment[current_section].append(line)
                            case Section.SEE:
                                doc_comment[current_section].append(line if not line.isspace() and line else "\n")
                elif current_section == Section.README:     # The line doesn't start with slash but current section is readme
                    if Section.NAMESPACE in doc_comment:
                        md_doc.title = Header().choose_header(level=1, title=doc_comment[Section.NAMESPACE])
                    if Section.README in doc_comment:
                        md_doc.new_paragraph(doc_comment[Section.README])
                        md_doc.write('\n')
                    doc_start = False
                    doc_comment.clear()
                else:
                    index_colon = line.find(":")
                    obj = line[:index_colon].strip()
                    keywords.add(obj)
                    md_doc.new_header(2, obj, add_table_of_contents="n")
                    if Section.DEPRECATED in doc_comment:
                        md_doc.new_paragraph("Deprecated", bold_italics_code="bi")
                        md_doc.write('\n')
                    md_doc.new_paragraph(" ".join(doc_comment[Section.SUMMARY]))
                    if Section.PARAM in doc_comment:
                        params = doc_comment[Section.PARAM]
                        md_doc.new_paragraph("Parameter:", bold_italics_code="b")
                        param_list = ["Name", "Type", "Description"]
                        param_list.extend(itertools.chain.from_iterable([param.name, param.datatype, param.description] for param in params))
                        md_doc.write('\n')
                        md_doc.new_table(columns=3, rows=len(params)+1, text=param_list, text_align="left")
                    if Section.RETURN in doc_comment:
                        md_doc.new_paragraph("Returns:", bold_italics_code="b")
                        md_doc.write('\n')
                        md_doc.new_table(columns=2,
                                         rows=2,
                                         text=["Type", "Description", doc_comment[Section.RETURN].datatype, doc_comment[Section.RETURN].description],
                                         text_align="left")
                    if Section.THROWS in doc_comment:
                        md_doc.new_paragraph("Throws:", bold_italics_code="b")
                        md_doc.write('\n')
                        md_doc.new_table(columns=2,
                                         rows=2,
                                         text=["Type", "Description", doc_comment[Section.THROWS].datatype, doc_comment[Section.THROWS].description],
                                         text_align="left")
                    if Section.EXAMPLE in doc_comment and doc_comment[Section.EXAMPLE]:
                        md_doc.new_paragraph("Example:", bold_italics_code="b")
                        md_doc.insert_code(code="\n".join(doc_comment[Section.EXAMPLE]), language="q")
                        md_doc.write('\n')
                    if Section.SEE in doc_comment and doc_comment[Section.SEE]:
                        md_doc.new_paragraph("See also:", bold_italics_code="b")
                        md_doc.new_paragraph(" ".join(doc_comment[Section.SEE]))
                        md_doc.write('\n')
                    doc_start = False
                    doc_comment.clear()
        return Document(path, md_doc, keywords)
