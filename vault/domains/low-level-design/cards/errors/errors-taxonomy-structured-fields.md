---
id: errors-taxonomy-structured-fields
node: errors.taxonomy
type: qa
step: 4
---
## Q
自定义异常带两个字段，`__init__(self, account, short)` 里调用 `super().__init__(f"{account}:{short}")` 拼成一句消息。这样写在线程池、`multiprocessing` 里会出什么问题？

## A
**`args` 要是构造参数；字段放属性，别只拼进字符串**

- **异常靠 `args` 重建**：`pickle` 用 `类(*args)` 还原；`args` 只剩拼好的一句话，还原时参数个数对不上，抛 `TypeError`，真正的错误被一个无关的错取代；
- **做法**：`super().__init__(account, short)`，把构造参数原样交给基类，文字由 `__str__` 生成；
- **字段是合同的一部分**：调用方读 `e.short` 决定补多少，不解析消息；
- **消息只给人看**：改措辞不能让任何调用方坏掉；
- **跨进程、队列、`concurrent.futures` 的进程池都会 pickle 异常**，自定义异常第一次被远端抛出来时才发现问题，已经晚了。

```python
import pickle

class Insufficient(Exception):
    def __init__(self, account: str, short: int):
        super().__init__(account, short)          # args 就是构造参数
        self.account, self.short = account, short

    def __str__(self) -> str:
        return f"{self.account} 差 {self.short}"

e = pickle.loads(pickle.dumps(Insufficient("a1", 30)))
print(e, e.short, e.args)                         # a1 差 30 30 ('a1', 30)
```

**知识点：**错误类型体系（Error Taxonomy）
