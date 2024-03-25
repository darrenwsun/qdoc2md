import sys

from qdoc2md.generator import Generator


def qdoc2md() -> None:
    """
    Convert q documentation comments into Markdown documents.
    """
    if len(sys.argv) != 2:
        raise Exception('Expect one argument for q source directory')
    generator = Generator()
    generator.generate(src=sys.argv[1])


if __name__ == "__main__":
    qdoc2md()
