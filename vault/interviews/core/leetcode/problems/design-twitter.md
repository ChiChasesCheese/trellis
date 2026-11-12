---
slug: design-twitter
---
## Q
**LC 355 设计推特**｜Medium

实现简化推特：`postTweet` 发推、`follow` / `unfollow` 关注与取关、`getNewsFeed` 返回自己和关注的人最近的 10 条推文 id（由新到旧）。

## A
**一句话。** 每人按时间存推文，关注存集合；取推送时把每个人最新一条放进最大堆，弹出后补同一人的前一条，取满 10 条。

```python
class Twitter:
    def __init__(self):
        self.clock = 0                  # 全局递增时间戳
        self.tweets = defaultdict(list) # 用户 -> [(时间, id)]
        self.following = defaultdict(set)

    def postTweet(self, userId, tweetId):
        self.clock += 1
        self.tweets[userId].append((self.clock, tweetId))

    def getNewsFeed(self, userId):
        heap = []     # (-时间, 推文 id, 用户, 下标)
        for u in self.following[userId] | {userId}:
            if self.tweets[u]:
                i = len(self.tweets[u]) - 1
                t, tid = self.tweets[u][i]
                heap.append((-t, tid, u, i))
        heapify(heap)
        feed = []
        while heap and len(feed) < 10:
            _, tid, u, i = heappop(heap)
            feed.append(tid)
            if i > 0:                   # 补同一人更早的一条
                t, prev = self.tweets[u][i - 1]
                heappush(heap, (-t, prev, u, i - 1))
        return feed

    def follow(self, followerId, followeeId):
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        self.following[followerId].discard(followeeId)
```

**复杂度。** `getNewsFeed` 为 `O(F + 10 log F)`（`F` 为关注数加 1），其余 `O(1)`。

**易错点。**
- 忘了「包括自己」：只合并关注的人，首次 `getNewsFeed(1)` 得 `[]`，应为 `[5]`。
- 用推文 id 当时间排序：id 不保证递增，要用独立时间戳。
- 取关用 `remove`：没关注过会抛 `KeyError`，要用 `discard`。

**追问。**
- 关注人很多怎么办？：每人只保留最近 10 条，或发推时推送到粉丝的收件箱（写扩散）。

**同模式。** LC 23 合并 K 个升序链表、LC 347 前 K 个高频元素、LC 295 数据流的中位数、LC 460 LFU 缓存
