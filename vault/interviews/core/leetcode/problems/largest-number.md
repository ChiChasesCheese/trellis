---
slug: largest-number
---
## Q
**LC 179 最大数**｜Medium

把一组非负整数重新排列并拼接，使结果最大，返回字符串。

## A
**一句话。** 自定义排序：比较 `a+b` 与 `b+a`，拼起来大的排前面；全是 `0` 特判成 `"0"`。

```python
def largest_number(nums):
    def compare(a, b):            # a+b 更大则 a 排前，返回负数
        return (b + a > a + b) - (b + a < a + b)

    strs = sorted(map(str, nums), key=cmp_to_key(compare))
    return "0" if strs[0] == "0" else "".join(strs)
```

**复杂度。** 时间 `O(n log n · L)`，空间 `O(nL)`。

**易错点。**
- 按字典序降序排：`[3,30]` 得 `"303"`，应为 `"330"`。
- 全零不特判：`[0,0]` 拼出 `"00"`，应为 `"0"`。
- 比较器返回布尔值：`cmp_to_key` 要负 / 零 / 正的整数。

**追问。**
- 不用比较器怎么写？：每个数至多 `10` 位，按 `s * 10` 字典序降序排，同样正确。
- 要最小的拼接数？：比较方向反过来，注意前导零的题意。

**同模式。** LC 56 合并区间、LC 406 根据身高重建队列、LC 253 会议室 II、LC 937 重新排列日志文件
