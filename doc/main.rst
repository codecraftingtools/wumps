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
:repo:`test/test_intro.wumps` example file.  As you read over it, you
can examine the resulting parse tree in :repo:`test/test_results.txt`
to help understand how the language works.  The
:repo:`wumps/lark/grammar.lark` file may also be of interest.  The
`Lark grammar documentation`_ describes the format of the grammar
file.

Installation Instructions
=========================

The Wumps parser is written `Python 3 <cc:python>` and requires the
`Lark <cc:lark>` Python package to operate.  Please set up a
``codecraftsmen`` virtual Python environment using `virtualenvwrapper
<cc:virtualenvwrapper-install>` and then follow the `installation
instructions <cc:lark-install>` for the Lark package.

Make sure that `Git <cc:git-install>` is installed and then pull down
the Wumps source code from `GitHub <cc:github>` using these commands::

  mkdir -p ~/git
  cd ~/git
  git clone https://github.com/codecraftingtools/wumps.git

This checkout of the Wumps repository can be installed in the
``codecraftsmen`` virtual environment like this::
  
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

.. _Lark grammar documentation:
   https://lark-parser.readthedocs.io/en/latest/grammar.html
