"""前置课练习的共享 fixture。

默认加载你的作答文件 exNN_*.py；设置环境变量 EX_IMPL=solution 则加载 solutions/exNN_solution.py，
用来验证参考答案本身是对的（`EX_IMPL=solution python -m pytest -q`）。
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent


def load_exercise(test_file: str):
    """test_ex01.py → ex01_*.py（或 solutions/ex01_solution.py）。"""
    num = Path(test_file).stem.split("_")[1]  # "ex01"
    if os.environ.get("EX_IMPL") == "solution":
        path = HERE / "solutions" / f"{num}_solution.py"
    else:
        matches = sorted(p for p in HERE.glob(f"{num}_*.py") if not p.name.startswith("test_"))
        if not matches:
            pytest.skip(f"没有找到 {num}_*.py")
        path = matches[0]
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def ex(request):
    return load_exercise(str(request.fspath))
