---
slug: remove-letter-to-equalize-frequency
---
## Q
**LC 2423 删除字符使频率相同**｜Easy

小写字母字符串 `word`。恰好删除一个字符后，剩下的所有字母出现次数是否可以相同。

## A
**一句话。** 试着对每种字母减去一次出现，看剩余字母的出现次数（忽略为 `0` 的）是否只有一个不同值。

```python
def equal_frequency(word):
    cnt = Counter(word)
    for c in list(cnt):
        cnt[c] -= 1
        if len({v for v in cnt.values() if v}) == 1:
            return True
        cnt[c] += 1                     # 还原
    return False
```

**复杂度。** 时间 `O(26²)`，空间 `O(26)`。

**易错点。**
- 把次数为 `0` 的字母也算进去：删光一种字母后它不再存在。
- 忘了还原：试下一个字母时计数已被改过。

**追问。**
- `word` 很长也不怕？：只有 `26` 种字母，每次检查 `O(26)`。

**同模式。** LC 1647 字符频次唯一的最小删除次数、LC 2370 最长理想子序列
