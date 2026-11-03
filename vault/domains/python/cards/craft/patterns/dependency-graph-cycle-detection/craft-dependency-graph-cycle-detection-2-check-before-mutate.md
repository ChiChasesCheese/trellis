---
id: craft-dependency-graph-cycle-detection-2-check-before-mutate
node: craft.patterns.dependency-graph-cycle-detection
type: qa
step: 2
---
## Q
**依赖图与环检测 · 用户每改一个格子，怎样在改之前就拒绝成环**｜模式

电子表格里每个格子的公式会读别的格子。用户把 A1 改成 `=C1`，而 C1 读 B1、B1 读 A1。如果先写入新公式、再在重算时发现环，要处理什么？有什么办法让「拒绝」时表格一个字节都不变？

## A
**要点。** 动态改图时，环检测放在任何状态修改之前：新公式要读的格子集合是 `reads`，从 `reads` 沿「它读了谁」的边走，若能走到被改的格子本身，新边就会闭成环。这是一次只读的可达性（reachability）搜索，不需要先建边再检测。

```python
class Sheet:
    def __init__(self):
        self.deps = {}         # 格 -> 它的公式读了哪些格
        self.users = {}        # 格 -> 谁读了它（反向边，重算用）

    def reaches(self, starts, target):
        """从 starts 沿"读了谁"走，能碰到 target 就说明新公式会闭成环。"""
        seen, stack = set(), list(starts)
        while stack:
            c = stack.pop()
            if c == target: return True
            if c not in seen:
                seen.add(c); stack.extend(self.deps.get(c, ()))
        return False

    def set(self, cell, reads):
        if self.reaches(reads, cell):          # 先查环，再改任何状态
            raise ValueError(f"{cell} would depend on itself")
        for d in self.deps.pop(cell, set()):   # 摘掉旧边
            self.users[d].discard(cell)
        self.deps[cell] = reads                # 到这里才开始改
        for d in reads:
            self.users.setdefault(d, set()).add(cell)

s = Sheet(); s.set("B1", {"A1"}); s.set("C1", {"B1"})      # B1 读 A1，C1 读 B1
before = ({k: set(v) for k, v in s.deps.items()}, {k: set(v) for k, v in s.users.items()})
try: s.set("A1", {"C1"})                                    # A1 -> C1 -> B1 -> A1
except ValueError as e: print("拒绝：", e)
print("状态没动：", before == (s.deps, s.users))
```

B1 读 A1、C1 读 B1，再把 A1 改成读 C1：

```
拒绝： A1 would depend on itself
状态没动： True
```

**为什么。** 先改后查的版本，失败时要回滚两张表（正向边和反向边）和已经重算过的值，漏回滚一项就是脏状态。先查后改，拒绝的路径是零副作用，不需要回滚代码，也不会有回滚本身出错。解析公式同理：语法错误在 `parse_raw` 就抛，那时表格也没动过。

**代价。** 每次 `set` 多一次 O(可达格子数) 的遍历；表格很大、更新频繁时要缓存或限制检查范围。

**易错。** 新旧公式读的格子不同，旧边必须先摘干净再建新边，否则反向边表里留着已经不存在的依赖，之后重算会算多余的格子。
