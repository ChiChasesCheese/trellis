---
slug: minimum-number-of-pushes-to-type-word-ii
---
## Q
**LC 3016 输入单词需要的最少按键次数 II**｜Medium

把 26 个字母任意分配到 8 个按键上，同键第 `p` 个字母要按 `p` 次。求打出 `word` 的最少按键总次数。

## A
**一句话。** 每档 8 个位置代价分别为 1、2、3…，按出现次数从高到低依次填：第 `i` 个字母代价 `i // 8 + 1`。

```python
def minimum_pushes(word):
    freq = sorted(Counter(word).values(), reverse=True)
    return sum(f * (i // 8 + 1) for i, f in enumerate(freq))
```

**复杂度。** 时间 `O(n)`，空间 `O(26)`。

**易错点。**
- 按字母表顺序分配：要按频率，高频字母放第一位。
- 写成 `i // 8`：第一档代价是 1 不是 0。

**追问。**
- 为什么贪心对？：频率 `a > b`、代价 `p < q` 时 `ap + bq < aq + bp`，交换逆序只会更好。
- 每个字母只出现一次（LC 3014）？：频率全为 1，答案只看字母个数。

**同模式。** LC 455 分发饼干、LC 3014 输入单词需要的最少按键次数 I、LC 2285 道路的最大总重要性
