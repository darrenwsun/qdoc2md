# qdoc2md

This tool converts q documentation comments conforming to the specifications below to Markdown documents.

## Getting Started

Install the package via `pip install qdoc2md` and run the following command to generate docs saved in `docs`.

```bash
qdoc2md --src <your_q_src> --target <output_dir>
```

## Specifications of Documentation Comments

1. Docomments start with `///` (referred to as "docomment prompt" below) with whitespaces on both ends of the line ignored, and they are placed in a consecutive block above the entity (function or variable) to be documented
1. The first docomment presents a high-level summary of what the entity does. It may span multiple lines. 
1. The following tags are supported (`<>` represents placeholder, `[]` represents optional element, `{}` are verbatim to put an element in a group regardless of whitespace):
   1. `@title <title>`: A word or very short phrase about the script. This is preferably put at the top of the script. In its absence, the name of the script is used as the title.
   1. `@overview <description>`: An high-level summary of what the script does, written in Markdown. This is preferably put at the top of the script, following `@title`.
   1. `@param <name> [@atomic] [{datatype}] [description]`: Description of a parameter of a function, including its name, optional flag for atomic behavior, optional datatype, and more details such as what it represents.
   1. `@returns [<name>] [{<datatype>}] [description]`: Description of return value of a function, including its optional name, optional datatype, and more details such as what it represents.
   1. `@signal {<error>} [description]`: errors that may be signaled.
   1. `@example`: Example usage of a function. It should appear following the docomment prompt, and the example starts from the next line until the presence of another tag.
   1. `@see {<name>} <description>`: Entry for reference. Preferably `<name>` is a link either via `@link` or a usual Markdown link. `<description>` supports Markdown syntax.   
   1. `@deprecated`: Mark the entity deprecated. It should appear following the docomment prompt.
   1. `@link <name>`: Add a link to a name which is documented in the same project.
1. All occurrences of `<description>` above support Markdown syntax.
1. Use a datatype described below for `<datatype>`.

## Datatypes

Datatype is free-form text but it is suggested to use the following for consistency.

### Basic Types

1. Atom datatypes such as `boolean` and `guid`, as shown in [Datatypes](https://code.kx.com/q/ref/#datatypes) on the reference page of q.
1. `number`: alias to either `short`, `int`, `long`, `real` or `float`.
1. `hsym`: a subclass of `symbol` for file or process symbols
1. `dict` or `dict(symbol->int)`: a dictionary, with optionally the datatypes of its key and value.
1. `table` or `table([c1:date]c2:symbol)`: a table, with optionally column names and datatypes
1. `fn` or `fn(date;long)->date`: a function, with optionally the datatypes of its parameters and return value.

### Compound Types

1. Vector of atom datatypes, e.g. `boolean[]`.
1. `list` or `list(symbol;long)`: generic list, with optionally datatypes of its elements.
1. `string`: an alias to `char[]`.
1. `any`: any datatype.

# Example

See [sample.q](resources/sample.q) for a sample q script with the designated docomments, and [sample.md](resources/docs/sample.md) for the generated Markdown document. A static site can be built on top of the generated doc via [mkdocs](https://www.mkdocs.org/), e.g.  `cd resources && mkdocs serve`