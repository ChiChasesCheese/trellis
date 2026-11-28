---
id: py-out-mutation-default-arg
node: output.mutation
type: qa
step: 1
---
## Q
**默认参数**｜读代码说输出

```python
def add(x, acc=[]):
    acc.append(x)
    return acc
print(add(1))
print(add(2))
print(add(3, []))
print(add(4))
print(add.__defaults__)
```

输出什么？

## A
**输出。**

```
[1]
[1, 2]
[3]
[1, 2, 4]
([1, 2, 4],)
```

**为什么。**

- `def` 是一条可执行语句：执行到它时，默认值 `[]` 只求值一次，创建的列表存进函数对象的 `__defaults__`。
- 不传 `acc` 的调用都用这同一个列表，所以前两次、第四次累积到一起。
- 第三次自己传了新列表，改的是那个列表，默认列表不受影响。

**语言为什么这样设计。**

- 默认值只求值一次省掉每次调用的求值开销，也让 `def` 与普通语句的语义统一；代价是默认值若可变就会被所有调用共享。
- JavaScript 和 Ruby 在每次调用时才求值默认表达式，所以没有这个坑；Python 官方 FAQ 把它列为常见陷阱。

**怎么写才对。**

```python
def add(x, acc=None):
    if acc is None:
        acc = []
    acc.append(x)
    return acc
```

**面试里一句话。**

Default argument values are evaluated once at function definition, so a mutable default is shared across calls; use None as a sentinel.
