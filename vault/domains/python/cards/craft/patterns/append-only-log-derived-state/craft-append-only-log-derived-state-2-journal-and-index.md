---
id: craft-append-only-log-derived-state-2-journal-and-index
node: craft.patterns.append-only-log-derived-state
type: qa
step: 2
---
## Q
**只追加日志 + 派生状态 · 账本里的日志、余额、冲正**｜写法

账本需要又快又准的当前余额，也要能审计每一笔，还要能纠错。把余额直接存成一个会被修改的数字行不行？日志和余额的关系应该是什么？

## A
**要点。** 日志（journal）是唯一事实来源，只追加、不修改；余额是日志的缓存，在每次写入的同一个临界区里同步更新。纠错不改历史，而是追加一条相反的冲正分录（reversing entry）。

```python
def post(self, e: Entry) -> None:
    assert sum(d for _, d in e.postings) == 0       # 校验在前
    self._journal.append(e)                         # 提交：追加事实
    for acct, d in e.postings:
        self._bal[acct] += d                        # 同一个临界区里更新索引

def reverse(self, e_id, new_id):
    old = next(e for e in self._journal if e.id == e_id)
    # 纠错 = 追加一条相反的分录，历史原样保留
    self.post(Entry(new_id, tuple((a, -d) for a, d in old.postings), reverses=e_id))
```

记两笔，冲正第一笔，对账（拿日志重算和索引比）：

```
日志长度 3 余额 {'cash': -50, 'fees': 0, 'rent': 50}
索引 == 重放日志: True
总和恒为 0: True
```

**为什么。** 「余额只是日志的缓存」带来可验证的不变量：随时可以重放日志重算，与索引必须相等；所有账户总和恒为 0。纠错只追加，审计看得到谁在什么时候改了什么；并发上也不存在「同时修改同一行历史」。

**易错。** 日志和索引必须在同一把锁里更新，否则读者会看到「日志有了、余额没动」。
