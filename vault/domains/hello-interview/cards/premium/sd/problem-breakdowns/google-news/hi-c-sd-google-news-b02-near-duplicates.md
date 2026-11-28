---
id: hi-c-sd-google-news-b02-near-duplicates
node: sd.problem-breakdowns.google-news.beyond
type: qa
step: 2
---
## Q
**新闻聚合 · 拓展：同一事件几十家媒体都在报道，怎么去重和聚类**｜拓展 · 加分

动态流里同一场比赛有 50 篇相近的报道，怎么识别并合并？Python 里怎么写？

## A
- **问题：** 按 URL 去重只能去掉完全重复的链接；转载、通稿和同一事件的各家改写，URL 不同、内容相近。用户看到一屏同一件事很糟糕。
- **相似度：** 把文本切成连续 k 个词的片段（shingle），两篇的相似度用 Jaccard（交集 ÷ 并集）衡量。
- **MinHash：** 对每篇文章的片段集合，用 n 个哈希函数各取最小值，得到长度 n 的签名；两个签名对应位置相等的比例，就是 Jaccard 的无偏估计，所以只存 128 个整数就能比较，不用保存全文。实测两句只差一个词的新闻：真实 Jaccard 0.65，128 位签名估计 0.72（标准差约 0.04）；无关文章估计 0.00。
- **LSH（局部敏感哈希）：** 把签名分成几段，段内相同就放进同一个桶，只比较同桶的文章，避免两两比较的平方复杂度。
- **SimHash：** 另一种常用方法，把文章映射成 64 位指纹，汉明距离小就是近似重复，存储更小，适合只要"是不是重复"的场景。
- **用在哪里：** 采集管线入库时聚类，动态流里同一簇只显示代表性的一篇，并标注"另有 N 家报道"。
- **模式。** 草图（sketch）：用小而定长的概率摘要代替全量比较。

```python
def minhash(sh: set[str], n: int = 128) -> list[int]:
    # 用 n 个不同的盐模拟 n 个哈希函数，每个函数取所有片段哈希的最小值
    return [min(int.from_bytes(blake2b(f"{i}|{s}".encode(), digest_size=8).digest(), "big")
                for s in sh) for i in range(n)]

def est_jaccard(a, b) -> float:
    return sum(x == y for x, y in zip(a, b)) / len(a)   # 相等位置的比例 ≈ Jaccard
```
