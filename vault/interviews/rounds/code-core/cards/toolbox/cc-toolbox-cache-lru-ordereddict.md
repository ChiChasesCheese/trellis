---
id: cc-toolbox-cache-lru-ordereddict
node: toolbox.cache
type: qa
---
## Q
A fixed-capacity LRU with O(1) get and put. Write it with the stdlib.

## A
**`OrderedDict` — `move_to_end` on touch, `popitem(last=False)` to evict.**

```python
def get(self, k):
    if k not in self.d: return None
    self.d.move_to_end(k)
    return self.d[k]

def put(self, k, v):
    self.d[k] = v; self.d.move_to_end(k)
    if len(self.d) > self.cap:
        self.d.popitem(last=False)          # evict the least recently used
```

- A plain `dict` also preserves order but has no `move_to_end`: touching a key means `del` then re-insert, which is the same thing spelled worse ([[cc-toolbox-hash-insertion-order]]).
- Evict **after** inserting, and only when over capacity — evicting first lets a `put` of an existing key shrink the cache below its size.
- `functools.lru_cache(maxsize=n)` is the right answer when you are memoizing a pure function, and the wrong one when the entries are program state you also mutate.
- What counts as a "touch" is a spec decision, not a library one ([[cc-toolbox-cache-lru-tiebreak]]).

## Q zh
一个固定容量、get 和 put 都 O(1) 的 LRU。用标准库写出来。

## A zh
**`OrderedDict` —— 访问时 `move_to_end`，淘汰时 `popitem(last=False)`。**

```python
def get(self, k):
    if k not in self.d: return None
    self.d.move_to_end(k)
    return self.d[k]

def put(self, k, v):
    self.d[k] = v; self.d.move_to_end(k)
    if len(self.d) > self.cap:
        self.d.popitem(last=False)          # 淘汰最久未使用的
```

- 普通 `dict` 也保持顺序，但没有 `move_to_end`：碰一个 key 就得 `del` 再插入，是同一件事的糟糕写法（[[cc-toolbox-hash-insertion-order]]）。
- 在插入**之后**、且仅在超容量时淘汰 —— 先淘汰会让对已有 key 的 `put` 把缓存缩到容量以下。
- 记忆化纯函数时 `functools.lru_cache(maxsize=n)` 是正确答案；当条目是你还会修改的程序状态时它是错误答案。
- 什么算一次「访问」是 spec 的决定，不是库的决定（[[cc-toolbox-cache-lru-tiebreak]]）。
