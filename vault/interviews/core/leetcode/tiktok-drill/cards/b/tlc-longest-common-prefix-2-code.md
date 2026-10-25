---
id: tlc-longest-common-prefix-2-code
node: b.longest-common-prefix
type: qa
step: 2
---
## Q
**LC 14 最长公共前缀**｜写出 Python 实现

字符串数组 `strs`（`1..200` 个，每个长度 `0..200`，非空时仅小写字母）。返回所有字符串的最长公共前缀，不存在则返回 `""`。

## A
**思路。** `zip(*strs)` 依次产出每一列（所有字符串的第 `j` 个字符组成的元组），在最短串耗尽时自动停止。若这一列只有一种字符，前缀长度加一；否则立即结束。最后从 `strs[0]` 里切出这么长的前缀。

```python
def longest_common_prefix(strs: list[str]) -> str:
    size = 0
    for column in zip(*strs):                    # 按列扫：第 j 列是所有字符串的第 j 个字符；zip 在最短串处自动停
        if len(set(column)) != 1:                # 这一列有不同字符：前缀到此为止
            break
        size += 1
    return strs[0][:size]
```

**运行。** `["flower","flow","flight"]` → `"fl"`；`["dog","racecar","car"]` → `""`；`["a"]` → `"a"`；`[""]` → `""`；`["ab","","abc"]` → `""`；`["abc","abc"]` → `"abc"`。

**复杂度。** 时间 `O(S)`，`S` 为所有字符总数，遇到第一列不齐立即停止；空间 `O(n)`，每列的 `set` 至多 `n` 项。

**写法要点。** `zip(*strs)` 用星号解包把列表展开成多个位置参数，等价于转置；`set(column)` 去重后长度为 `1` 就说明全相同；`strs[0][:size]` 只在最后切片一次，不在循环里拼接字符串；`for … break` 不需要 `else`，因为 `size` 本身记录了通过的列数；空串会让 `zip` 立刻结束，不必特判。
