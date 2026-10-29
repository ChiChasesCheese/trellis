---
id: tlc-create-maximum-number-4-followup
node: b.create-maximum-number
type: qa
step: 4
---
## Q
**LC 321 拼接最大数**｜追问

面试官接着问：（1）只有一个数组，要删掉 `k` 位使数**最小**（LC 402）？（2）每步后缀比较是 `O(k)`，能否更快？（3）两个字符串合并成字典序最大的串（LC 1754）？

## A
1. **单数组最小**：单调栈方向反过来，栈顶比当前数字**大**且还能删就弹；删不够从尾部截；最后去掉前导 0，空串返回 `"0"`。

```python
def remove_kdigits(num: str, k: int) -> str:
    stack: list[str] = []
    for ch in num:
        while k and stack and stack[-1] > ch:
            stack.pop()
            k -= 1
        stack.append(ch)
    return "".join(stack[: len(stack) - k]).lstrip("0") or "0"
```

2. **加速后缀比较**：把两个序列拼成 `a + [-1] + b`（`-1` 作分隔），建后缀数组或后缀排名，比较两个后缀就变成比较两个排名，`O(1)`。在 `k <= 1000` 时列表切片比较在 C 层执行，通常已足够快，先讲清楚瓶颈在哪即可。
3. **合并字符串（LC 1754）**：规则一样，`if a[i:] >= b[j:]` 直接比较字符串切片。

**Python 提醒**：`a[i:]` 每次都会复制一份新列表，`O(len)`；比较本身在第一个不同处就停，但复制不会提前停，这是它最坏 `O(k)` 的原因。
