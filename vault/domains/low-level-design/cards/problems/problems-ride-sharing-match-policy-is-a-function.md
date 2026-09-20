---
id: problems-ride-sharing-match-policy-is-a-function
node: problems.marketplaces.ride-sharing
type: qa
step: 6
tags: [grown]
---
## Q
网约车的匹配规则要从「最近优先」换成「距离 + 评分 + 空闲时长」的综合打分。在 Python 里该怎么留这条缝？打分函数本身有哪两个坑？

## A
留成一个**函数类型**，不是一族抽象基类的子类——这就是策略模式（Strategy）在 Python 里的自然形态：

```python
MatchPolicy = Callable[[RideRequest, Driver, datetime], float]

def weighted_score(per_km=1.0, per_rating_point=1.0, per_idle_minute=0.05) -> MatchPolicy:
    def score(request, driver, now) -> float:
        idle = (now - driver.idle_since).total_seconds() / 60
        return (driver.location.distance_to(request.pickup) * per_km
                - driver.rating * per_rating_point - idle * per_idle_minute)
    return score
```

策略只有一个方法、没有跨调用要记的状态，就该是函数；要参数用闭包，要组合就套一层函数。写成抽象基类唯一的收益是「能被 `isinstance` 认出来」，而这里没人需要。

两个坑：

1. **量纲**。距离是公里、评分是分、空闲是分钟，相加没有物理意义——所以权重本身就是换算率（「一个评分点值多少公里」）。说出这句话等于承认这是业务调参，不是数学。
2. **并列必须被打破**。排序键要写成 `(score, driver.id)`。只按 score 排，同分时派给谁取决于字典迭代顺序，测试会飘，线上会出现没法复现的投诉。确定性是可测试性的前提。

另外，空闲时长取负权重是司机端公平性的最低限度：只按距离排，市中心那位永远抢不到单。
