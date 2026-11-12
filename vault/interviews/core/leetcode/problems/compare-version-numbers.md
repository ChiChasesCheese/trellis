---
slug: compare-version-numbers
---
## Q
**LC 165 比较版本号**｜Medium

比较两个以 `.` 分隔修订号的版本号，缺失的修订号视为 `0`，前导零忽略；返回 `-1`、`0` 或 `1`。

## A
**一句话。** 按 `.` 切开，`zip_longest` 补 `"0"`，逐段转 `int` 比较，第一个不同的决定结果。

```python
def compare_version(version1, version2):
    v1, v2 = version1.split("."), version2.split(".")
    for a, b in zip_longest(v1, v2, fillvalue="0"):
        x, y = int(a), int(b)       # int 去掉前导零
        if x != y:
            return -1 if x < y else 1
    return 0
```

**复杂度。** 时间 `O(m + n)`，空间 `O(m + n)`。

**易错点。**
- 直接比字符串：`"1.2"` 与 `"1.10"` 得 `1`，应为 `-1`。
- 用 `zip` 丢掉多出的修订号：`("1.0.1", "1")` 得 `0`，应为 `1`。
- 返回 `x - y`：只要 `-1/0/1`，`("1.2", "1.10")` 会得 `-8`。

**追问。**
- 想省掉 `split` 的列表？：两个指针直接在字符串上边读边累加，`O(1)` 空间。
- 修订号超出 32 位？：Python 不用管；其他语言去掉前导零后先比长度再比字典序。

**同模式。** LC 179 最大数、LC 93 复原 IP 地址、LC 468 验证 IP 地址、LC 8 字符串转换整数
