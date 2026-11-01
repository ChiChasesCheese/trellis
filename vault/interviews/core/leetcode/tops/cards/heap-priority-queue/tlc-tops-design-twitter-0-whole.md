---
id: tlc-tops-design-twitter-0-whole
node: heap-priority-queue.design-twitter
type: qa
---
## Q
**LC 355 设计推特**｜Medium · 全公司热度第 323 名 · NeetCode 150

设计一个简化版的推特，可以让用户发送推文，关注 / 取消关注其他用户，能够看见关注人（包括自己）的最近 10 条推文。实现 `Twitter` 类：`Twitter()` 初始化；`postTweet(userId, tweetId)` 创建一条新推文，每次调用使用不同的 `tweetId`；`getNewsFeed(userId)` 检索当前用户新闻推送中最近 10 条推文的 ID，每一项必须由用户关注的人或者用户自己发布，按时间由最近到最远排序；`follow(followerId, followeeId)` 开始关注；`unfollow(followerId, followeeId)` 取消关注。`1 <= userId, followerId, followeeId <= 500`，`0 <= tweetId <= 10^4`，所有推特的 ID 互不相同，四个方法合计最多调用 `3 * 10^4` 次，用户不能关注自己。例：`postTweet(1, 5)`；`getNewsFeed(1)` → `[5]`；`follow(1, 2)`；`postTweet(2, 6)`；`getNewsFeed(1)` → `[6, 5]`；`unfollow(1, 2)`；`getNewsFeed(1)` → `[5]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 系统设计小题：数据结构组合（哈希表 + 列表 + 集合）+ K 路归并（k-way merge）用最大堆取前 10。

**一句话。** 每个用户按时间存自己的推文列表，关注关系存成集合；读取时把「自己 + 关注的人」每人最新的一条放进最大堆，弹出最新的，再把它同一用户的前一条补进堆，取够 10 条为止。

**识别。** 「合并多个按时间有序的列表，只要前 10 个」就是 K 路归并，堆的大小只和关注人数有关，与推文总数无关。`getNewsFeed` 只取 10 条，所以不必把所有推文排序。

**推导。** 最直接：把所有被关注者的全部推文拼起来排序取前 10，一次读取 `O(T log T)`，`T` 是总推文数，推文多了就慢。每个用户自己的推文本来就按时间顺序追加，各列表已经有序，只需要比较各列表的"队尾"：堆里放每个用户最新一条，弹出最大的时间戳，再补入该用户的前一条，最多弹 10 次，一次读取 `O(F + 10 log F)`（`F` 为关注人数，含自己）。

```python
class Twitter:
    def __init__(self) -> None:
        self.clock = 0                                              # 全局递增时间戳，保证推文可以比较先后
        self.tweets: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)   # 用户 -> [(时间, 推文 id)]，按时间追加
        self.following: defaultdict[int, set[int]] = defaultdict(set)   # 用户 -> 关注的人

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.clock += 1
        self.tweets[userId].append((self.clock, tweetId))

    def getNewsFeed(self, userId: int) -> list[int]:
        heap: list[tuple[int, int, int, int]] = []                  # (-时间, 推文 id, 用户, 在该用户列表里的下标)
        for u in self.following[userId] | {userId}:                 # 自己也算
            if self.tweets[u]:
                i = len(self.tweets[u]) - 1                         # 每个用户先放最新一条
                t, tid = self.tweets[u][i]
                heap.append((-t, tid, u, i))
        heapify(heap)
        feed: list[int] = []
        while heap and len(feed) < 10:
            _, tid, u, i = heappop(heap)                            # 当前最新的一条
            feed.append(tid)
            if i > 0:                                               # 同一用户更早的一条补进堆
                t, prev = self.tweets[u][i - 1]
                heappush(heap, (-t, prev, u, i - 1))
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)              # 没关注过也不报错
```

运行：按示例依次调用，`getNewsFeed(1)` 依次返回 `[5]`、`[6, 5]`、`[5]`；用户 `1` 发 `12` 条推文（id `1..12`）后 `getNewsFeed(1)` → `[12, 11, 10, 9, 8, 7, 6, 5, 4, 3]`；没有任何推文的用户 `getNewsFeed(9)` → `[]`。

**复杂度。** `postTweet`、`follow`、`unfollow` 为 `O(1)`；`getNewsFeed` 为 `O(F + 10 log F)`，`F` 是关注人数加 1；空间 `O(推文数 + 关注关系数)`。

**拓展优化。**
- 标准库一步到位：`heapq.merge` 对多个降序序列做懒惰归并，每个用户只需截取最近 10 条：

```python
def news_feed_merge(tweets: dict[int, list[tuple[int, int]]], users: set[int]) -> list[int]:
    # 每个用户只取最近 10 条并倒过来，得到按时间降序的序列；merge 懒惰归并，islice 取前 10
    feed = merge(*(reversed(tweets[u][-10:]) for u in users), reverse=True)
    return [tid for _, tid in islice(feed, 10)]
```

在 `getNewsFeed` 里调用 `news_feed_merge(self.tweets, self.following[userId] | {userId})` 即可。

- 规模放大后（读多写少）改成**写扩散**：发推时把推文推进每个粉丝的收件箱，读取是 `O(1)`；明星用户粉丝太多时退回**读拉取**，两种混用，这也是真实的 Feed 系统设计。

**易错点。**
- 忘了「包括自己」：`getNewsFeed(1)` 只合并关注的人，示例第一次调用会返回 `[]`（正确 `[5]`）。
- 用推文 `id` 当时间排序：`id` 不保证递增（题目只说互不相同），必须用独立的递增时间戳。
- 取消关注一个并没关注过的人时用 `remove` 会抛 `KeyError`，要用 `discard`。
- 堆元素里时间戳取负数以得到最大堆；元组第二项推文 id 只用来在时间戳相同时打破平局，实际时间戳互不相同所以不会比较到后面的字段。

**同模式。** LC 23 合并 K 个升序链表、LC 347 前 K 个高频元素、LC 295 数据流的中位数、LC 460 LFU 缓存。
