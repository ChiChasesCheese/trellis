---
id: reading-mindiff-follow-existing
node: reading.minimal-diff
type: qa
step: 2
---
## Q
给一个已有的片单服务加“重命名片单”功能。代码里所有方法都先调用同一个 `_get(pid, user)` 取片单并检查所有者。你想自己写一个更“优雅”的检查，为什么不该这么做？

## A
**沿用现有的约定和抽象：新代码要像原来的代码，而不是像你**

- **已有的 helper 里藏着看不见的规则**：`_get` 已经做了存在检查和所有权检查；绕过它，新方法可能漏掉其中一条；
- **一致性比局部的“更好”更值钱**：读代码的人看到相同的形状，就知道每个方法都一样安全；
- **风格也一样**：命名、异常类型、返回形状、日志格式、错误信息，按已有的来；
- **想改变约定时**：单独提出，改全部地方，不要在新功能里夹带一种新写法，让代码库里出现两套规则；
- **先读五个相邻的方法**：它们共同的那几行，就是这里的约定。

```python
class Lists:
    def __init__(self): self._data = {1: ("ann", {"name": "周末片单"})}

    def _get(self, pid, user):                       # 已有：存在 + 所有权
        owner, data = self._data[pid]
        if owner != user: raise KeyError(pid)
        return data

    def view(self, pid, user): return self._get(pid, user)["name"]
    def rename(self, pid, user, name):               # 新增：沿用 _get，只多这几行
        self._get(pid, user)["name"] = name

l = Lists(); l.rename(1, "ann", "新名字"); print(l.view(1, "ann"))    # 新名字
try: l.rename(1, "bob", "x")
except KeyError: print("别人改不了")
```

**知识点：**最小改动（Minimal Diff）
