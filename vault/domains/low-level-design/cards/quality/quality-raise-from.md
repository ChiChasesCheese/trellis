---
id: quality-raise-from
node: quality.errors
type: qa
step: 6
---
## Q
```python
try:
    row = parse_row(line)
except ValueError:
    raise RowFormatError(line)
```
把底层的 `ValueError` 包装成一个更贴合业务语义的 `RowFormatError` 之后重新抛出，这样写丢了什么信息？怎么补上？

## A
直接 `raise RowFormatError(line)` 会切断和原始异常的联系——traceback 里只看得到 `RowFormatError` 是在 `except` 块里被创建的，看不出它的根因其实是一次 `ValueError`；调试时只能靠猜。

```python
try:
    row = parse_row(line)
except ValueError as exc:
    raise RowFormatError(line) from exc
```
`raise ... from exc` 会把原始异常挂在新异常的 `__cause__` 属性上，Python 打印 traceback 时会同时展示"底层原因"和"包装后的异常"两段完整链路,不丢失任何调试信息。如果确实想彻底隐藏底层细节（比如避免把内部实现暴露给 API 调用方）,可以显式写 `raise RowFormatError(line) from None`,告诉 Python 这是故意为之,而不是忘了带上 `from`。
