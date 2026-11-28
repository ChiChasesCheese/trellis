---
id: hi-pt-image-transform-pipeline-10-match-merge
node: qb.lld.image-transform-pipeline.points
type: qa
step: 10
---
## Q
**图像变换流水线 · 化简里的 match**｜追问 · 出自：图像变换流水线 › 深入 6

化简流水线时，相邻两个步骤能否合并要同时看两个步骤的类型和字段。用什么 Python 写法最清楚？

## A
**写法。** `match a, b:` 加类模式，守卫直接写在规则旁边。

```python
case Rotate(n), Rotate(m):
    return Rotate((n + m) % 4)
case Brighten(d1), Brighten(d2) if d1 * d2 >= 0:
    return Brighten(d1 + d2)
```
**对比。** `isinstance` 链要先拆字段再比较（代数数据类型上的模式匹配）。合并成功就弹出栈顶继续往下试，所以合并会级联。
