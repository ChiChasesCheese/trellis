---
id: py-out-numbers-floor-div-mod
node: output.numbers
type: qa
step: 1
---
## Q
**负数的整除与取模**｜读代码说输出

```python
print(-7 // 2, -7 % 2)
print(7 // -2, 7 % -2)
print(int(-3.5), -7 // 2 * 2 + -7 % 2)
```

输出什么？

## A
**输出。**
```
-4 1
-4 -1
-3 -7
```

**为什么。**
- `//` 是向下取整除法（floor division）：-3.5 向下取整得 -4，不是 -3。
- `%` 的结果跟除数同号：-7 % 2 = 1，7 % -2 = -1。
- 恒等式 `a == (a // b) * b + a % b` 始终成立，第三行 -4*2 + 1 = -7 就是它。
- `int()` 是截断（向 0 取整），所以 int(-3.5) 是 -3，和 `//` 不同。

**语言为什么这样设计。**
- Python 选 floor：保证 `a % b` 落在 [0, b)（b 为正），用来做环形下标、哈希桶、星期几都不会出现负数。
- C、Java、Go 选截断：直接对应 CPU 的除法指令，-7 % 2 得 -1；Python 选了数学上一致的语义，牺牲一点与硬件的对应。

**怎么写才对。**
```python
q, r = divmod(-7, 2)   # (-4, 1)；要截断语义用 math.fmod 或 int(a / b)
```

**面试里一句话。**
Python's `//` floors toward negative infinity and `%` takes the sign of the divisor, so `a == (a // b) * b + a % b` always holds, unlike C and Java which truncate.
