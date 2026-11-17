---
id: fluency-mutability-class-attribute
node: fluency.mutability
type: qa
step: 3
---
## Q
`class Log: seen = []` 里 `self.seen.append(x)`，两个实例的 `seen` 为什么是同一个列表？而 `class Cnt: n = 0` 里 `self.n += 1` 为什么两个实例互不影响？状态应该放在哪里？

## A
**状态放在 `__init__` 里的 self 上**

- **属性查找顺序**：先找实例，再找类；类里的 `seen = []` 只有一个列表，所有实例读到的都是它；
- **`append` 是改对象，不是改属性**：不会给实例新增 `seen`，改的是类上那个列表，所有实例都看到；
- **`self.n += 1` 展开成 `self.n = self.n + 1`**：读到类属性 0，把结果 1 写成实例属性，类上的 `n` 不变，所以两个实例互不影响；同样的写法碰到列表，`self.seen += [x]` 先原地改了共享列表，再把它写回实例，仍然改了类上的列表；
- **规则**：可变的状态在 `__init__` 里创建，`self.seen = []`；类属性只放常量和配置；
- **模块级缓存同理**：模块里的 `_cache = {}` 在整个进程里只有一份，两个服务实例会互相看到；需要隔离就让它属于实例。

```python
class Bad:
    seen = []                          # 类属性：只有一份
    def log(self, x):
        self.seen.append(x)

class Good:
    def __init__(self):
        self.seen = []                 # 每个实例一份
    def log(self, x):
        self.seen.append(x)

b1, b2 = Bad(), Bad(); b1.log(1)
g1, g2 = Good(), Good(); g1.log(1)
print(b2.seen, g2.seen, "seen" in vars(b1))   # [1] [] False
```

**知识点：**可变性与别名（Mutability & Aliasing）
