---
id: pl-errors-models-foundation-exceptions
node: errors.models
type: qa
step: 2
---
## Q
异常（exception）的 `throw`、`try`、`catch` 是什么？一次抛出会让程序发生什么？

## A
异常是一种“非局部跳转”的错误传播机制：
- `throw`（Python 里是 `raise`）：在发现错误的地方抛出一个异常对象，当前函数立刻停止执行。
- `try ... catch`（Python 里是 `try ... except`）：包住可能失败的代码，并指明“如果抛出了某种异常，由这里处理”。
- 异常**不是返回值**：它沿着调用栈自动向上寻找最近的、类型匹配的 `catch`，中间经过的函数不用写任何代码。找不到就一直到线程顶层，程序终止并打印栈追踪。

```python
def parse(s): return int(s)          # raises ValueError for "12x"
try:
    n = parse("12x")
except ValueError as e:
    print("bad:", e)                 # bad: invalid literal for int() ... '12x'
```

`parse` 里没有任何错误处理代码，错误直接跳到了调用者的 `except`。Java 的写法等价：`try { Integer.parseInt("12x"); } catch (NumberFormatException e) { ... }`；C++ 写作 `try { std::stoi(s); } catch (const std::invalid_argument& e) { ... }`，可以抛出任何类型的值，惯例是继承 `std::exception`。

栈追踪（stack trace）是异常对象创建时记录的调用路径（哪个文件、哪一行调用了哪个函数），是调试的主要依据。

要记住的一个事实：异常让“正常路径”和“错误路径”分开写，代价是错误路径隐藏在控制流里，读一个调用你看不出它会不会跳走。
