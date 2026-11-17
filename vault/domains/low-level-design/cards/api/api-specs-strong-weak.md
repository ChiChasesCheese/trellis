---
id: api-specs-strong-weak
node: api.specs
type: qa
step: 2
---
## Q
两个规格 A、B 怎么比强弱？为什么“前置更弱、后置更强”的规格可以替换另一个？

## A
**弱前置加强后置，才是更强的规格**

- **更强**：接受更多输入（前置弱），承诺更多结果（后置强）；
- **可替换**：把实现从规格 A 换成强于 A 的规格 B，按 A 写的调用方不会坏，这就是里氏替换在单个函数上的样子；
- **反过来会坏**：收紧前置（多拒一些输入）或放松后置（少承诺），老调用方就可能出错；
- **代价**：规格越强，实现越难、行为越被锁死；弱规格给实现者自由，例如“返回任意一个下标”。

```python
def find_a(xs, v):
    """Requires: v in xs.  Returns: some i with xs[i] == v."""
    return xs.index(v)

def find_b(xs, v):
    """Requires: nothing.  Returns: the first i with xs[i] == v, else -1."""
    return xs.index(v) if v in xs else -1

print(find_a([5, 7, 5], 5), find_b([5, 7, 5], 9))     # 0 -1
```

<details class="pt"><summary>延伸</summary>

`find_b` 比 `find_a` 强，但 `-1` 是个哨兵值，调用方忘了判断就会拿它当下标用（`xs[-1]` 是最后一个元素，不报错）。强规格也要看返回值的设计，这是返回值那一叶的话题。

</details>

**知识点：**规格与契约（Specifications）
