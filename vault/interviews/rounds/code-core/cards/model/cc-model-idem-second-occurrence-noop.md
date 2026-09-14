---
id: cc-model-idem-second-occurrence-noop
node: model.idempotency
type: qa
---
## Q
A `CONNECT c1` arrives for a connection id that is already active. What happens, and how do you recognize the case?

## A
**Nothing happens — the handler returns before any state changes, and produces no output line.**

```python
if cid in live:
    return                # duplicate of a live id
```

Recognition is a membership test against the set of *currently live* ids, done first, before any placement or logging. The two mistakes: recognizing it after allocating a slot (the slot leaks), and logging the placement anyway (a spurious output line fails the byte comparison even though the state is right).

The first occurrence always stands; idempotency never means "the last one wins".

## Q zh
一条 `CONNECT c1` 到达，而这个连接 id 已经处于活动状态。会发生什么？你怎么识别这种情形？

## A zh
**什么都不发生 —— handler 在任何状态改变之前返回，也不产生任何输出行。**

```python
if cid in live:
    return                # duplicate of a live id
```

识别方式是对**当前活动** id 集合做成员判断，而且要放在最前面，先于任何放置或日志。两个错误：分配了槽位之后才识别（槽位泄漏）；以及照样打了日志（尽管状态正确，多余的输出行仍会让逐字节比较失败）。

第一次出现永远算数；幂等从不意味着"后来者覆盖"。
