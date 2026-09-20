---
id: problems-tinder-bloom-filter-storage-reduction
node: problems.social.tinder
type: qa
step: 4
tags: [grown]
---
## Q
For a dating app's seen-set (the set of users a given user has already swiped on, which must never be re-shown), storing 3×10^11 total swipe edges explicitly as 8-byte user ids costs about 2.4 TB. Storing the same relationship as per-user Bloom filters at a 0.1% target false-positive rate (about 14.38 bits/element) costs about 0.539 TB. What is the storage reduction factor, and why is this safe given that a Bloom filter can only err by saying 'possibly seen' about someone who was never actually swiped?

## A
2.4 TB / 0.539 TB ≈ 4.45x storage reduction. This is safe because a Bloom filter never produces false negatives — it will never claim an actually-seen user is unseen, so a previously-swiped profile can never be wrongly re-shown. Its only error direction is a false positive: occasionally hiding a candidate who was never actually swiped, which just means one fewer candidate shown out of a pool of thousands — a negligible cost in exchange for the storage savings.

## Q zh
在约会应用的 seen set（用户已经划过、绝不能再展示的集合）里，把 3×10^11 条滑动边显式存成 8 字节用户 id 需要约 2.4 TB；把同样的关系存成每用户一个 Bloom filter（目标假阳性率 0.1%，约 14.38 bits/element）只需要约 0.539 TB。存储降低了多少倍？考虑到 Bloom filter 唯一可能出错的方向是把「从未划过的人」误判为「可能划过」，为什么这是安全的？

## A zh
2.4 TB / 0.539 TB ≈ 4.45 倍存储降低。这是安全的，因为 Bloom filter 永远不会产生假阴性——它绝不会把一个确实已经划过的用户误判为「没划过」，所以一个划过的档案绝不可能被误判重新展示。它唯一的出错方向是假阳性：偶尔把一个从未真正划过的候选人误判排除，这只意味着在几千人的候选池里少展示一个人，为换来这样的存储节省，代价可以忽略不计。
