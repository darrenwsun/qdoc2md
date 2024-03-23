# This is a sample Python script.
from qdoc2md.generator import Generator


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    # parser = Parser()
    # md_doc = parser.parse("test.q")
    # md_doc.create_md_file()
    generator = Generator(source_suffix="q")
    # generator.generate(src="q")
    generator.generate(src="../qutils/src/src", output="../qutils/src/qdocs")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
