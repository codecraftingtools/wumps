Wumps
=====

The goal of this project is to define a widely useful macro
programming syntax suitable for defining domain-specific languages.
The aim is reduce the number of language keywords and built-in
constructs in favor of user-defined functions and macros.  Although I
have been pursuing the ideas encompassed by this project for quite a
while, this project is fairly new, so the documentation is currently
very scarce.  I hope to improve this over time.

Where to Start
--------------

For an idea of the language syntax, please see the `test_intro.wumps`_
file in the ``test`` subdirectory.  As you read over it, you can
examine the resulting parse tree in `test_results.txt`_ to help
understand how the language works.  The `grammar.pg`_ file will also
be of interest.  The parglare_ `grammar documentation`_ describes the
format of the grammar file.

Running the Parser
------------------

The ``wumps`` parser is written in Python 3.  If you want to try
running the parser yourself, first `install parglare`_.  Right now,
``wumps`` requires a modified branch of ``parglare``, so please use
the installation instructions below to install ``parglare``.  Also
note that I had to use ``pip3`` instead of ``pip`` as specified in
``parglare`` installation instructions.

::

  git clone -b recognizer-context https://github.com/codecraftingtools/parglare.git
  sudo pip3 install -e parglare

Next, clone the ``wumps`` git repository:

::

  git clone https://github.com/codecraftingtools/wumps.git

The parser can now be run like this:

::

  cd wumps
  ./parse.py test/test_intro.wumps

You can now make up your own grammar files and try them.

.. _test_intro.wumps: https://github.com/codecraftingtools/wumps/blob/master/test/test_intro.wumps
.. _test_results.txt: https://github.com/codecraftingtools/wumps/blob/master/test/test_results.txt
.. _grammar.pg: https://github.com/codecraftingtools/wumps/blob/master/wumps/grammar.pg
.. _parglare: https://github.com/igordejanovic/parglare
.. _grammar documentation: http://www.igordejanovic.net/parglare/grammar_language/
.. _install parglare: https://github.com/igordejanovic/parglare#installation
