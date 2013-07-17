pysoft-basic
============

1980s style console MS BASIC interpreter written in Python.

TODO: Almost everything.  The file `pysoft_parser.py` contains the parser
definition, using the excellent
[pyparsing](http://www.onlamp.com/pub/a/python/2006/01/26/pyparsing.html?page=1)
module, of a subset of BASIC (but a Turing-complete subset!)  This
needs a lot more unit tests, but those that are there can be run by
executing the file alone (it's meant to be imported by another Python
file).

Next job is to add a lot more unit tests.  After that,
to define actions to interpret the parse tree as actual code,
following Paul McGuire's model in [this StackOverflow answer](http://stackoverflow.com/questions/15154375/how-do-you-parse-node-and-node-relationships-in-pyparsing).
