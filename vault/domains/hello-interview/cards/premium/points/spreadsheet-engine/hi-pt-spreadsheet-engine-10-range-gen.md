---
id: hi-pt-spreadsheet-engine-10-range-gen
node: qb.lld.spreadsheet-engine.points
type: qa
step: 10
---
## Q
**电子表格引擎 · 区间与生成器**｜加分 · 出自：电子表格引擎 › 逐步扩展 3

`SUM(A1:B3)` 的依赖怎么登记？区间忽略空格子，而且函数要能随之更新，代码里用了什么 Python 写法，代价是什么？

## A
**做法。** 区间展开成它覆盖的每个格子登记依赖（空格子也登记），环检测和重算机制不用改。`cells_in` 是生成器，依赖和求值共用。

```python
def cells_in(a: str, b: str) -> Iterator[str]:
    for col in range(ord(a[0]), ord(b[0]) + 1):
        for row in range(int(a[1:]), int(b[1:]) + 1):
            yield f"{chr(col)}{row}"
```
**代价。** `SUM(A1:Z999)` 展开成 26 × 999 = 25,974 条边；大表要把区间当单独的依赖节点。
