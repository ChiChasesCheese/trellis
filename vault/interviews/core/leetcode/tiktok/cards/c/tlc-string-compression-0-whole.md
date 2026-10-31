---
id: tlc-string-compression-0-whole
node: c.string-compression
type: qa
---
## Q
**LC 443 压缩字符串**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 11 次 · 最近 2024-05-12（国内 CodeTop）

给定字符数组 `chars`，按连续重复字符分组压缩：组长为 1 只写字符，否则写字符再写组长（组长 `>= 10` 要拆成多个字符）。结果必须原地写回 `chars`，返回新长度，只能用常量额外空间；超出返回长度的内容无关紧要。`1 <= chars.length <= 2000`，`chars[i]` 是小写字母、大写字母、数字或符号。例：`["a","a","b","b","c","c","c"]` → `6`，前 6 个字符为 `a2b2c3`；`["a"]` → `1`；`["a","b","b",…共 12 个 b]` → `4`，前 4 个字符为 `ab12`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 读指针找出每个连续组，写指针紧跟其后把「字符 + 组长的各位数字」写回同一个数组，写指针永远不超过读指针。

**识别。** 「原地」「常量空间」「连续重复」三个信号合起来就是读写双指针；结果不会比原串长，所以覆盖是安全的。

**推导。** 暴力：用 `groupby` 生成新字符串再拷回，额外空间 `O(n)`，违反题目要求。洞察：组长为 `k >= 2` 时写入长度是 `1 + len(str(k)) <= k`，写位置不会追上还没读的位置，所以直接在原数组上覆盖。

**简单解法。** 用 `groupby` 分组、拼出压缩串，再整体赋值回 `chars`。

```python
from itertools import groupby


def compress_extra_space(chars: list[str]) -> int:
    parts: list[str] = []
    for ch, group in groupby(chars):             # 连续相同字符分组
        size = len(list(group))
        parts.append(ch if size == 1 else f"{ch}{size}")
    compressed = "".join(parts)
    chars[: len(compressed)] = compressed        # 覆盖回原数组前缀（长度不会超过原长）
    return len(compressed)
```

`O(n)` 时间但 `O(n)` 额外空间，不满足常量空间要求。

最优解：

```python
def compress(chars: list[str]) -> int:
    write = read = 0                             # write 之前是已压缩的结果，read 扫描原数组
    while read < len(chars):
        ch, start = chars[read], read
        while read < len(chars) and chars[read] == ch:   # 吃掉整个连续组
            read += 1
        chars[write] = ch
        write += 1
        if (count := read - start) > 1:          # 只有长度 >1 才写数字，且逐位写（12 -> '1','2'）
            for digit in str(count):
                chars[write] = digit
                write += 1
    return write                                 # write <= read 恒成立，不会覆盖未读内容
```

运行：`"aabbccc"` → `6`（`a2b2c3`）；`"a"` → `1`；`"a" + "b" * 12` → `4`（`ab12`）；`"a" * 100` → `4`（`a100`）；`"abc"` → `3`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`（`str(count)` 至多 4 个字符）。

**拓展优化。**
- 同时要求「压缩后更长则保持原样」（面试常见变体）：先算压缩长度，大于等于原长就不写。
- 解压缩（`LC 394` 类）：反向读，注意多位数字拼成整数。

**易错点。**
- 把 `12` 当一个字符写入：数组元素只能是单个字符，必须 `for digit in str(count)` 逐位写。
- 组长为 1 时也写 `1`：`["a"]` 应得到 `a`，而不是 `a1`。
- 循环结束后忘记处理最后一组：把「找组」写成内层 `while` 就不会漏。

**追问。**
- 为什么写指针不会覆盖未读内容：组长 `k = 2` 时写 2 个字符等于读了 2 个，之后 `k` 越大写入增长越慢。
- 字符集是 Unicode 或字节流：逻辑不变，比较的是元素相等。

**同模式。** LC 27 移除元素、LC 26 删除有序数组中的重复项、LC 283 移动零、LC 38 外观数列、LC 394 字符串解码。
