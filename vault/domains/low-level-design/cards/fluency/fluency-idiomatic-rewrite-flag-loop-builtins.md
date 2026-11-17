---
id: fluency-idiomatic-rewrite-flag-loop-builtins
node: fluency.idiomatic-rewrite
type: qa
step: 1
---
## Q
订单行里找“第一个数量超过上限的行”，同事写成：先 `found = None`，循环里命中就赋值并 `break`，最后返回 `found`。另一处“找金额最大的行”也是 `best = None` 加比较。这些手写循环怎么改成地道写法，改完哪些地方要小心？

## A
**“找一个”用 `next`，“取最大”用 `max`，别手写标志位**

- **找第一个**：`next((r for r in rows if cond), None)`，生成器遇到第一个命中就停，和 `break` 的行为一样，默认值写在最后；
- **取最大**：`max(rows, key=…, default=None)`；平局时返回最先出现的那个，和 `>` 比较的手写循环一致；
- **默认值不能省**：空序列上 `max(...)` 直接抛 `ValueError`，`next(...)` 抛 `StopIteration`，要么给 `default`，要么确认调用方保证非空；
- **生成器里别裸用 `next`**：在生成器函数内部，漏出的 `StopIteration` 会变成 `RuntimeError`（PEP 479），必须带默认值；
- **什么时候不改**：循环体里还要记日志、累计多个结果、早退时做别的事，一个标志位三个出口的逻辑塞进表达式只会更难读。

```python
rows = [{"id": 1, "qty": 3}, {"id": 2, "qty": 9}, {"id": 3, "qty": 9}]

found = None                              # 手写版
for r in rows:
    if r["qty"] > 5:
        found = r
        break

same = next((r for r in rows if r["qty"] > 5), None)     # 地道版
big = max(rows, key=lambda r: r["qty"], default=None)    # 平局取先出现的
print(found == same, big["id"], max([], default=None))   # True 2 None
```

<details class="pt"><summary>延伸</summary>

改写不是目的：每次改动要能说出一条好处（少一个可变变量、默认值显式、意图一眼可见）。说不出就别改。

</details>

**知识点：**改写成地道代码（Idiomatic Rewrite）
