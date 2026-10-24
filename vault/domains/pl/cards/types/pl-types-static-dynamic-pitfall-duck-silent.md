---
id: pl-types-static-dynamic-pitfall-duck-silent
node: types.static-dynamic
type: qa
step: 6
---
## Q
动态类型最危险的不是报 `TypeError`，而是什么？请用 Python 的 `x + x` 举例。

## A
最危险的是类型错了却不报错，程序悄悄做了另一件事。

```python
def double(x):
    return x + x

print(double(21), double("21"), double([1]))
```

实际输出：`42 2121 [1, 1]`。

函数的本意是「把数字翻倍」。传进整数 `21` 得到 `42`，对；但传进字符串 `"21"`（比如从表单或 CSV 读出来忘了转换），`+` 变成字符串拼接，得到 `"2121"`，没有任何报错；传进列表又变成列表拼接。因为 Python 只要对象支持 `+` 就接受（鸭子类型），所以类型对不对完全由调用方保证。这种 bug 往往在几个函数之后、结果被存进数据库时才暴露。

静态类型语言里，`double(x int) int` 只接受整数，`double("21")` 无法编译。对应的补救办法在 Python 里是类型提示加外部检查器（`def double(x: int) -> int` 再用 `mypy`），或者在入口处显式转换和校验（`int(x)`）。没有这两样，动态类型语言的类型错误可以一路传播很远。
