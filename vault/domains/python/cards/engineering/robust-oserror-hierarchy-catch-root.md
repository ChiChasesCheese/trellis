---
id: robust-oserror-hierarchy-catch-root
node: engineering.robustness
type: qa
source: python-docs
---
## Q
标准库的 `ConnectionError`、`BlockingIOError`、`ChildProcessError` 等都是 `OSError` 的子类，这种设计对调用方捕获异常有什么好处？库作者可以怎样效仿这个模式？

## A
调用方只需 `except OSError` 就能一次性捕获所有操作系统相关的失败，不必逐个列出每种具体错误；需要区分时，再单独捕获更具体的子类（如 `ConnectionError`）。库作者可以照此模式为自己的库定义一个根异常类（继承自 `Exception`），库内所有异常都从这个根类派生，调用方只需捕获这一个根类型就能拦住库抛出的一切错误，同时不会误伤库之外的异常。
