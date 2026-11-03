---
id: craft-dependency-graph-cycle-detection-3-ancestors-not-visited
node: craft.patterns.dependency-graph-cycle-detection
type: qa
step: 3
---
## Q
**依赖图与环检测 · 遍历时用祖先链，而不是全局 visited**｜写法

遍历带符号链接（symlink）的目录树，要避免 `/a/loop -> /a` 这样的环导致无限递归。习惯写法是维护一个全局 `visited` 集合，见过的目录不再展开。这个写法在带环的目录树里会漏掉什么？

## A
**要点。** 环的定义是「从根走到当前节点的那条路上，又遇到了路上已有的节点」，所以判环用的是当前路径（祖先链），不是全局访问记录。全局 `visited` 回答的是「这个节点有没有来过」，而一个节点通过另一条合法路径再次到达，并不是环，输出里应该有它。

```python
class D:                                    # 目录：name + 子节点
    def __init__(self, name, kids=None): self.name, self.kids = name, kids or {}

real = D("real", {"f.txt": D("f.txt")}); a = D("a", {"real": real}); b = D("b")
a.kids["loop"] = a                          # 环：/a/loop 指回 /a
b.kids["alias"] = real                      # 合法的第二条路径：同一个目录经由 /b/alias 再到达一次
root = D("/", {"a": a, "b": b})

def walk(global_visited: bool):
    out, seen = [], set()
    stack = [("/", root, frozenset())]      # 栈里放 (路径, 节点, 祖先目录 id 集合)
    while stack:
        path, node, ancestors = stack.pop()
        out.append(path)
        if id(node) in ancestors or (global_visited and id(node) in seen):
            continue                        # 祖先链上已有（环），或（全局版）来过：不展开
        seen.add(id(node))
        chain = ancestors | {id(node)}      # 每个子节点拿到的是自己那条路的链
        for name in sorted(node.kids, reverse=True):
            stack.append((f"{path.rstrip('/')}/{name}", node.kids[name], chain))
    return out

print("祖先链:", walk(False))
print("全局 visited 版:", walk(True))
```

输出：

```
祖先链: ['/', '/a', '/a/loop', '/a/real', '/a/real/f.txt', '/b', '/b/alias', '/b/alias/f.txt']
全局 visited 版: ['/', '/a', '/a/loop', '/a/real', '/a/real/f.txt', '/b', '/b/alias']
```

**为什么。** `find` 命令的语义是「按路径列出」，`/b/alias/f.txt` 是一条真实存在的路径。全局 visited 把它当成环截断了，输出少了一行，而且没有任何报错。

**代价。** 祖先链每个节点要带一份集合（这里用不可变集合 `|` 出新集合），内存 O(深度) 每条路径；全局 visited 是 O(节点数) 一份。要在输出大小与正确性之间取舍时，先问「同一节点出现在两条路径上，算不算两个结果」：算，用祖先链；不算（只要可达节点集合），用全局 visited。

**对照。** 有向图里的 DFS 判环用「三色」（白未访问、灰在当前路径、黑已完成）：灰色就是这里的祖先链，黑色才等于全局 visited。
