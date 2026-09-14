---
id: cc-round-ambiguity-comment-the-assumption
node: round.ambiguity
type: qa
---
## Q
Where and how do you record an assumption you had to make about an underspecified rule?

## A
**As a one-line comment at the decision point, quoting the spec's own words.**

```python
# spec: "minimum volume before the ratio applies" — read as a gate on
# ratio thresholds only; count thresholds stay volume-free.
if kind == "ratio" and total < min_count:
    return False
```

At the decision point, because that is where the next reader (or you at minute 50) asks the question. Quoting the spec's phrase, because it lets a reviewer check your reading against the source without re-reading everything. Never in a README nobody opens, and never only in your head.

## Q zh
对一条说得不够清楚的规则，你不得不做了某个假设。在哪里、以什么形式记录它？

## A zh
**在做决定的那一行写一句注释，引用题面自己的措辞。**

```python
# spec: "minimum volume before the ratio applies" — read as a gate on
# ratio thresholds only; count thresholds stay volume-free.
if kind == "ratio" and total < min_count:
    return False
```

写在决策点，因为下一个读者（或第 50 分钟的你）正是在那里产生疑问。引用题面原话，是为了让 reviewer 不必重读全文就能核对你的读法。别写进没人打开的 README，更别只留在脑子里。
