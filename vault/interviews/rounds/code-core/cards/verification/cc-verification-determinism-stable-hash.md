---
id: cc-verification-determinism-stable-hash
node: verification.determinism
type: qa
---
## Q
You bucket users into a 10 % rollout with `hash(user_id) % 100`. It works, then a rerun puts different users in the bucket. Why, and what do you use instead?

## A
**`hash()` on `str` and `bytes` is salted per process** (`PYTHONHASHSEED`), so it is not stable across runs, machines or interpreter versions.

```python
bucket = zlib.crc32(f"{flag}:{user}".encode()) % 100
```

- `zlib.crc32` and `hashlib.md5(...).hexdigest()` are stable and fast. `hash()` of an `int` happens to be stable, which is precisely how the bug hides during development.
- Put the flag or experiment name **inside** the hashed string, or every rollout buckets the same users together and your "independent" experiments are correlated.
- Anything a grader re-runs — a rollout, a shard assignment, a tie-break — must not depend on `hash()`.

## Q zh
你用 `hash(user_id) % 100` 把用户分进 10% 的灰度桶。一开始好用，重跑一次却换了一批用户。为什么？改用什么？

## A zh
**`str` 和 `bytes` 的 `hash()` 是按进程加盐的**（`PYTHONHASHSEED`），所以它在不同运行、不同机器、不同解释器版本之间都不稳定。

```python
bucket = zlib.crc32(f"{flag}:{user}".encode()) % 100
```

- `zlib.crc32` 和 `hashlib.md5(...).hexdigest()` 稳定且快。`int` 的 `hash()` 恰好是稳定的 —— 这正是这个 bug 在开发期藏身的方式。
- 把开关名或实验名放**进**被哈希的字符串里，否则每个灰度都把同一批用户分到一起，你那些「互相独立」的实验其实是相关的。
- 任何会被评测机重跑的东西 —— 灰度、分片分配、平局裁决 —— 都不能依赖 `hash()`。
