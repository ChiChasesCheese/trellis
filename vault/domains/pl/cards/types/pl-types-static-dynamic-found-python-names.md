---
id: pl-types-static-dynamic-found-python-names
node: types.static-dynamic
type: qa
step: 2
---
## Q
Python 里变量到底是什么？「变量没有类型，值有类型」是什么意思？

## A
Python 的变量只是名字（name），是贴在对象上的标签。赋值 `x = 1` 的意思是：创建（或找到）一个整数对象 `1`，让名字 `x` 指向它。对象带着自己的类型；名字没有类型，下一行可以让它指向别的对象。

```python
x = 1
print(type(x).__name__)    # int
x = "a"                    # 同一个名字，现在指向字符串
print(type(x).__name__, isinstance(x, str))   # str True
y = x
print(x is y)              # True：两个名字指向同一个对象
```

实际输出：`int`，然后 `str True`，最后 `True`。

三个后果。第一，类型检查只能发生在「对对象做操作」的时刻：`x + 1` 执行时才去问 `x` 当前指向的对象支不支持加整数。第二，赋值不复制对象，只是多贴一个标签，`y = x` 后两个名字共享同一个对象，修改可变对象（列表、字典）会被两个名字同时看到。第三，所谓「鸭子类型」（duck typing）就是这个模型的自然结果：函数不声明参数的类型，只要传进来的对象支持函数里用到的操作就行，「走起来像鸭子，就当作鸭子」。
