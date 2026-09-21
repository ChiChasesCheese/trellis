---
id: robust-except-exception-specific-first
node: engineering.robustness
type: qa
source: python-docs
---
## Q
捕获异常时为什么建议先列出具体的异常类型（如 `OSError`、`ValueError`），把 `except Exception` 放在最后，而且 `except Exception` 分支里往往要 `raise` 重新抛出？

## A
`Exception` 能当作几乎捕获一切的通配符，但把它当第一选择会连自己没预料到的错误也悄悄吞掉，掩盖真正的 bug。好的做法是先精确处理已知的异常类型，最后用 `except Exception as err` 兜底并打印或记录日志后 `raise` 重新抛出，让调用方仍能感知并处理这个意外错误，而不是让程序假装没事地继续跑。
