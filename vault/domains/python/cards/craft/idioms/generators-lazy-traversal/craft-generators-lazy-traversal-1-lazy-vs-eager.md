---
id: craft-generators-lazy-traversal-1-lazy-vs-eager
node: craft.idioms.generators-lazy-traversal
type: qa
step: 1
---
## Q
**生成器与惰性遍历 · 为什么 `find` 用 `yield` 产出结果，而不是先收集成列表再返回**｜写法

文件搜索要在一棵很大的目录树里找匹配项。调用方常常只想要第一个，或者前十个。把所有匹配项收集进列表再返回，和用 `yield` 一个个产出，各自的代价是什么？怎样用测试**证明**它真的是惰性的？

## A
**要点。** 生成器（generator）函数里每个 `yield` 都会暂停函数，把一个值交给调用方，调用方再要下一个时才从暂停处继续。所以工作量跟着**调用方消费了多少**走：只取第一个就只走了一步。列表版必须先走完整棵树，才能返回第一个；树大时既慢又占内存，调用方还不能提前停。

```python
@dataclass
class Node:
    name: str
    children: list["Node"]

@dataclass
class Stats:
    visited: int = 0

def make(depth: int, width: int) -> Node:
    if depth == 0:
        return Node("leaf", [])
    return Node(f"n{depth}", [make(depth - 1, width) for _ in range(width)])

def walk_eager(root: Node, stats: Stats) -> list[Node]:
    out, stack = [], [root]
    while stack:
        n = stack.pop(); stats.visited += 1; out.append(n)
        stack.extend(reversed(n.children))
    return out                                     # 先把整棵树走完，才返回

def walk_lazy(root: Node, stats: Stats) -> Iterator[Node]:
    stack = [root]
    while stack:
        n = stack.pop(); stats.visited += 1
        yield n                                    # 调用方要一个，才走一步
        stack.extend(reversed(n.children))

root = make(depth=6, width=4)                      # 4^6 个叶子, 总共几千个节点
s1, s2 = Stats(), Stats()
first = walk_eager(root, s1)[0]
print("eager 取第 1 个节点, 实际访问了", s1.visited, "个")
first = next(walk_lazy(root, s2))
print("lazy  取第 1 个节点, 实际访问了", s2.visited, "个")
s3 = Stats()
it = walk_lazy(root, s3)
list(zip(range(10), it))                           # 只取前 10 个
print("lazy  取前 10 个, 访问了", s3.visited, "个")
```

实际输出：

```
eager 取第 1 个节点, 实际访问了 5461 个
lazy  取第 1 个节点, 实际访问了 1 个
lazy  取前 10 个, 访问了 10 个
```

**怎么证明惰性。** 只看返回结果对不对证明不了惰性，因为两种写法的结果一样。`find` 的测试给搜索器传入一个统计对象（`FindStats.visited`），测试里断言「取第一个后 `visited == 1`」。计数器是可观测的副作用，正好能区分两种写法。

**代价。** 惰性意味着工作被推迟到消费时：创建生成器不执行任何代码，异常和副作用都发生在被消费的那一刻（见第 3 张卡）；并且调用方要处理「半途停止」时的资源清理。
