---
id: cc-rules-money-negative-formatting
node: rules.money
type: qa
---
## Q
Render `-350` cents as `x.xx`. Why does `f"{c // 100}.{abs(c) % 100:02d}"` produce `-4.50`?

## A
**Because `//` floors toward minus infinity: `-350 // 100` is `-4`, not `-3`.**

Format the magnitude and attach the sign separately:

```python
sign = "-" if c < 0 else ""
a = abs(c)
s = f"{sign}{a // 100}.{a % 100:02d}"        # -3.50
```

Two more failures in the same line: `-3.5` where the spec demands two decimals (`{a % 100:02d}` fixes it), and a value of `-50` printing as `-0.50`, which is correct and must not be "tidied" to `-.50` or `0.50`. Render in one place and unit-test it on `0`, `5`, `-5`, `-100` and `-350`.

## Q zh
把 `-350` 分渲染成 `x.xx`。为什么 `f"{c // 100}.{abs(c) % 100:02d}"` 会得到 `-4.50`？

## A zh
**因为 `//` 向负无穷取整：`-350 // 100` 是 `-4`，不是 `-3`。**

对绝对值做格式化，符号单独接上：

```python
sign = "-" if c < 0 else ""
a = abs(c)
s = f"{sign}{a // 100}.{a % 100:02d}"        # -3.50
```

同一行里还有两个失败：题面要求两位小数却打出 `-3.5`（用 `{a % 100:02d}` 修好）；以及 `-50` 会打成 `-0.50`，这是正确的，不要"整理"成 `-.50` 或 `0.50`。只在一处渲染，并对 `0`、`5`、`-5`、`-100`、`-350` 做单元测试。
