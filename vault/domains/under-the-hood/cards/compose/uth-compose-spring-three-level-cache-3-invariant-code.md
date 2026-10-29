---
id: uth-compose-spring-three-level-cache-3-invariant-code
node: compose.spring-three-level-cache
type: qa
step: 3
---
## Q
**不变量与核心代码：先登记，后注入**｜Spring Framework · 7.0

三张表加一个集合要始终守住什么？用不到 30 行的 Python 写出“取 Bean”的流程。

## A
**不变量。**

- 一个名字同一时刻只在三张表之一：放进一级会删掉另两级，放进三级会删掉二级
- 名字在“正在创建”集合里，当且仅当它的创建流程还在调用栈上
- 顺序不能反：先把工厂登记进三级，再去注入依赖，环上的邻居才拿得到

**核心代码。** 第 4 步沿用早期引用：别人已经拿走了，最终对象就必须是同一个。

```python
from collections.abc import Callable


class Registry:
    def __init__(self, deps: dict[str, list[str]]) -> None:
        self.deps = deps                                       # 名字 -> 它要注入的名字
        self.done: dict[str, dict] = {}                        # 一级：成品
        self.early: dict[str, dict] = {}                       # 二级：早期引用
        self.factories: dict[str, Callable[[], dict]] = {}     # 三级：工厂
        self.creating: set[str] = set()                        # 正在创建的名字

    def get(self, name: str) -> dict:
        if name in self.done:                                  # 一级命中：直接返回
            return self.done[name]
        if name in self.creating:                              # 撞上“正在创建”的名字：循环依赖
            if name not in self.early and name in self.factories:
                self.early[name] = self.factories.pop(name)()  # 第一次被要：现在才产出早期引用
            if name in self.early:
                return self.early[name]
            raise RuntimeError(f"{name} 还没有对象可以提前暴露")
        self.creating.add(name)
        try:
            raw: dict = {"name": name}                         # 1 实例化：先造出空壳
            self.factories[name] = lambda: raw                 # 2 登记工厂：真实实现在这里决定要不要包代理
            for dep in self.deps[name]:
                raw[dep] = self.get(dep)                       # 3 注入：递归，可能又撞上自己
            self.done[name] = self.early.pop(name, raw)        # 4 别人拿过早期引用就沿用它，再升到一级
            return self.done[name]
        finally:                                               # 无论成败都收尾，三级、二级里的残留也在这里清掉
            self.creating.discard(name)
            self.factories.pop(name, None)
            self.early.pop(name, None)
```

**例题：** LC 133 克隆图

给无向连通图中一个节点的引用，返回该图的深拷贝（所有节点都是新建的）。每个节点有整数 `val` 和邻居列表 `neighbors`。节点数在 `[0, 100]`。例：邻接表 `[[2,4],[1,3],[2,4],[1,3]]` 克隆后结构相同。同一个思路：新节点先登记进表，再处理邻居，遇到环直接从表里取。

```python
from collections import deque

def clone_graph(node: Node | None) -> Node | None:
    if node is None:
        return None
    copies = {node: Node(node.val)}            # 原节点 -> 它的拷贝，同时充当 visited
    queue = deque([node])
    while queue:
        cur = queue.popleft()
        for nb in cur.neighbors:
            if nb not in copies:               # 第一次见到：先建拷贝再入队
                copies[nb] = Node(nb.val)
                queue.append(nb)
            copies[cur].neighbors.append(copies[nb])
    return copies[node]
```
