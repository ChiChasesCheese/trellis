---
id: api-parameters-reject-not-clamp
node: api.parameters
type: qa
step: 2
---
## Q
报表接口的 `k` 取值 1 到 20，缺省 10。调用方传了 `k=500`，服务悄悄当成 20 处理并返回 200。这样做有什么问题，应该怎样处理越界和缺省？

## A
**越界报错，不要悄悄修正；缺省写进合同**

- **静默夹值（clamp）掩盖 bug**：调用方以为拿到了 500 条，实际只有 20，分页和统计从此对不上，没有任何错误提示；
- **报 400**：`invalid_k`，调用方马上知道自己的参数不对，合同里的“上限 20”是可见的；
- **缺省值是合同的一部分**：没传就是 10，写进文档和测试；缺省值改动是行为变更；
- **类型也严格**：`k` 是真的 `int`，`True`、`10.0`、`"10"` 都不是；`bool` 是 `int` 的子类，要用 `type(k) is int` 判断；
- **只校验当前路径用到的参数**：不同策略各用自己的参数，没用到的参数不需要校验，也不应该报错。

```python
DEFAULT_K, MAX_K = 10, 20

def top_k(items: list[int], k: int = DEFAULT_K) -> list[int]:
    if type(k) is not int or not 1 <= k <= MAX_K:
        raise ValueError("invalid_k")               # 不夹值：调用方的错要让他知道
    return sorted(items, reverse=True)[:k]

print(top_k(list(range(30)), 3))
try: top_k(list(range(30)), 500)
except ValueError as e: print(e)
```

**知识点：**参数设计（Parameters）
