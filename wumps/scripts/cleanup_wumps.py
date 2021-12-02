#!/usr/bin/env python3

# Copyright (C) 2021 NTA, Inc.

import os

# Clean up backup and Python cache files from wumps
if __name__ == "__main__":
    os.system("find . -name '__pycache__' | xargs rm -rf")
    os.system("find . -name '*~' | xargs rm -f")
