///@title Sample
///@overview A sample q script annotated with documentation comments.
///@owner [Darren Sun](https://github.com/darrenwsun)

///Check if a path is an existing directory.
///@param path {hsym} A file system path.
///@return {boolean} `1b` if `path` is an existing directory; `0b` otherwise.
///@signal {TypeError} If `path` is not an hsym.
///@see {@link .sample.isfile} For file check.
///@example
///q).sample.isdir `:src
///1b
///q).sample.isdir `src
///'TypeError: not an hsym
.sample.isdir:{[path]
  if[not .sample.ishsym path; ' "TypeError: not an hsym"];
  ()~key path};

///Check if a path is an existing file.
///@param path {hsym} A file system path.
///@return {boolean} `1b` if `path` is an existing file; `0b` otherwise.
///@signal {TypeError} If `path` is not an hsym.
///@see {@link .sample.isdir} For directory check.
///@example
///q).sample.isfile `:tests/resources/sample.q
///1b
///q).sample.isfile "tests/resources/sample.q"
///'TypeError: not an hsym
.sample.isfile:{[path]
  if[not .sample.ishsym path; ' "TypeError: not an hsym"];
  path~key path};

///Check if a given value is an hsym.
///@param x {any} Anything.
///@return {boolean} `1b` if `x` is an hsym; `0b` otherwise.
///@example
///q).sample.ishsym `:/tmp/abc
///1b
///q).sample.ishsym `$"/tmp/abc"
///0b
.sample.ishsym:{[x]
  if[-11h<>type x; :0b];
  $[":"=first string x; 1b; 0b]
 };

///Return the day of the week as an integer, where Monday is 1 and Sunday is 7.
///@param d @atomic {date} A date.
///@return {long} The day of the week.
.sample.isoweekday:{[d] (d-1) mod 7 };