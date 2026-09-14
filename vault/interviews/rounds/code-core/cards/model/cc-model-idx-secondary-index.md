---
id: cc-model-idx-secondary-index
node: model.index
type: qa
---
## Q
Connections are stored per server as a set, and now `DISCONNECT <connection_id>` must find the server holding it. What do you add?

## A
**A secondary index — the reverse map — maintained in the same functions that maintain the first.**

```python
by_target[t].add(cid)
target_of[cid] = t          # both, always together
```

Without it, `DISCONNECT` scans every server: fine for three servers, fatal for 10^5. With it, every placement and every removal must update both maps, so wrap the pair in `place(cid, t)` and `remove(cid)` rather than repeating two lines at four call sites. See [[cc-model-idx-keep-in-step]].

## Q zh
连接按服务器存成集合，现在 `DISCONNECT <connection_id>` 必须找到持有它的服务器。你加什么？

## A zh
**加一个二级索引 —— 反向映射 —— 并在维护第一个映射的同一批函数里维护它。**

```python
by_target[t].add(cid)
target_of[cid] = t          # both, always together
```

没有它，`DISCONNECT` 就要扫遍所有服务器：三台还行，10^5 台就致命。有了它，每次放置和每次移除都必须更新两个映射，所以把这一对包进 `place(cid, t)` 和 `remove(cid)`，而不是在四个调用点各重复两行。见 [[cc-model-idx-keep-in-step]]。
