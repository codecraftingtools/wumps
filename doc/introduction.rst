.. Copyright (C) 2018, 2020, 2021 Jeffrey A. Webb
   Copyright (C) 2021 NTA, Inc.

============
Introduction
============

Synopsis
========

To get an idea of the language syntax, you can take a look at the
:repo:`test/test_intro.wumps` example file.  As you read it over, you can
examine the resulting parse tree in :repo:`test/test_results.txt` to help
understand how the language works.  The :repo:`wumps/lark/grammar.lark` file
may also be of interest.  The `Lark grammar documentation`_ describes the
format of this grammar file.

Walk-Through
============

Let us now discuss the :repo:`test/test_intro.wumps` example in detail.

.. highlight:: none

Lines starting with the ``--`` character sequence are classified as comments
and are completely ignored by the parser.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 5
   :lines: 5

Blank lines are also discarded.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 6
   :lines: 6

The following simple expression contains only a single identifier.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 10
   :lines: 10

Simple identifiers like the one shown above are very similar to identifiers
in most programming languages (e.g. C and C++) and have similar restrictions.
Complex identifiers containing more unusual characters can be formed using
single quotes.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 14
   :lines: 14

Top-level expressions are separated by new lines or semicolons.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 17
   :lines: 17-18

Indentation is significant, so each of these lines is indented the same
amount.  The above code is not equivalent to what you see below.  Don't worry
about exactly what the code means for now.  We will address that later.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 23
   :lines: 23-24

Sequence elements are separated by commas.  Also note that partial line
comments are permitted.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 27
   :lines: 27

Expressions can span multiple lines by escaping the newline character
with a backslash.  Indentation of the continued line is insignificant.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 31
   :lines: 31-33

Another way to span multiple lines is by placing a continuation marker at the
end of the first line.  In this case, the continuation line(s) must be
indented.  If more than one continuation line is required, the subsequent
continuation lines must be aligned with the first continuation line.  No more
continuation markers are required on the continuation lines, however.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 41
   :lines: 41-43

Expressions can be named like this:

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 46
   :lines: 46

Even an empty expression can be named.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 49
   :lines: 49

Naming has a higher precedence than sequence construction.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 52
   :lines: 52

Parentheses can be used for controlling precedence.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 55
   :lines: 55

Empty parentheses can also be used to construct an empty sequence.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 58
   :lines: 58

Note that inside parentheses, new lines and alignment are ignored.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 61
   :lines: 61-64

Calls with a single argument can be written like this.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 67
   :lines: 67

Multiple arguments can be passed as a sequence.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 73
   :lines: 73

A call with no arguments can be made by using an empty sequence as an
argument.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 77
   :lines: 77
           
Multiple argument calls can also nest.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 80
   :lines: 80
           
Named expressions can be used to form keyword arguments.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 83
   :lines: 83
           
The positional arguments are not required to be first.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 86
   :lines: 86

Keyword arguments might not have a value.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 89
   :lines: 89

Although multiple positional arguments cannot be passed to a function without
using parentheses, additonal keyword arguments can be tacked on the end of a
function call.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 94
   :lines: 94

The above expression is equivalent to this one:

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 97
   :lines: 97

One positional argument and many keyword arguments can be called without
using parentheses.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 101
   :lines: 101

Some of the expressions above are not easy to understand, so don't write
things like that just because you can.  Hang in there and you will hopefully
see the reason for some of these features very soon.

Whitespace is significant, like in YAML or Python.  In Wumps, indentation can
be used to create a sequence.  An increase in indentation begins a sequence
of newline-separated expressions, and a decrease in indentation ends the
sequence.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 124
   :lines: 124-126

The above code is equivalent to this:

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 129
   :lines: 129

Nesting works.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 132
   :lines: 132-136

The above expression is equivalent to this:

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 139
   :lines: 139

This allows us to build flow-control constructs using a function call syntax
instead of using language keywords.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 143
   :lines: 143-148

A *partial unindent* is seen as an implicit continuation of the parent
expression, allowing things like this:

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 152
   :lines: 152-155

For some constructs, named arguments might be repeated.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 158
   :lines: 158-163

Another way to create a sequence is to use braces.  Inside the braces,
expressions are separated by semicolons, but new lines and indentation are
ignored.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 168
   :lines: 168-170

We have just been using literals so far, but native types like integers,
floats, and strings are also supported.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 174
   :lines: 174

The syntax is good for declarative uses as well.

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 177
   :lines: 177-188

Here is an example with nested named items:

.. literalinclude:: ../test/test_intro.wumps
   :linenos:
   :lineno-start: 191
   :lines: 191-194

More Examples
=============

Some more contrived examples (mostly for testing purposes) can be found in
the :repo:`test` directory.  These examples may be of interest to those
wanting to understand the language syntax in more detail.  The resulting
parse trees are also included in :repo:`test/test_results.txt`.

.. _Lark grammar documentation:
   https://lark-parser.readthedocs.io/en/latest/grammar.html
