=====
Wumps
=====

The goal of this project is to define a widely useful macro
programming syntax suitable for defining domain-specific languages.
The aim is to reduce the number of language keywords and built-in
constructs in favor of user-defined functions and macros.

`Wumps`_ is part of the `Code Craftsmen`_ project.  The
`documentation`_ is hosted on `Read the Docs`_ and the `source code`_
can be found on `GitHub`_.

Status
======

At this point, the grammar is fairly complete and the parser is able
to parse source files and build an abstract syntax tree.  Although the
ideas encompassed by this project have been developing for quite a
while, the code base is fairly new.  As one might expect, the current
documentation is sparse, but this will hopefully improve over time.

Where to Start
==============

To get an idea of the language syntax, please see the
`test_intro.wumps`_ file in the ``test`` subdirectory.  As you read
over it, you can examine the resulting parse tree in
`test_results.txt`_ to help understand how the language works.  The
`grammar.lark`_ file may also be of interest.  The `Lark grammar
documentation`_ describes the format of the grammar file.

Installation Notes
==================

The Wumps parser is written in `Python 3`_ and requires the `Lark`_
Python package to operate.  Please set up a ``codecraftsmen`` virtual
Python environment using `virtualenvwrapper`_ and then follow the
`installation instructions for the Lark package <lark-install_>`_.

Make sure that `Git`_ is installed and then pull down the Wumps source
code from `GitHub`_ using these commands::

  mkdir -p ~/git
  cd ~/git
  git clone https://github.com/codecraftingtools/wumps.git

This checkout of the Wumps repository can be installed in the
`codecraftsmen` virtual environment like this::
  
  cd ~/git
  workon codecraftsmen
  pip install -e wumps

Running the Parser
==================

The parser can now be run like this:

::

  workon codecraftsmen
  cd ~/git/wumps
  ./lark_parse.py --ast test/test_intro.wumps

You can now make up your own source files using the Wumps syntax and
parse them.

.. _Wumps: https://www.codecraftsmen.org/software.html#wumps
.. _Code Craftsmen: https://www.codecraftsmen.org
.. _documentation: https://wumps.readthedocs.io
.. _Read the Docs: https://www.codecraftsmen.org/foundation.html#read-the-docs
.. _source code: https://github.com/codecraftingtools/wumps
.. _GitHub: https://www.codecraftsmen.org/foundation.html#github
.. _test_intro.wumps: https://github.com/codecraftingtools/wumps/blob/master/test/test_intro.wumps
.. _test_results.txt: https://github.com/codecraftingtools/wumps/blob/master/test/test_results.txt
.. _grammar.lark: https://github.com/codecraftingtools/wumps/blob/master/wumps/lark/grammar.lark
.. _Lark grammar documentation: https://lark-parser.readthedocs.io/en/latest/grammar.html
.. _Python 3: https://www.codecraftsmen.org/foundation.html#python
.. _Lark: https://www.codecraftsmen.org/foundation.html#lark
.. _virtualenvwrapper:
      https://www.codecraftsmen.org/virtualenvwrapper-notes.html#virtualenvwrapper-install
.. _lark-install:
      https://www.codecraftsmen.org/lark-notes.html#lark-install
.. _Git: https://www.codecraftsmen.org/git-notes.html#git-install
