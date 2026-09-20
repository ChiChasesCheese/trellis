---
id: problems-text-editor-random-model-test
node: problems.components.text-editor
type: qa
step: 10
tags: [grown]
---
## Q
撤销／重做的 bug 几乎都藏在手写不出来的操作组合里（在刚撤销过的位置删除、撤销到底再插入……）。用什么测试方法能把它们逼出来？

## A
拿一个**显然正确但很慢**的朴素模型当参照，跑长随机序列逐步对照。具体做法：固定随机种子造一串插入／删除／撤销，同时维护一个"每步之后的完整文本"的列表——编辑就追加一份全文，撤销就弹出一份——每一步都断言编辑器的文本等于列表末尾那份。

```python
rng = random.Random(20260920)
for _ in range(600):
    ...  # 随机插入 / 删除 / 撤销
    assert editor.text == model[-1]
```

那个模型慢得不能用在生产里（每步存一份全文），但它显然正确，正好用来检查那个聪明的实现。固定种子保证失败可以复现。任何"有一个朴素参照实现"的问题都该这么测。
