"""Start the verified Streamlit source distribution. The bundle contains Python and UI configuration only."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import runpy
import sys
import tempfile
from zipfile import ZipFile

repo = Path(__file__).resolve().parent
bundle = repo / "course_source.zip"
version = "5a9b9667890b05b289f563872d63b88540052264eb5611855452ab26cd260f06"
root = Path(tempfile.gettempdir()) / ("xuheng-course-" + version)
if not root.is_dir():
    if hashlib.sha256(bundle.read_bytes()).hexdigest() != version:
        raise RuntimeError("源码版本未通过校验。")
    with tempfile.TemporaryDirectory(prefix="xuheng-stage-",dir=root.parent) as tmp:
        stage = Path(tmp) / "source"
        stage.mkdir(mode=0o700)
        with ZipFile(bundle) as archive:
            for name in archive.namelist():
                relative=Path(name)
                if relative.is_absolute() or ".." in relative.parts:
                    raise ValueError("源码包目录异常。")
            archive.extractall(stage)
        try: stage.rename(root)
        except OSError:
            if not root.is_dir(): raise
if str(root) not in sys.path:
    sys.path.insert(0,str(root))
runpy.run_path(str(root/"streamlit_app.py"),run_name="__main__")
