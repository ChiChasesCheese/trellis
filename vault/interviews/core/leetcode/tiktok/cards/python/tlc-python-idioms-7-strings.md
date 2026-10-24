---
id: tlc-python-idioms-7-strings
node: python.idioms
type: qa
step: 7
---
## Q
**Python 工具箱｜字符串的常用写法**

拼接大量字符串、字符与编号互转、判断字符类别分别用什么？为什么 `s += c` 在循环里要避免？

## A
字符串不可变，`s += c` 每次可能新建一个字符串，循环里累计 `O(n^2)`（CPython 有就地扩展的优化，但不应依赖）。收集到列表，最后 `"".join` 一次，`O(n)`。

```python
print(" ".join(["a", "b"]), ",".join(map(str, [1, 2])))   # a b 1,2：join 要求元素都是 str
print(ord("a"), chr(97 + 2), ord("c") - ord("a"))          # 97 c 2：字母映射到 0..25
print("abc".startswith(("x", "a")))                        # True：可传元组，任一前缀匹配
```

- 字母下标：`ord(c) - ord('a')`，开 26 长度数组替代字典，常数更小（LC 242、438、49 的计数签名）。
- 判断类别：`c.isalpha()`、`c.isdigit()`、`c.isalnum()`、`c.isspace()`；LC 125、227 用得到。
- 分割：`s.split()` 不带参数时按任意空白切分并丢掉空串，`s.split(" ")` 则保留空串（LC 151、165 的差别）。
- 查找：`s.find(t)` 找不到返回 `-1`，`s.index(t)` 找不到抛 `ValueError`；`in` 只判断存在。
- 数字转字符串 `str(n)`、`int(s)`；`int(s, 2)` 按二进制解析；`bin(n)[2:]` 去掉 `0b` 前缀；`format(n, "b")` 同样得到二进制。
- 面试写加法 / 乘法类题（LC 43、415、67）时，不要用 `int(a) + int(b)` 偷懒，题目就是要你模拟逐位运算。
- **坑**：`str` 没有 `.reverse()`；`sorted("cba")` 返回的是**列表**，不是字符串，要 `"".join(sorted(s))`。
