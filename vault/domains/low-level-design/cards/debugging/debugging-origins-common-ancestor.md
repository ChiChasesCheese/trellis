---
id: debugging-origins-common-ancestor
node: debugging.failure-origins
type: qa
step: 4
---
## Q
片单服务里，用户 B 能看到、往里加片、甚至删除用户 A 的片单。三个方法都越权了，是要给三个方法分别补检查吗？

## A
**多个症状指向同一个祖先：先找它们共同调用的那一处**

- **看症状的共同点**：三个方法都先调同一个读取函数 `_get`；
- **缺陷在 `_get`**：它按 id 取片单，却没有比较拥有者；三个方法只是三个受害者；
- **在祖先处修一次**：别的方法有没有做拥有者检查，都不再重要；将来新增的第四个方法自动安全；
- **在每个方法里补检查是错的处理**：改了四处，漏改第五处，缺陷还活着；
- **验证要走遍所有症状**：为三个方法各写一条越权用例，修祖先后全部变绿，证明真的是同一个根因。

```python
class Lists:
    def __init__(self): self._data = {1: ("ann", ["m1"])}   # id -> (拥有者, 片单)
    def _get(self, pid, user):
        owner, items = self._data[pid]
        if owner != user: raise KeyError(pid)               # 修在这里：一处
        return items
    def view(self, pid, user): return list(self._get(pid, user))
    def add(self, pid, user, m): self._get(pid, user).append(m)
    def remove(self, pid, user, m): self._get(pid, user).remove(m)

lists = Lists()
for op in (lambda: lists.view(1, "bob"), lambda: lists.add(1, "bob", "m2"),
           lambda: lists.remove(1, "bob", "m1")):
    try: op()
    except KeyError: print("拒绝")          # 三次“拒绝”
```

<details class="pt"><summary>延伸</summary>

找祖先的方法：列出出错的所有函数，看它们的调用链在哪里汇合；或者在共同入口处打日志，看错值最早出现在哪一层。

</details>

**知识点：**追踪失败源头（Tracking Failure Origins）
