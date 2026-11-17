---
id: bank-linear-multi-pattern-automaton
node: bank.structures.linear
type: qa
step: 4
---
## Q
内容审核按关键词拦截，关键词表从一百个涨到一百万个。每次检查都写 `any(w in text for w in words)` 并且持着锁，会怎样？换成什么结构，才能让每个字符只处理一次？

## A
**Aho–Corasick：字典树加失败转移，一遍扫完**

- **逐词扫描的代价**：时间与词数成正比。十万个 8 字母词、2000 字符的内容，逐词 `in` 实测约 70 ms（3.11）；检查在锁里做，吞吐就是每秒十几次；
- **状态**：已读字符中，仍是某个关键词前缀的最长后缀。每读一个字符，从当前状态走一步，不回头重读；
- **命中**：每个状态带「以它结尾的所有关键词」，扫描时取并集；`ushers` 里同时出现 `she`、`he`、`hers`；
- **下面的代码是定义版**：用 `go` 按定义算转移，`@cache` 记住，每个状态第一次出现时要扫一遍词表。生产版用广度优先一次建好失败指针，建表只与关键词总字符数有关；
- **更新配置**：自动机建好后不可变，新词表在后台建新的，再一次性换引用，检查不会被建表阻塞；
- **先归一化再建**：关键词和内容都先 `casefold()`，因为 `"ß".casefold()` 是 `"ss"`，只用 `lower()` 会漏掉全大写的 `STRASSE`。

```python
from functools import cache
def make_scanner(words):
    prefixes = {w[:i] for w in words for i in range(len(w) + 1)}   # 字典树的全部节点
    @cache
    def go(s): return s if s in prefixes else go(s[1:])           # 最长的、仍是前缀的后缀
    @cache
    def out(state): return frozenset(w for w in words if state.endswith(w))
    def find(text):
        state, hits = "", set()
        for ch in text:
            state = go(state + ch); hits |= out(state)            # 每个字符只走一步
        return hits
    return find
print(sorted(make_scanner(["he", "she", "hers", "his"])("ushers")))   # ['he', 'hers', 'she']
```

<details class="pt"><summary>延伸</summary>

新的瓶颈是内存：每个节点一个 `dict`，词表到百万级要用紧凑的数组表示（双数组字典树）或 C 实现的库；再往上就是把匹配拆成独立的服务，按用户或按关键词分片。拦截服务里的「一把锁罩住判封、匹配、记一次」与自动机的取舍，见 [[solution-lcp-keyword-user-blocklists|关键词与用户拦截（Keyword & User Blocking）]]。

</details>

**知识点：**栈、队列、Trie 及变体（Linear & Trie）
