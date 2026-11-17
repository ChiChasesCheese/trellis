---
id: api-specs-pre-post
node: api.specs
type: qa
step: 1
---
## Q
函数的规格（specification）里，前置条件和后置条件各是什么？它们怎样划分调用方和实现者的责任？

## A
**前置条件归调用方，后置条件归实现者**

- **前置条件（precondition）**：调用前必须成立的事，由调用方保证；
- **后置条件（postcondition）**：前置成立时，返回后必须成立的事——返回值、被改的状态、没改的状态；
- **契约**：调用方违反前置，实现者做什么都不算错（抛异常、返回乱值、崩溃）；前置满足而后置不成立，才是实现的 bug；
- **写法**：docstring 里分行写 Requires / Returns / Mutates，描述承诺，不描述实现步骤。

```python
import heapq

def pop_min(heap: list[int]) -> int:
    """Requires: heap is a non-empty min-heap.
    Returns: the smallest element, removed from heap.
    Mutates: heap only; what remains is still a min-heap."""
    return heapq.heappop(heap)

h = [3, 1, 2]
heapq.heapify(h)
print(pop_min(h), h[0])      # 1 2
```

<details class="pt"><summary>延伸</summary>

规格是调用方能依赖的全部。docstring 没写的行为，哪怕当前实现恰好如此，也不算承诺；调用方依赖它，等于押注实现永远不变。

</details>

**知识点：**规格与契约（Specifications）
