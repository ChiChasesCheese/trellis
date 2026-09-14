---
id: cc-toolbox-cache-versioned-map
node: toolbox.cache
type: qa
---
## Q
"What was the value of key `k` at time `t`?" — with writes arriving out of order. Design the structure.

## A
**Per key, a list of write times kept sorted, parallel to a list of values.** The read is `bisect_right(times, t) - 1`.

```python
i = bisect_right(ts, t)
if i and ts[i - 1] == t:
    vs[i - 1] = value                # same key, same time ⇒ last write wins
else:
    ts.insert(i, t); vs.insert(i, value)
```

- `bisect_right - 1` gives the latest write **at or before** `t`, so a read exactly at a write time sees that write ([[cc-toolbox-sorted-bisect-left-right]]).
- Out-of-order writes are why this is an insertion and not an append ([[cc-toolbox-sorted-insort-cost]]).
- `i == 0` means there is no write at or before `t` — the "no value" sentinel, not an empty collection ([[cc-output-sentinels-null-vs-empty]]).
- With TTLs, an **expired newest version does not fall back** to the older one: it reads as missing, because the newer write is what is in force.

## Q zh
「key `k` 在 `t` 时刻的值是多少？」—— 而且写入是乱序到达的。设计这个结构。

## A zh
**每个 key 一份保持有序的写入时间列表，外加一份平行的值列表。** 读取是 `bisect_right(times, t) - 1`。

```python
i = bisect_right(ts, t)
if i and ts[i - 1] == t:
    vs[i - 1] = value                # 同 key 同时间 ⇒ 后写覆盖
else:
    ts.insert(i, t); vs.insert(i, value)
```

- `bisect_right - 1` 给出**在 `t` 或之前**的最新写入，所以恰好在写入时刻读取会看到那次写入（[[cc-toolbox-sorted-bisect-left-right]]）。
- 写入乱序正是这里用插入而不是追加的原因（[[cc-toolbox-sorted-insort-cost]]）。
- `i == 0` 表示 `t` 或之前没有任何写入 —— 这是「无值」哨兵，而不是空集合（[[cc-output-sentinels-null-vs-empty]]）。
- 带 TTL 时，**过期的最新版本不会回退**到更旧的那个：它读作缺失，因为生效的是那次更新的写入。
