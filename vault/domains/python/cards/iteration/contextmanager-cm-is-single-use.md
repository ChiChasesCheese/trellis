---
id: contextmanager-cm-is-single-use
node: iteration.context-managers
type: qa
source: python-docs
---
## Q
用 `@contextmanager` 创建的上下文管理器实例（如 `cm = my_ctx()`）能不能被两个不同的 `with cm:` 块各用一次？

## A
不能，它是一次性（single-use）的：第一次 `with cm:` 结束后，底层生成器已经跑到 yield 之后的清理代码并耗尽。第二次再 `with cm:` 会重新调用它的 `__enter__()`，但生成器已经无法再产出一次值，Python 会检测到「生成器没有 yield」并报错。要重复使用，需要每次都重新调用工厂函数产生一个新的生成器实例，而不是复用同一个 `cm`。
