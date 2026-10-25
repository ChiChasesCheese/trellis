---
id: tlc-codetop-supp-9-4-followup
node: b.codetop-supp-9
type: qa
step: 4
---
## Q
**补充题 9 36进制加法**｜追问

面试官接着问：（1）推广到任意进制（2 到 36）？（2）字母可能大小写混用？（3）做乘法？（4）为什么不直接用内置转换？

## A
1. **任意进制**：把进制 `base` 当参数，字母表取 `DIGITS[:base]`，进位用 `divmod(total, base)`；每位总和最大 `2 * (base - 1) + 1 = 2 * base - 1`，进位仍只有 `0` 或 `1`。
2. **大小写混用**：在查表之前统一 `num1.lower()`、`num2.lower()`，或者让 `VALUE` 同时包含大写字母；输出统一用小写。
3. **乘法**（LC 43 的 36 进制版）：长度为 `m` 和 `n` 的两个数相乘最多 `m + n` 位；用数组 `res[i + j + 1] += a[i] * b[j]` 累加，最后从低位到高位统一进位（`carry, res[k] = divmod(res[k] + carry, 36)`），`O(m·n)`。
4. **内置转换**：`int(num, 36)` 是合法的 Python，但有两个问题——面试里通常被禁止；Python 3.11 起对非 2 的幂进制的转换有位数上限，`int("z" * 10000, 36)` 会抛 `ValueError: Exceeds the limit (4300 digits)`，要用 `sys.set_int_max_str_digits(0)` 才能放开，而且转换是平方级。

**Python 提醒**：`divmod(a, b)` 同时返回商和余数，对非负数没有歧义；对负数它是向下取整的商、余数与除数同号，这里的总和始终非负，所以安全。`str` 是不可变的，循环里 `s = c + s` 每次 `O(n)`，会让整体变成 `O(n^2)`；先放进列表再 `"".join(reversed(out))`。
