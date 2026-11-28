---
id: py-out-identity-small-int
node: output.identity
type: qa
step: 1
---
## Q
**is 与小整数缓存**｜读代码说输出

```python
a = int("256"); b = int("256")
c = int("257"); d = int("257")
print(a is b, c is d, c == d)
x = 257; y = 257
print(x is y)
```

输出什么？

## A
**输出。**

```
True False True
True
```

**为什么。**

- CPython 预先创建了 -5 到 256 的整数对象，`int("256")` 每次返回同一个对象，所以 `a is b` 为 True；257 超出范围，每次新建对象。
- `==` 比较值，`c == d` 为 True；`is` 比较身份（是不是同一个对象）。
- `x = 257; y = 257` 在同一段代码里，编译器把相同的常量合成一个对象，所以 `is` 为 True。这是脚本里的结果，换成交互式一行一编译就不同。

**语言为什么这样设计。**

- 小整数缓存是 CPython 的实现细节，语言只保证 `is` 比较身份；缓存只是为了少分配常用的小对象。
- Java 的 `Integer` 缓存 -128 到 127，`==` 比较装箱对象同样踩坑；Python 的做法是约定俗成：值用 `==`，`is` 只留给 `None` 和哨兵对象。

**怎么写才对。**

```python
if x == 257: ...
if y is None: ...
```

**面试里一句话。**

The is operator tests object identity, and small-integer caching is a CPython implementation detail, so compare values with == and reserve is for None.
