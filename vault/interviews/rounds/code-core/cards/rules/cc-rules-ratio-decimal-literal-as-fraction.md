---
id: cc-rules-ratio-decimal-literal-as-fraction
node: rules.exact-ratio
type: qa
---
## Q
A threshold arrives as the string `0.34`. Turn it into something you can compare exactly, and say what `1/3` does against it.

## A
**Store it as numerator over a power of ten, taken from the digit count.**

```python
whole, frac = tok.split(".")
num, den = int(whole + frac), 10 ** len(frac)   # "0.34" -> 34/100
```

Then `1/3 >= 34/100` is `100 >= 102` → **False**, while `1/3 >= 33/100` is `100 >= 99` → **True**. Both are decided exactly, with no epsilon.

`float("0.34")` is not 34/100 — it is a nearby binary value, and which side of it `1/3` falls on is an accident of representation. Since the threshold is *given* as a decimal literal, keeping it as one is both exact and faithful to the statement.

## Q zh
阈值以字符串 `0.34` 到达。把它变成能精确比较的东西，并说出 `1/3` 与它比较的结果。

## A zh
**按小数位数把它存成"分子 / 10 的幂"。**

```python
whole, frac = tok.split(".")
num, den = int(whole + frac), 10 ** len(frac)   # "0.34" -> 34/100
```

于是 `1/3 >= 34/100` 变成 `100 >= 102` → **False**；而 `1/3 >= 33/100` 变成 `100 >= 99` → **True**。两者都被精确判定，不需要 epsilon。

`float("0.34")` 不是 34/100 —— 它是附近的一个二进制值，`1/3` 落在它哪一侧纯属表示上的偶然。既然阈值本来就是以十进制字面量**给出**的，把它保持为字面量既精确又忠于题面。
