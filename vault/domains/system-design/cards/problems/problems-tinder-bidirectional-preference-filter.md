---
id: problems-tinder-bidirectional-preference-filter
node: problems.social.tinder
type: qa
step: 3
tags: [grown]
---
## Q
In a dating app's candidate feed, why does the geo-sharded search index query need to apply preference filters (age range, gender interest) bidirectionally — not just 'candidates matching my preferences' but also 'candidates whose own preferences would match me' — rather than filtering only on the viewer's own stated preferences?

## A
Filtering only on the viewer's stated preferences can return candidates who would never be interested back (their own preferences exclude the viewer), producing swipes that can never become a mutual match no matter which way the viewer swipes — wasted interaction and worse candidate density. Applying both directions as filter conditions in the same index query (rather than filtering one direction in the index and the other in application code) ensures the index only returns candidates who are mutually eligible, keeping the effective candidate density high even in areas with an unbalanced population.

## Q zh
在约会应用的候选人 feed 里，为什么地理分片搜索索引的查询要双向应用偏好过滤——不只是「符合我偏好的候选人」，还要「对方的偏好也会匹配我」——而不是只按查看者自己设置的偏好过滤？

## A zh
只按查看者自己的偏好过滤，可能返回一些根本不会对查看者感兴趣的候选人（对方自己的偏好设置就排除了查看者），无论查看者怎么滑都不可能产生互相匹配——造成无意义的滑动和更差的有效候选密度。把两个方向的条件都作为过滤条件放进同一次索引查询（而不是索引里过滤一个方向、应用层再过滤另一个方向），能保证索引只返回真正双向兼容的候选人，即使在人口结构不均衡的地区也能维持较高的有效候选密度。
