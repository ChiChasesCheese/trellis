---
id: problems-reddit-hot-score-pure-function
node: problems.social.reddit
type: cloze
step: 2
tags: [grown]
---
In Reddit's open-sourced `hot` ranking function, the score is computed as {{c1::sign(ups − downs) × log10(max(|ups − downs|, 1)) + (created_at − epoch) / 45000}}, where `created_at` is the post's fixed creation time, not the current time. Because the formula never references 'now', a post's hot score {{c2::only needs to be recomputed when a new vote changes its ups/downs}}, not on a recurring schedule — one `ZADD`-style update per vote, touching only that post, instead of a periodic full-site rescan.

## zh
在 Reddit 开源的 `hot` 排序函数里，分数的计算方式是 {{c1::sign(ups − downs) × log10(max(|ups − downs|, 1)) + (created_at − epoch) / 45000}}，其中 `created_at` 是帖子固定的创建时间，不是当前时间。因为公式里从不出现「现在几点」，一篇帖子的 hot 分数{{c2::只需要在新投票改变了它的 ups/downs 时才重算}}，不需要按周期性任务重算——每次投票只对应一次类似 `ZADD` 的单条更新，只影响这一篇帖子，而不是对全站做周期性全量重扫描。
