---
id: tlc-most-popular-video-creator-2-code
node: b.most-popular-video-creator
type: qa
step: 2
---
## Q
**LC 2456 最流行的视频创作者**｜写出 Python 实现

字符串列表 `creators`、`ids` 与整数列表 `views`，长度相同，`1 <= n <= 10^5`，名字与 id 长 `1..5`、只含小写字母，`0 <= views[i] <= 10^5`。创作者的流行度是其所有视频的播放量之和。返回所有流行度最高的创作者，每人配上他播放量最大的视频 id（并列取字典序最小）。结果顺序任意。

## A
**思路。** 一趟 `zip` 扫描：用 `defaultdict(int)` 累加流行度；用字典保存每个创作者当前最佳的 `(-播放量, id)`，新视频的元组更小就替换；最后取最大流行度，筛出所有等于它的创作者。

```python
from collections import defaultdict


def most_popular_creator(creators: list[str], ids: list[str], views: list[int]) -> list[list[str]]:
    popularity: defaultdict[str, int] = defaultdict(int)
    best_video: dict[str, tuple[int, str]] = {}    # 创作者 -> (-播放量, id)，元组越小越好
    for creator, vid, view in zip(creators, ids, views):
        popularity[creator] += view
        candidate = (-view, vid)                   # 播放量大优先，并列取字典序小的 id
        if creator not in best_video or candidate < best_video[creator]:
            best_video[creator] = candidate
    top = max(popularity.values())
    return [[c, best_video[c][1]] for c, total in popularity.items() if total == top]
```

运行：示例 1 → `[['alice', 'one'], ['bob', 'two']]`，示例 2 → `[['alice', 'b']]`，`(["a"], ["x"], [0])` → `[['a', 'x']]`。

**复杂度。** 时间 `O(n)`；空间 `O(k)`，`k` 是不同创作者的个数。

**写法要点。** `zip(creators, ids, views)` 同时遍历三个数组，不用下标。`defaultdict(int)` 让 `popularity[c] += view` 无需先判断是否存在。把“播放量大、id 小”编码成 `(-view, vid)` 元组，Python 的元组比较会先比第一项再比第二项，一个 `<` 就同时处理两个条件。`best_video[c][1]` 取元组的第二项（id）。变量名 `vid` 避开内置函数 `id`。
