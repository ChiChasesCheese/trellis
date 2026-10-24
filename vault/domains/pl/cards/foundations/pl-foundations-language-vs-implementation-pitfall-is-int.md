---
id: pl-foundations-language-vs-implementation-pitfall-is-int
node: foundations.language-vs-implementation
type: qa
step: 6
---
## Q
为什么在 CPython 里 `int("256") is int("256")` 是 `True`，而 `int("257") is int("257")` 是 `False`？这个结果能依赖吗？

## A
`is` 比较的是对象身份（是不是内存里同一个对象），`==` 比较的才是值。CPython 为了省内存和时间，把 -5 到 256 之间的小整数预先创建好并复用，所以任何地方得到的 256 都是同一个对象；257 超出了缓存范围，每次计算会新建一个对象。

```python
a, b = int("256"), int("256")
c, d = int("257"), int("257")
print(a is b, c is d, c == d)
```

实际输出：`True False True`。

不能依赖这个结果：缓存范围是 CPython 的实现细节，语言规范只说「小整数对象可能被复用」；换到 PyPy，或者编译器常量折叠后在同一个模块里写两个 `257`，结果都可能不同。判断值相等永远用 `==`，`is` 只用在 `x is None` 这类判断单例的场合。

Java 里有一模一样的陷阱：`Integer` 缓存 -128 到 127，所以 `Integer a = 127, b = 127; a == b` 为真，而 128 为假。两门语言各自选了一个缓存范围，原因相同：自动装箱的小对象太常用了。
