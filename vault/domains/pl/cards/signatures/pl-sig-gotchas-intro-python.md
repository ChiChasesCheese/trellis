---
id: pl-sig-gotchas-intro-python
node: signatures.gotchas
type: qa
step: 5
---
## Q
Python 最值得认识的经典陷阱有哪些：可变默认参数、晚绑定闭包、遍历时修改列表、作用域错误？每个的真实输出和根源是什么？

## A
**1. 可变默认参数**。默认值在**函数定义时**求值一次，之后所有调用共享同一个对象：

```python
def add(x, items=[]): items.append(x); return items
print(add(1), add(2))      # [1, 2] [1, 2]
```

真实输出 `[1, 2] [1, 2]`：两次调用返回同一个列表。修法：默认值用 `None`，函数内部创建 `items = [] if items is None else items`。

**2. 闭包的晚绑定**。闭包捕获的是**变量**，不是调用时的值，等被调用时变量已是最终值：

```python
fs = [lambda: i for i in range(3)]
[f() for f in fs]          # [2, 2, 2]
fs2 = [lambda i=i: i for i in range(3)]   # [0, 1, 2]
```

真实输出 `[2, 2, 2]` 与 `[0, 1, 2]`。修法：用默认参数在定义时绑定，或 `functools.partial`。

**3. 遍历列表时修改它**：

```python
a = [1, 2, 3]
for x in a:
    if x == 1: a.remove(x)
print(a)                   # [2, 3]
```

真实输出 `[2, 3]`：删除后迭代器的位置错位，元素 2 被跳过（没有被检查）。修法：遍历副本或构造新列表。

**4. 赋值让变量变成局部**：函数里先读全局 `x`、后面又给 `x` 赋值，整个函数里 `x` 都是局部变量，读取时报 `UnboundLocalError: cannot access local variable 'x' where it is not associated with a value`（真实输出）。

**5. 数值细节**：`0.1 + 0.2 == 0.3` 为 `False`（二进制浮点）；`round(2.5)` 是 `2`、`round(3.5)` 是 `4`（四舍六入五成双）；`-7 // 2` 是 `-4`（向负无穷取整），`-7 % 2` 是 `1`，而 `int(-3.5)` 是 `-3`。

**6. `is` 与 `==`**：`is` 比较身份，小整数与短字符串的驻留会让 `is` 偶然成立。

**共同点**：都来自 Python 的动态和“一切皆对象”：默认值是对象、闭包捕获变量、迭代器依赖索引。linter（ruff 的 B006、B023 规则）能抓住其中几个。
