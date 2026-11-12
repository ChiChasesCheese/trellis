---
slug: rotate-string
---
## Q
**LC 796 旋转字符串**｜Easy

一次旋转是把 `s` 最左字符移到最右。判断 `s` 经若干次旋转能否变成 `goal`。

## A
**一句话。** `s` 的所有旋转都是 `s + s` 的长度为 `n` 的子串，长度相等且 `goal` 在 `s + s` 里即可。

```python
def rotate_string(s, goal):
    return len(s) == len(goal) and goal in s + s
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 漏掉长度判断：`s = "a"`、`goal = "aa"` 时 `"aa" in "aa"` 为真，应为 `false`。
- 只查 `goal in s`：`"cdeab"` 不在 `"abcde"` 里，必须在拼接后的 `s + s` 里找。

**追问。**
- 怎么保证线性时间？：`in` 的实现不保证线性，换成 KMP 匹配。
- 零次旋转算吗？：算，`s == goal` 时 `goal in s + s` 自然成立。

**同模式。** LC 459 重复的子字符串、LC 28 找出字符串中第一个匹配项的下标、LC 189 轮转数组
