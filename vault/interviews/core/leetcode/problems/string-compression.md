---
slug: string-compression
---
## Q
**LC 443 压缩字符串**｜Medium

把字符数组 `chars` 原地压缩：每组连续重复字符写成「字符 + 组长」，组长为 `1` 不写数字，组长 `≥ 10` 拆成多个字符。返回新长度，只能用常量额外空间。

## A
**一句话。** 双指针：`read` 数每组长度，`write` 在同一数组里写字符和组长，写指针不会超过读指针。

```python
def compress(chars):
    write = read = 0
    while read < len(chars):
        ch, start = chars[read], read
        while read < len(chars) and chars[read] == ch:
            read += 1                    # 数出这组的长度
        chars[write] = ch
        write += 1
        if read - start > 1:             # 组长 1 不写数字
            for d in str(read - start):  # 12 拆成 '1'、'2'
                chars[write] = d
                write += 1
    return write
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 组长 `12` 当一个元素写入：每格只能放一个字符，要拆成 `'1'`、`'2'`。
- 组长为 `1` 也写数字：`["a"]` 应压成 `["a"]`，不是 `["a","1"]`。
- 内层 `while` 漏掉 `read < len(chars)`：最后一组越界。

**追问。**
- 反过来解压？：展开会变长，先算总长再从后往前写；或直接用新列表。
- 不要求常量空间？：`groupby(chars)` 逐组取字符和长度，代码最短。

**同模式。** LC 283 移动零、LC 27 移除元素、LC 26 删除有序数组中的重复项、LC 38 外观数列
