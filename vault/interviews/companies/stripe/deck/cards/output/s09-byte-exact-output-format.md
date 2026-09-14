---
id: s09-byte-exact-output-format
node: stripe.output
type: qa
---

## Q
为什么候选人报告里反复出现 "spacing/commas errors causing rejection"？字节级精确的输出格式要逐项核对哪些点，怎么自查？

## A
**为什么考**：候选人报告里反复出现 "spacing/commas errors causing rejection"。

**清单**：
- 分隔符：`,` 还是 `, `？题面的样例是唯一真相，**复制粘贴样例**去对照。
- 小数位：`$0.00` 要两位，`0` 不行，`0.0` 也不行 → `f"{x:.2f}"`。
- 补零：`f"{n:016d}"`（16 位卡号）、`f"{h:02d}:{m:02d}"`。
- 千分位：`f"{n:,}"`（题面要求才加）。
- 空结果：`NONE`？空行？不输出？三选一，题面里找。
- 末尾换行：`print()` 自带 `\n`；用 `sys.stdout.write` 时自己补。
- **格式化只写在一个函数里**（`render`），改一次全对。

**自查方法**：

```python
assert out == expected, f"{out!r} != {expected!r}"   # repr 能看见空格和 \r
```
