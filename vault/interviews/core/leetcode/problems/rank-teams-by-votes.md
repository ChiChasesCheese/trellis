---
slug: rank-teams-by-votes
---
## Q
**LC 1366 通过投票对团队排名（Rank Teams by Votes）**｜Medium

每个投票者都按从高到低的顺序对所有参赛团队排位。排名规则：先比「排位第一」的票数；并列时比「排位第二」的票数，以此类推；考虑完所有投票后仍并列，则按团队字母顺序排名。给你字符串数组 `votes` 代表全体投票者给出的排位情况，返回按排名系统排序后的所有团队字符串。`1 <= votes.length <= 1000`，`1 <= votes[i].length <= 26`，所有 `votes[i]` 长度相同，由互不重复的大写字母组成，且所有投票出现的字母集合相同。例：`votes = ["ABC","ACB","ABC","ACB","ACB"]` → `"ACB"`；`votes = ["WXYZ","XYZW"]` → `"XWYZ"`；`votes = ["ZMNAGUEDSJYLBOPHRQICWFXTVK"]` → `"ZMNAGUEDSJYLBOPHRQICWFXTVK"`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 计数矩阵 + 自定义排序键（元组/列表字典序比较）。

**一句话。** 为每个团队统计「在每个名次上获得的票数」，排序键就是这串票数（取负，票多的在前）再接团队字母。

**识别。** 「先比第一名票数，平局再比第二名……」恰好是列表按字典序比较；最后「按字母序」是键末尾追加团队名。团队至多 26 个、名次至多 26 个，计数表很小。

**推导。** 把每张选票逐个比较两两团队很难写对。换个角度：每个团队的得分向量 `[第1名票数, 第2名票数, ...]` 就是完整的比较依据，先把向量算出来（遍历所有选票 `O(V * m)`），再排序。票数大的靠前，所以键里取负数。

```python
def rank_teams(votes: list[str]) -> str:
    m = len(votes[0])
    count = {team: [0] * m for team in votes[0]}     # count[队][i]：该队获得「排位第 i 名」的票数
    for vote in votes:
        for i, team in enumerate(vote):
            count[team][i] += 1
    # 排位靠前的票越多越靠前：取负后升序，列表比较正好是「先比第一名票数，平局再比第二名……」；全平局按字母序
    return "".join(sorted(count, key=lambda t: ([-c for c in count[t]], t)))
```

运行：`["ABC","ACB","ABC","ACB","ACB"]` → `"ACB"`，`["WXYZ","XYZW"]` → `"XWYZ"`，单张选票 `"ZMNAGUEDSJYLBOPHRQICWFXTVK"` → 原样返回，`["BCA","CAB","CBA","ABC","ACB","BAC"]` → `"ABC"`（完全平局，按字母序），`["A"]` → `"A"`。

**复杂度。** 时间 `O(V * m + m^2 log m)`（`V` 张选票、`m` 个团队）；空间 `O(m^2)`。

**易错点。**
- 排序键只有第一名票数：`["WXYZ","XYZW"]` 里 `W`、`X` 第一名各 1 票，必须继续比第二名，只比第一名会得到 `"WXYZ"`，正确 `"XWYZ"`。
- 按票数升序排：没取负就会把票数少的排在前面，示例一得到 `"BCA"`。
- 平局时没有字母序兜底：Python 的 `sorted` 稳定，会保留 `votes[0]` 里的顺序，`["BCA","CAB","CBA","ABC","ACB","BAC"]` 会得到 `"BCA"`，正确 `"ABC"`。

**同模式。** LC 451 根据字符出现频率排序、LC 1636 按照频率将数组升序排序、LC 937 重新排列日志文件、LC 179 最大数。
