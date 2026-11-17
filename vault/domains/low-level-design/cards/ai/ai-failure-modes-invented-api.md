---
id: ai-failure-modes-invented-api
node: ai.failure-modes
type: qa
step: 1
---
## Q
智能体交来的代码里有一行调用了 `d.getOrDefault(w, 0)`，测试恰好没走到这一行。怎么发现这类“方法名看着对、其实不存在”的调用？

## A
**没跑过的一行，就是没验证过的一行**

- **表现**：属性不存在只在执行到那一行时抛 `AttributeError`，导入时不报，空输入、常见路径都正常；
- **来源**：名字常常是别的语言或别的库里真有的方法（`getOrDefault` 是 Java 的 `Map` 方法）；
- **查法**：让代码真的跑到（覆盖率看这一行有没有被执行），或者用类型检查器——写了类型注解的函数里，mypy 会直接报“没有这个属性”；
- **版本也是一种不存在**：`str.removeprefix` 要 3.9 以上，`datetime.UTC` 要 3.11 以上；对不确定的名字查官方文档，不凭“看着像”。

```python
def count(words: list[str]) -> dict[str, int]:
    d: dict[str, int] = {}
    for w in words:
        d[w] = d.getOrDefault(w, 0) + 1     # 语法合法，导入不报错
    return d

print(count([]))                            # {}：没走到那一行，看起来正常
try: count(["a"])
except AttributeError as e: print(e)        # 'dict' object has no attribute 'getOrDefault'
```

<details class="pt"><summary>延伸</summary>

没有类型注解的函数，mypy 默认不检查函数体（文档里的 `check_untyped_defs` 默认关闭）。给要验证的函数补上注解，类型检查才看得到这类错误。

</details>

**知识点：**AI 的典型错误（Failure Modes）
