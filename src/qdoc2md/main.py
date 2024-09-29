import argparse

from qdoc2md.generator import generate


def qdoc2md() -> None:
    """
    Convert q documentation comments into Markdown documents.
    """
    parser = argparse.ArgumentParser(description='Generate Markdown documents from q documentation comments')
    parser.add_argument('-s', '--src', default='src', nargs='*', help='Source files or directories')
    parser.add_argument('-t', '--target', default='docs', help='Output directory for generated docs')
    args = parser.parse_args()
    generate(args.src, args.target)


if __name__ == "__main__":
    qdoc2md()
