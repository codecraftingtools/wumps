# Copyright (C) 2019, 2020, 2021 Jeffrey A. Webb
# Copyright (C) 2021 NTA, Inc.

"""
Wumps parser interface.
"""

from pathlib import Path

class Parser:
    def __init__(self, args):
        self._args = args

    def process_files_and_dirs(self, file_names):    
        for file_name in file_names:
            self.process_file_or_dir(file_name)
            
    def process_file_or_dir(self, file_name):
        file_path = Path(file_name)
        if file_path.is_dir():
            subdirs = []
            subpaths = file_path.iterdir()
            for subpath in sorted(subpaths):
                if subpath.is_dir():
                    subdirs.append(subpath)
                else:
                    self.process_file(subpath)
            for subdir in subdirs:
                self.process_file_or_dir(subdir)
        else:
            self.process_file(file_name)
            
    def process_file(self, file_name):
        raise Exception(f"process_file() not implemented in base class")
