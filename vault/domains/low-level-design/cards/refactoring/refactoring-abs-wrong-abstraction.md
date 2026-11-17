---
id: refactoring-abs-wrong-abstraction
node: refactoring.over-abstraction
type: qa
step: 1
---
## Q
两个报表函数有六行很像，第二个人把它们合并成一个带 `csv`、`total`、`mask`、`title` 四个开关的 `export`。这个合并为什么可能比重复更贵？“重复三次再抽象”是什么道理？

## A
**抽象是在押注“这些差异不会继续分化”；押错了，比重复更难受**

- **两处相似不等于同一个概念**：它们现在长得像，可能因为不同的原因各自演化；
- **每多一个调用方，就多一个开关**：开关之间还会互相影响（`mask` 时不能显示 `total`），读代码的人要在脑子里跑所有组合；
- **改一个调用方，要小心不弄坏另一个**：合并之前它们是互不影响的；
- **重复的代价是有上限的**：两三份几行的重复，修改时多改几处；错误的抽象，每次改动都要穿过它；
- **三次规则**：第三次出现时，你才同时看到三个真实的用例，能看出什么是真正共同的、什么是各自不同的。

```python
def export(rows, *, csv=False, total=False, mask=False, title=None):    # 合并后的版本
    out = [title] if title else []
    for name, amt in rows:
        amt = "***" if mask else amt
        out.append(f"{name},{amt}" if csv else f"{name}: {amt}")
    if total and not mask: out.append(f"total={sum(a for _, a in rows)}")
    return "\n".join(out)

def report(rows): return "\n".join(f"{n}: {a}" for n, a in rows)          # 两个直白的版本
def csv_dump(rows): return "\n".join(f"{n},{a}" for n, a in rows)

rows = [("a", 1), ("b", 2)]
assert export(rows) == report(rows) and export(rows, csv=True) == csv_dump(rows)
print(report(rows), csv_dump(rows), sep="\n")
```

**知识点：**过度抽象（Over-Abstraction）
