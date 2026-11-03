"""电子表格引擎（Spreadsheet Engine）——起始模板。

公开的类名、方法签名和异常都和 `solution.py` 一致；把 `raise NotImplementedError` 的方法体补全。
"""

from __future__ import annotations


class SpreadsheetError(Exception):
    """所有失败路径的公共基类。"""


class InvalidCellError(SpreadsheetError, ValueError):
    """单元格名不合法：只接受 A1 到 Z999（一个大写字母加 1 到 3 位行号，行号不以 0 开头）。"""


class InvalidFormulaError(SpreadsheetError, ValueError):
    """公式语法错误，或字面量既不是数字也不是公式。"""


class CycleError(SpreadsheetError, ValueError):
    """这次赋值会让公式互相依赖成环（含自己引用自己）。"""


class EvalError(SpreadsheetError, ArithmeticError):
    """公式求值失败（除以零）；依赖出错格子的公式得到同样的错误。"""


class Spreadsheet:
    eval_count: int  # 第 3 关：公式被求值的累计次数（字面量不计）

    def __init__(self) -> None:
        raise NotImplementedError

    def set(self, cell: str, raw: str) -> None:
        """给格子赋值。raw 是数字字面量（"42"、"-3.5"）、以 "=" 开头的公式，或 "" 表示清空。

        - 格子名不合法抛 InvalidCellError；公式或字面量写错抛 InvalidFormulaError，且格子保持原样。
        - 第 1 关：公式只有用 + 连起来的数字和格子引用（"=A1+B2+3"，加号两边可以有空格）。
          会成环（含自己引用自己）抛 CycleError，且整张表保持原样。
        - 第 2 关：完整表达式 + - * /、括号、一元负号（"=A1*(B1+2)"）；除以零不在 set 时抛，而是 get 时抛 EvalError。
        - 第 4 关：SUM / MIN / MAX 加区间，如 "=SUM(A1:B3)"；区间必须左上到右下。
        """
        raise NotImplementedError

    def get(self, cell: str) -> float:
        """返回格子的值（float）。空格子是 0.0；格子的公式出错时抛 EvalError（第 2 关起）；格子名不合法抛 InvalidCellError。"""
        raise NotImplementedError
