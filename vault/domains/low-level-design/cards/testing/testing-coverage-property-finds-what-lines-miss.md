---
id: testing-coverage-property-finds-what-lines-miss
node: testing.coverage-limits
type: qa
step: 4
---
## Q
把一笔账平均分给 n 个人的函数 `split_cents(total, n)`，示例测试 `split_cents(100, 4) == [25] * 4` 通过，行覆盖和分支覆盖都是 100%。为什么它仍然是错的，性质测试（property-based testing）怎么抓住它？

## A
**示例只验证挑好的输入，性质验证所有输入**

- **覆盖的是路径，不是数据**：函数只有一行，示例把这一行跑了一遍就是 100%；而 `total` 不能被 `n` 整除时余数丢了；
- **性质**：不依赖具体实现、对任意输入都成立的断言：各份之和等于总额（下面的代码只检查这一条），还可以加上各份之差不超过 1 分；
- **随机输入加性质**：生成大量 `(total, n)`，每一对都检查性质，找到的反例就是一个现成的回归用例；
- **固定种子**：失败要能复现，用固定种子的 `random.Random`；`hypothesis` 在此之上还会生成边界值并把反例缩到最小；
- **性质别照抄实现**：拿被测公式再算一遍等于没测；用守恒、对称、往返（`decode(encode(x)) == x`）这类外部事实。

```python
import random

def split_cents(total, n):
    return [total // n] * n                      # 余数丢了

assert split_cents(100, 4) == [25] * 4           # 示例测试：100% 覆盖，通过
rng = random.Random(7)
for _ in range(1000):
    total, n = rng.randint(0, 10**6), rng.randint(1, 12)
    parts = split_cents(total, n)
    if sum(parts) != total:                      # 性质：总额守恒
        print("counterexample:", total, n, parts); break
```

<details class="pt"><summary>延伸</summary>

修法是 `q, r = divmod(total, n)`，前 `r` 份各多 1 分。性质测试和变异测试互补：前者扩大输入，后者检查断言是否够强。

</details>

**知识点：**覆盖率的边界（Coverage Limits）
