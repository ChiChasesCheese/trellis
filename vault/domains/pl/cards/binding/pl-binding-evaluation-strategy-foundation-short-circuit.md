---
id: pl-binding-evaluation-strategy-foundation-short-circuit
node: binding.evaluation-strategy
type: qa
step: 2
---
## Q
短路求值（short-circuit evaluation）是什么？为什么 `a && b` 不能当成普通函数 `and(a, b)` 来实现？

## A
**短路**指逻辑运算符在结果已经确定时，不再计算右边：`false && x` 已经是 `false`，`true || x` 已经是 `true`，所以 `x` 不会被求值。`?:`（三元表达式）也一样：只算被选中的那个分支。

这是严格求值语言里**唯一的内建惰性**，它不是优化，而是语义的一部分，程序依赖它写出惯用法：Java 的 `if (p != null && p.ready())` 在 `p` 为空时不会调用 `p.ready()`；Python 的 `x = cache or compute()` 只在 `cache` 为假时才调用 `compute()`。

为什么不能写成函数：函数调用先求值所有参数，再进入函数，右操作数早已被算过了。

```python
def my_and(a, b): return a and b
def boom(): print("boom evaluated"); return True
print(my_and(False, boom()))   # boom evaluated, then False
print(False and boom())        # False  (boom never runs)
```

第一行输出 `boom evaluated` 然后 `False`；第二行只输出 `False`。所以 `&&`、`||` 必须是编译器特殊对待的**语法**，不是函数；`if`、`while`、`match` 也是同理。

Python 的 `and`/`or` 还有一个区别于 Java 的细节：它们返回**决定结果的那个操作数**，而不是布尔值：`[] or "default"` 得到 `"default"`，`0 and 5` 得到 `0`，`"a" and "b"` 得到 `"b"`。这让 `x or default` 成为常见的取默认值写法，但也要小心，`0`、`""`、`[]` 这些「假值」也会触发 `or`（取默认值时把合法的 `0` 当成了缺失）。

C++ 的内建 `&&`、`||` 同样短路，但它们可以被重载，重载后就变成普通函数调用，两边都先求值，短路消失：
```cpp
struct B { bool v; };
bool operator&&(B a, B b) { return a.v && b.v; }
B boom() { std::println("boom evaluated"); return {true}; }
// B{false} && boom()   -> prints "boom evaluated", then false
```
本机实际输出 `boom evaluated`，然后 `false`。所以 C++ 的最佳实践是永远不要重载 `&&`、`||`。
Rust 的 `&&`、`||` 同样短路，只作用于 `bool`；Java 另有不短路的 `&`、`|`，两边都会计算，一般只在刻意需要副作用时使用。
