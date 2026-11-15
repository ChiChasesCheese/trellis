---
slug: xor-queries-of-a-subarray
---
## Q
**LC 1310 子数组异或查询**｜Medium

正整数数组 `arr` 和若干查询 `[l, r]`，每个查询求 `arr[l] ^ arr[l+1] ^ ... ^ arr[r]`。返回所有查询的答案。

## A
**一句话。** 前缀异或：`pre[i]` 是前 `i` 个数的异或，异或自己抵消自己，所以 `[l, r]` 的结果是 `pre[r+1] ^ pre[l]`，每个查询 `O(1)`。

```python
def xor_queries(arr, queries):
    pre = [0]
    for x in arr:
        pre.append(pre[-1] ^ x)    # pre[i] = arr[0..i-1] 的异或
    return [pre[r + 1] ^ pre[l]
            for l, r in queries]
```

**复杂度。** 时间 `O(n + q)`，空间 `O(n)`。

**易错点。**
- 用 `pre[r] ^ pre[l-1]`：`l = 0` 时下标越界；前缀数组从 `pre[0] = 0` 开始，统一写 `pre[r+1] ^ pre[l]`。
- 以为要线段树：数组不修改，前缀异或就够了。

**追问。**
- 为什么异或能像求和那样做差？：`a ^ a = 0`，`pre[r+1] = pre[l] ^ (区间异或)`，两边再异或 `pre[l]` 即得区间。
- 数组会修改呢？：改用树状数组，单点修改与前缀异或都是 `O(log n)`。

**同模式。** LC 303 区域和检索 - 数组不可变、LC 560 和为 K 的子数组、LC 1442 形成两个异或相等数组的三元组数目、LC 1915 最美子字符串的数目
