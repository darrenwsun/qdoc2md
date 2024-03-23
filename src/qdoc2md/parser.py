import itertools
from pathlib import Path

from mdutils import MdUtils
from mdutils.tools.Header import Header

from qdoc2md.param import Param
from qdoc2md.section import DocCommentSection


class Parser(object):
    def __init__(self, doc_start="///"):
        self.doc_start = doc_start

    def parse(self, source):
        doc_start = False
        md_doc = MdUtils(file_name=Path(source).with_suffix('.md').as_posix(), title=Path(source).stem)
        doc_comment = {}
        with open(source, mode="r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(self.doc_start):
                    doc_start = True
                    current_section = DocCommentSection.SUMMARY
                    doc_comment[current_section] = []
                    continue
                if not doc_start:
                    continue
                if line.startswith("/"):
                    line = line.lstrip("/")
                    if line.startswith(" "):
                        line = line[1:]
                    if line.startswith(DocCommentSection.NAMESPACE):
                        current_section = DocCommentSection.README
                        line = line.removeprefix(DocCommentSection.NAMESPACE).lstrip()
                        doc_comment[DocCommentSection.NAMESPACE] = line
                    elif line.startswith(DocCommentSection.README):
                        current_section = DocCommentSection.README
                        line = line.removeprefix(DocCommentSection.README).lstrip()
                        doc_comment[DocCommentSection.README] = line
                    elif line.startswith(DocCommentSection.PARAM):
                        current_section = DocCommentSection.PARAM
                        line = line.removeprefix(DocCommentSection.PARAM).lstrip()
                        tokens = line.split(' ', 1)
                        param_name = tokens[0]
                        index_left_brace, index_right_brace = line.find("{"), line.find("}")
                        param_type = line[index_left_brace+1:index_right_brace]
                        param_desc = line[index_right_brace+1:]
                        if DocCommentSection.PARAM not in doc_comment:
                            doc_comment[DocCommentSection.PARAM] = [Param(param_name, param_type, param_desc)]
                        else:
                            doc_comment[DocCommentSection.PARAM].append(Param(param_name, param_type, param_desc))
                    elif line.startswith(DocCommentSection.RETURN):
                        current_section = DocCommentSection.RETURN
                        line = line.removeprefix("@return").lstrip()
                        index_left_brace, index_right_brace = line.find("{"), line.find("}")
                        datatype = line[index_left_brace+1:index_right_brace]
                        desc = line[index_right_brace+1:]
                        doc_comment[DocCommentSection.RETURN] = Param("", datatype, desc)
                    elif line.startswith(DocCommentSection.THROWS):
                        current_section = DocCommentSection.THROWS
                        line = line.removeprefix("@throws").lstrip()
                        index_left_brace, index_right_brace = line.find("{"), line.find("}")
                        datatype = line[index_left_brace+1:index_right_brace]
                        desc = line[index_right_brace+1:]
                        doc_comment[DocCommentSection.THROWS] = Param("", datatype, desc)
                    elif line.startswith(DocCommentSection.DEPRECATED):
                        doc_comment[DocCommentSection.DEPRECATED] = True
                    elif line.startswith(DocCommentSection.EXAMPLE):
                        current_section = DocCommentSection.EXAMPLE
                        doc_comment[DocCommentSection.EXAMPLE] = []
                    else:       # Continuation of the current section
                        match current_section:
                            case DocCommentSection.README: doc_comment[current_section] += line
                            case DocCommentSection.SUMMARY:
                                if current_section in doc_comment:
                                    doc_comment[current_section].append(line if not line.isspace() and line else "\n")
                                else:
                                    doc_comment[current_section] = [line]
                            case DocCommentSection.PARAM: doc_comment[current_section][-1].description += line
                            case DocCommentSection.RETURN: doc_comment[current_section].description += line
                            case DocCommentSection.THROWS: doc_comment[current_section].description += line
                            case DocCommentSection.EXAMPLE: doc_comment[current_section].append(line)
                elif current_section == DocCommentSection.README:
                    if DocCommentSection.NAMESPACE in doc_comment:
                        md_doc.title = Header().choose_header(level=1, title=doc_comment[DocCommentSection.NAMESPACE])
                    if DocCommentSection.README in doc_comment:
                        md_doc.new_paragraph(doc_comment[DocCommentSection.README])
                        md_doc.write('\n')
                    doc_start = False
                    doc_comment.clear()
                else:
                    index_colon = line.find(":")
                    obj = line[:index_colon].strip()
                    md_doc.new_header(2, obj, add_table_of_contents="n")
                    if DocCommentSection.DEPRECATED in doc_comment:
                        md_doc.new_paragraph("Deprecated", bold_italics_code="bi")
                        md_doc.write('\n')
                    md_doc.new_paragraph(" ".join(doc_comment[DocCommentSection.SUMMARY]))
                    if DocCommentSection.PARAM in doc_comment:
                        params = doc_comment[DocCommentSection.PARAM]
                        md_doc.new_paragraph("Parameter:", bold_italics_code="b")
                        param_list = ["Name", "Type", "Description"]
                        param_list.extend(itertools.chain.from_iterable([param.name, param.datatype, param.description] for param in params))
                        md_doc.write('\n')
                        md_doc.new_table(columns=3, rows=len(params)+1, text=param_list, text_align="left")
                    if DocCommentSection.RETURN in doc_comment:
                        md_doc.new_paragraph("Returns:", bold_italics_code="b")
                        md_doc.write('\n')
                        md_doc.new_table(columns=2,
                                         rows=2,
                                         text=["Type", "Description", doc_comment[DocCommentSection.RETURN].datatype, doc_comment[DocCommentSection.RETURN].description],
                                         text_align="left")
                    if DocCommentSection.THROWS in doc_comment:
                        md_doc.new_paragraph("Throws:", bold_italics_code="b")
                        md_doc.write('\n')
                        md_doc.new_table(columns=2,
                                         rows=2,
                                         text=["Type", "Description", doc_comment[DocCommentSection.THROWS].datatype, doc_comment[DocCommentSection.THROWS].description],
                                         text_align="left")
                    if DocCommentSection.EXAMPLE in doc_comment and doc_comment[DocCommentSection.EXAMPLE]:
                        md_doc.new_paragraph("Example:", bold_italics_code="b")
                        md_doc.insert_code(code="\n".join(doc_comment[DocCommentSection.EXAMPLE]), language="q")
                        md_doc.write('\n')
                    doc_start = False
                    doc_comment.clear()
        return md_doc
