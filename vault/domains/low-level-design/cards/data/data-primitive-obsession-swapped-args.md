---
id: data-primitive-obsession-swapped-args
node: data.primitive-obsession
type: qa
step: 1
---
## Q
`transfer(src, dst, amount)` 的三个参数都是 `int`，调用方写成 `transfer(amount, src, dst)`，代码照样跑，钱转错了账户。这类问题叫什么，为什么类型注解 `int` 拦不住？

## A
**用 `int`、`str` 表示业务概念，编译器分不清它们**

- **原始类型偏执（primitive obsession）**：账户 id、金额、用户 id 全是 `int`，互相换位置，类型检查器和运行时都认为合法；
- **出错的特点**：不报错、跑得通、结果错；只有数据对不上账的那天才发现；
- **程序里的信号**：函数有三个以上同类型参数；字符串里藏着格式（`"2026-11-17"`、`"USD:500"`），到处有人切分；`dict` 用魔法键，`tuple` 用下标取值；
- **治法的方向**：让每个概念有自己的类型，类型不同就不能互换；
- **并非都要治**：局部一次性的值、只在一处用的 `int`，不值得包装。

```python
def transfer(src: int, dst: int, amount: int) -> str:
    return f"move {amount} from {src} to {dst}"

src, dst, amount = 7, 9, 500
print(transfer(src, dst, amount))
print(transfer(amount, src, dst))             # 跑得通：从 500 号账户转了 9
```

**知识点：**用小类型代替裸值（Primitive Obsession）
