---
id: fluency-mutability-default-argument
node: fluency.mutability
type: qa
step: 2
---
## Q
`def add(item, bucket=[])` 连续调用两次，第二次的结果里为什么带着第一次的元素？同样的问题还会出现在构造函数的什么位置，怎么写才安全？

## A
**默认值只在 def 时求值一次，所有调用共享**

- **机制**：默认参数在函数定义那一刻求值，结果存进 `add.__defaults__`；每次不传参数的调用拿到的是同一个列表；
- **后果**：服务实例之间、请求之间互相污染，测试单独跑能过，整套一起跑才挂，因为状态是跨调用残留的；
- **惯用修法**：默认写 `None`，函数里 `if bucket is None: bucket = []`；用 `None` 而不是 `if not bucket`，因为调用方可能故意传了空列表，希望往里面添加；
- **构造函数的同类坑**：`def __init__(self, seen=[])` 把同一个列表挂到所有实例上；需要初始状态时先拷贝，`self.seen = [] if seen is None else list(seen)`，而不是直接保存传入的对象；
- **不可变默认值没问题**：`0`、`""`、`None`、`()`、`frozenset()`；
- **dataclass 里的对应写法**：`field(default_factory=list)`，写 `items: list = []` 会直接报错。

```python
def add(item, bucket=[]):            # 错：默认列表只建一次
    bucket.append(item)
    return bucket

print(add(1), add(2), add.__defaults__)    # [1, 2] [1, 2] ([1, 2],)

def add_ok(item, bucket=None):
    if bucket is None:
        bucket = []                  # 每次调用新建
    bucket.append(item)
    return bucket

print(add_ok(1), add_ok(2))          # [1] [2]
```

**知识点：**可变性与别名（Mutability & Aliasing）
