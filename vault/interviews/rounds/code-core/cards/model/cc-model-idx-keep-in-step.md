---
id: cc-model-idx-keep-in-step
node: model.index
type: qa
---
## Q
You maintain a primary map and a reverse index. What is the discipline that keeps them consistent?

## A
**Every mutation goes through one function that touches both; no call site ever writes one map directly.**

```python
def place(cid, t):
    by_target[t].add(cid); target_of[cid] = t

def remove(cid):
    t = target_of.pop(cid, None)
    if t is not None: by_target[t].discard(cid)
```

Two maps written at four call sites drift on the *fifth* — usually the reversal or shutdown path added in the last part, which removes from one and forgets the other. The symptom is a phantom entry: a connection that no server holds but that still counts against a capacity, and a hidden test that fails one placement later.

## Q zh
你同时维护一个主映射和一个反向索引。让它们保持一致的纪律是什么？

## A zh
**所有修改都经过一个同时改动两者的函数；任何调用点都不直接写单个映射。**

```python
def place(cid, t):
    by_target[t].add(cid); target_of[cid] = t

def remove(cid):
    t = target_of.pop(cid, None)
    if t is not None: by_target[t].discard(cid)
```

两个映射在四个调用点各写一遍，会在**第五个**调用点漂移 —— 通常是最后一部分才加的撤销或下线路径，它从一个映射里删了、却忘了另一个。症状是幽灵条目：一个没有任何服务器持有、却仍占着容量的连接，以及一次放置之后才失败的隐藏测试。
