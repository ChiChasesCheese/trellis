---
id: py-out-numbers-string-slice
node: output.numbers
type: qa
step: 4
---
## Q
**字符串的切片与不可变**｜读代码说输出

```python
s = "hello"
print(s[1:10], s[::-1], s[-3:-1])
t = s.upper()
print(s, t)
try:
    s[0] = "H"
except TypeError as e:
    print(type(e).__name__)
try:
    s[10]
except IndexError as e:
    print(type(e).__name__)
```

输出什么？

## A
**输出。**
```
ello olleh ll
hello HELLO
TypeError
IndexError
```

**为什么。**
- 切片（slice）越界不报错，只是被截到边界：`s[1:10]` 等于 `s[1:]`；单个下标越界才抛 IndexError。
- `s[::-1]` 步长为 -1，整串倒过来；`s[-3:-1]` 取倒数第 3 到倒数第 2 个字符，右端不含。
- 字符串不可变（immutable）：`upper()` 返回新字符串，`s` 不变；`s[0] = "H"` 直接 TypeError。

**语言为什么这样设计。**
- 不可变让字符串可以做字典键、可以安全共享和驻留（interning），哈希值也能缓存；Java、Go、JavaScript 的字符串同样不可变。
- 切片宽松是因为区间 `[start, stop)` 取交集有意义，空串是合理结果；单下标没有合理的“空”结果，所以报错。C++ 的 `std::string` 可变，`substr` 越界则抛异常。

**怎么写才对。**
```python
s = "H" + s[1:]                 # 改一个字符：造新串；大量拼接用 "".join(parts)
```

**面试里一句话。**
Python strings are immutable and slicing clamps out-of-range bounds, so only a single bad index raises.
