---
id: data-invariants-where-check
node: data.invariants
type: qa
step: 3
---
## Q
不变量应该在构造函数、公共方法入口还是出口检查？私有辅助方法要不要检查？

## A
**构造函数建立，公共方法保持，出口检查**

- **构造函数**：建立不变量，对象一旦存在就合法，不留“先构造、再 init”的半成品；
- **公共方法**：假设入口成立，保证出口成立；检查放在出口，因为刚被改动的是这里；
- **私有辅助方法**：可以暂时破坏，由调用它的公共方法在返回前修好，所以 helper 自己不检查；
- **成本**：O(n) 的全表检查放进热路径会拖慢，开发和测试时开，生产里只留 O(1) 的安全检查（封顶、非负）；
- **被外部输入破坏的是前置条件**，归边界校验，不是不变量检查。

```python
class Pool:
    """Rep invariant: 0 <= used <= capacity."""
    def __init__(self, capacity: int):
        if type(capacity) is not int or capacity < 0:
            raise ValueError("capacity")
        self.capacity, self.used = capacity, 0          # 构造即合法
    def take(self, n: int):
        if n < 0 or n > self.capacity - self.used:
            raise ValueError("bad take")               # 状态没动
        self.used += n
        assert 0 <= self.used <= self.capacity         # 出口检查

p = Pool(3)
p.take(2)
print(p.used)
```

**知识点：**不变量与封装（Invariants）
