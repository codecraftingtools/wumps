.. Copyright 2018, 2020, 2021 Jeffrey A. Webb

===============
Getting Started
===============

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

.. comment
   
  This checkout of the Wumps repository can be installed in the
  ``codecraftsmen`` virtual environment like this::
    
    cd ~/git
    workon codecraftsmen
    pip install -e wumps

No futher installation is required.

Running the Parser
==================

The parser can now be run like this:

::

  workon codecraftsmen
  cd ~/git/wumps
  ./wumps.py --ast test/test_intro.wumps

where ``test/test_intro.wumps`` is the Wumps-formatted input file to be processed.

