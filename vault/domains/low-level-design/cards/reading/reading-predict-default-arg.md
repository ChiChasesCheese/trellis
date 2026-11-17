---
id: reading-predict-default-arg
node: reading.predict-behaviour
type: qa
step: 2
---
## Q
一个 `add(item, bucket=[])` 函数被调用三次，每次都没传 `bucket`。第三次返回什么？默认参数藏着什么状态？

## A
**默认值在函数定义时只求值一次，之后所有调用共用同一个对象**

- **`def` 执行的那一刻创建默认列表**：它存在函数对象里（`add.__defaults__`），不是每次调用新建；
- **没传参数的调用都拿到这一个列表**：第一次放进去的东西，第二次、第三次还在；
- **推演时要把函数当成带状态的对象**：它的状态就是 `__defaults__`；
- **只有可变默认值才有问题**：`None`、数字、字符串、元组不会被原地修改；
- **标准写法**：默认 `None`，函数体里 `if bucket is None: bucket = []`。

```python
def add(item, bucket=[]):
    bucket.append(item)
    return bucket

print(add(1), add(2), add(3))   # [1, 2, 3] [1, 2, 3] [1, 2, 3]：三次返回同一个列表
print(add.__defaults__)         # ([1, 2, 3],)

def add_ok(item, bucket=None):
    if bucket is None: bucket = []
    bucket.append(item)
    return bucket
print(add_ok(1), add_ok(2))     # [1] [2]
```

<details class="pt"><summary>延伸</summary>

第一行 `print` 三个结果都显示 `[1, 2, 3]`，因为它们是同一个对象，`print` 在三次调用都结束之后才输出。

</details>

**知识点：**预测输出与副作用（Predicting Behaviour）
