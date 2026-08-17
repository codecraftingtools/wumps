#!/usr/bin/env python3

# Copyright (C) 2021 Jeffrey A. Webb

import os
import sys
from pathlib import Path

test_root = Path(sys.path[0])
wumps_root = (test_root / "..").resolve()
wumps_script = "./wumps/scripts/process_wumps.py"
test_root = test_root.relative_to(wumps_root)
results = "./new_results.txt"

cmd = f"cd {wumps_root} && {wumps_script} --print-ast {test_root}/test_*.wumps > {results}"
print("running:", cmd)
os.system(cmd)
