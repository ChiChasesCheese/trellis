---
slug: rank-teams-by-votes
---
## Q
**LC 1366 通过投票对团队排名**｜Medium

每张选票是对所有团队的排位字符串。按「第一名票数、第二名票数……」依次比较排序，全平局按字母序，返回团队排名字符串。

## A
**一句话。** 统计每队在各名次上的票数，把「负票数列表 + 字母」当排序键。

```python
def rank_teams(votes):
    m = len(votes[0])
    cnt = {t: [0] * m for t in votes[0]}  # 第 i 名票数
    for v in votes:
        for i, t in enumerate(v):
            cnt[t][i] += 1
    # 取负：票多的在前；列表比较 = 先比第一名再比第二名
    key = lambda t: ([-c for c in cnt[t]], t)
    return "".join(sorted(cnt, key=key))
```

**复杂度。** 时间 `O(Vm + m² log m)`，空间 `O(m²)`。

**易错点。**
- 只比第一名票数：`["WXYZ","XYZW"]` 得 `"WXYZ"`，应为 `"XWYZ"`。
- 没取负：票少的排前面。
- 缺字母序兜底：全平局时保留输入顺序，`["BCA","CAB","CBA","ABC","ACB","BAC"]` 得 `"BCA"`，应为 `"ABC"`。

**追问。**
- 为什么列表能直接当键？：Python 列表按字典序比较，正好是逐名次比较。

**同模式。** LC 451 根据字符出现频率排序、LC 1636 按照频率将数组升序排序、LC 937 重新排列日志文件、LC 179 最大数
