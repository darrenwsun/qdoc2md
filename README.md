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
1. The following tags are supported:
   1. `@title <title>`: A word or very short phrase about the script. This is preferably put at the top of the script. In its absence, the name of the script is used as the title.
   1. `@overview <description>`: An high-level summary of what the script does, written in Markdown. This is preferably put at the top of the script, following `@title`.
   1. `@param <name> [{datatype}] <description>`: Description of a parameter of a function, including its name, optional datatype, and more details such as what it represents.
   1. `@returns [<name>] [{<datatype>}] <description>`: Description of return value of a function, including its optional name, optional datatype, and more details such as what it represents.
   1. `@signal {<error>} <description>`: errors that may be signaled.
   1. `@example`: Example usage of a function. It should appear following the docomment prompt, and the example starts from the next line until the presence of another tag.
   1. `@see {<name>} <description>`: Entry for reference. Preferably `<name>` is a link either via `@link` or a usual Markdown link. `<description>` supports Markdown syntax.   
   1. `@deprecated`: Mark the entity deprecated. It should appear following the docomment prompt.
   1. `@link <name>`: Add a link to the name. It should be put within a pair of curly braces, e.g. `{@link myfunc}`, the name should be documented in order to resolve to the right url. If the name is not defined in the same script, its enclosing script should be included by `qdoc2md` command in one run.
1. All occurrences of `<description>` above support Markdown syntax.
1. Use a datatype described below for `<datatype>`.

## Datatypes

1. Atom datatypes such as `boolean` and `guid`, as shown in [Datatypes](https://code.kx.com/q/ref/#datatypes) on the Reference Card page of q.
1. Vector of atom datatypes, e.g. `boolean[]`.
1. `list` or `list(symbol;long)`: generic list, with optionally datatypes of its elements.
1. `hsym` or `hsym[]`: a special case of `symbol` or `symbol[]` for file or process symbols.
1. `string`: an alias to `char[]`.
1. `::`: generic null, e.g. the return datatype of a function that doesn't return anything
1. `dict` or `dict(symbol->int)`: a dictionary, with optionally the datatypes of its key and value.
1. `table` or `table(c1:date;c2:symbol)`: a table, with optionally column names and datatypes
1. `fn` or `fn(date,long)->date`: a function, with optionally the datatypes of its parameters and return value.
1. `any`: any datatype.