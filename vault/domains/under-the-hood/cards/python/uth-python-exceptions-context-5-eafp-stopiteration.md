---
id: uth-python-exceptions-context-5-eafp-stopiteration
node: python.exceptions-context
type: qa
step: 5
---
## Q
**for 循环怎么知道到头了**｜Python · CPython 3.14

`for x in it:` 从不先问「还有没有下一个」，它怎么知道什么时候停？

## A
**背景。** 读字典有两种写法：先问再做（LBYL，Look Before You Leap）`if k in d: v = d[k]`，或直接做、失败再处理（EAFP，Easier to Ask Forgiveness than Permission）`try: v = d[k]`。先问要查两遍；多线程下，问完到动手之间，键可能已被别的线程删掉。

**结构。** 迭代器协议（iterator protocol）是 EAFP 的典型：迭代器只有一个 `__next__()`，取完了就抛 `StopIteration`。`for` 循环就是不停调用它，把 `StopIteration` 当作正常结束：

```python
it = iter(xs)
while True:
    try: x = next(it)
    except StopIteration: break
    ...   # 循环体
```

**细节。**

- 迭代器抛过一次 `StopIteration` 之后，再调用必须继续抛，否则算坏迭代器。
- `list` 的迭代器是 C 写的，取完时只返回空指针，`for` 对应的 `FOR_ITER` 指令（3.14）直接结束循环，不创建异常对象；自己写的 `__next__` 才真的抛 `StopIteration`。

**坑。** 生成器里漏出来的 `StopIteration` 会被改成 `RuntimeError`（3.7 起，PEP 479）。

**例题：** LC 341 展平嵌套列表迭代器

给嵌套整数列表 `nestedList`（元素是整数或列表），实现迭代器：`next()` 返回下一个整数，`hasNext()` 判断是否还有。例：`[[1,1],2,[1,1]]` 依次得到 `1,1,2,1,1`。

```python
class NestedIterator:
    def __init__(self, nested_list):
        self.stack = list(reversed(nested_list))      # top of stack = next item to look at

    def has_next(self):
        while self.stack:                             # unwrap lists lazily until an integer is on top
            top = self.stack[-1]
            if top.isInteger():
                return True
            self.stack.pop()
            self.stack.extend(reversed(top.getList()))
        return False

    def next(self):
        if not self.has_next():                       # next() must be safe without a prior has_next()
            raise StopIteration
        return self.stack.pop().getInteger()
```
