---
id: tlc-most-popular-video-creator-0-whole
node: b.most-popular-video-creator
type: qa
---
## Q
**LC 2456 最流行的视频创作者**｜Medium · TikTok 高频

给两个字符串数组 `creators`、`ids` 和一个整数数组 `views`，长度都是 `n`。第 `i` 个视频的创作者是 `creators[i]`，视频 id 是 `ids[i]`，播放量是 `views[i]`。创作者的**流行度**是他所有视频播放量的总和。找出流行度**最高**的创作者，以及该创作者播放量**最大**的视频 id：流行度最高的创作者有多个时，全部返回；某个创作者有多个播放量最高的视频时，只取**字典序最小**的 id。返回二维字符串数组 `answer`，`answer[i] = [creator_i, id_i]`，可以按任意顺序返回。`n == creators.length == ids.length == views.length`，`1 <= n <= 10^5`，`1 <= creators[i].length, ids[i].length <= 5`，`creators[i]` 和 `ids[i]` 只含小写英文字母，`0 <= views[i] <= 10^5`。例：`creators = ["alice","bob","alice","chris"]`，`ids = ["one","two","three","four"]`，`views = [5,10,5,4]` → `[["alice","one"],["bob","two"]]`；`creators = ["alice","alice","alice"]`，`ids = ["a","b","c"]`，`views = [1,2,2]` → `[["alice","b"]]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 一趟扫描，用哈希表按创作者聚合两样东西：播放量总和（流行度）和“最佳视频”——用元组 `(-播放量, id)` 表示，元组越小越好，一次比较同时处理“播放量大优先”和“并列取字典序小”。最后找最大流行度，输出所有达到它的创作者及其最佳视频 id。`O(n)`。

**识别。** 「按某个字段分组，每组算总和 / 取最优」是哈希表聚合（group-by）的标志。“多关键字的最优”（先看播放量大，再看 id 小）适合用元组比较一次搞定。`n = 10^5`，一趟哈希聚合足够，不需要排序。

**推导。** 暴力：对每个创作者扫描全数组求总和，再扫一遍找最佳视频，`O(n · 创作者数)`，最坏 `O(n^2)`。浪费：每个创作者重复扫整个数组。洞察：一趟扫描，把每个视频累加到它的创作者名下，同时维护该创作者当前最佳的 `(−播放量, id)`。选 `−播放量` 是因为 Python 元组默认取最小，取负后“播放量最大”变成“最小”，并列时第二个元素 id 的字典序最小自然胜出。扫完后取流行度的最大值，把等于它的创作者全部输出。

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

运行：示例 1 → `[['alice', 'one'], ['bob', 'two']]`，示例 2 → `[['alice', 'b']]`，`(["a"], ["x"], [0])` → `[['a', 'x']]`；`10^5` 个视频、随机创作者与 id → 约 `7 ms`。

**复杂度。** 时间 `O(n)`：一趟扫描加一趟输出；空间 `O(k)`，`k` 为不同创作者数。

**易错点。**
- 更新最佳视频时只比较播放量、用 `>`：并列时保留先出现的 id，而不是字典序最小的。`creators = ["x","x"]`，`ids = ["c","b"]`，`views = [2,2]`：错误写法返回 `[['x', 'c']]`，正确是 `[['x', 'b']]`。
- 只返回流行度最高的一个创作者：题目要求并列的全部返回（示例 1 的 `alice` 和 `bob` 各 `10`）。
- 用播放量最大的视频的播放量当流行度：流行度是总和，不是单个视频的播放量。

**追问。**
- 返回前 `k` 个最流行的创作者：用 `heapq.nlargest(k, popularity.items(), key=...)`，`O(n log k)`，比整体排序省。
- 数据流式到达，随时查询当前最流行的创作者：维护字典的同时再维护“当前最大流行度和对应的创作者集合”，新视频只会让某个创作者的流行度增加，更新后与当前最大值比较即可。
- `views` 也可能为负或需要去重 id：先问清规则；如果同一个 id 可能出现多次，需要按 id 去重后再累加。

**同模式。** LC 692 前 K 个高频单词、LC 347 前 K 个高频元素、LC 1636 按频率排序、LC 49 字母异位词分组、LC 2418 按身高排序。
