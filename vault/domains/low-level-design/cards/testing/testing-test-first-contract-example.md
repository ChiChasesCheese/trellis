---
id: testing-test-first-contract-example
node: testing.test-first
type: qa
step: 2
---
## Q
需求文档给了几组「输入 → 输出」的例子（运费：首 500 克 400 分，之后每 100 克加 50 分，不足按 100 克算）。动手实现之前，为什么要把这些例子逐字写成测试？例子在旧代码上本来就是绿的时候，说明什么？

## A
**例子是最便宜的参照答案，绿了不等于没缺陷**

- **逐字抄**：期望值照文档写，不要自己心算一遍再写，心算的错会和实现的错互相掩护；
- **先于实现**：先有测试，实现时每写一步都能跑，不用等到最后才发现理解偏了；
- **例子只是抽样**：文档里的几行不会覆盖全部边界；每个你在读合同时发现的现象，要自己写一个失败测试；
- **旧代码上本来就绿**：这个例子没碰到缺陷。不要因此认为代码没问题，而是回头逐条对照合同，找例子没覆盖的规则；
- **示例的位置**：放进参数化列表，之后新增例子只加一行。

```python
def shipping_cents(grams: int) -> int:
    extra = max(0, grams - 500)
    return 400 + -(-extra // 100) * 50       # 向上取整到 100 克

EXAMPLES = [(500, 400), (501, 450), (1000, 650)]    # 文档里的例子，逐字抄
for grams, want in EXAMPLES:
    assert shipping_cents(grams) == want, (grams, shipping_cents(grams))
print("examples green")
```

**知识点：**先写失败的测试（Test First）
