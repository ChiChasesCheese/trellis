---
id: craft-memoize-on-frozen-5-scales-compile-cache
node: craft.idioms.memoize-on-frozen
type: qa
step: 5
---
## Q
**冻结与记忆化 · 从 Word Break 到编译结果缓存**｜写法

Word Break 用 `@cache` 按下标记忆化；查询解析器缓存「条件 → 语法树」；数据库缓存预编译语句，网关缓存路由表。它们都是「相同输入不重复算」。一路放大，缓存要额外面对什么问题？

## A
**要点。** 记忆化的核心条件不变：输入可哈希、输出不可变、函数是纯的。放大之后新增三个问题：上界（缓存不能无限长，否则就是内存泄漏）、失效（输入之外的依赖变了，旧结果要作废）、并发（同一个 key 的多个请求怎么合并）。

```python
from functools import cache, lru_cache

def word_break(s: str, words: frozenset[str]) -> bool:
    @cache
    def ok(i: int) -> bool:                  # 参数是整数 i：天然可哈希
        if i == len(s):
            return True
        return any(s[i:j] in words and ok(j) for j in range(i + 1, len(s) + 1))
    r = ok(0)
    print(ok.cache_info())
    return r

print(word_break("catsandog", frozenset({"cats", "dog", "sand", "and", "cat"})))

@lru_cache(maxsize=2)                        # 有上限：满了丢最久没用的
def compile_(where: str) -> str:
    return where.upper()
for w in ["a", "b", "a", "c", "b"]:
    compile_(w)
print(compile_.cache_info())
```

实际输出：

```
CacheInfo(hits=1, misses=4, maxsize=None, currsize=4)
False
CacheInfo(hits=1, misses=4, maxsize=2, currsize=2)
```

**变化。** Word Break 的缓存活在一次调用内（闭包里的 `ok`），调用结束就回收，不需要上界和失效。查询解析器的缓存是进程级，给了 `maxsize=256`：这条上界是必须的。第二段 `maxsize=2` 的输出显示：放入 `a, b, a, c, b` 时，`c` 进来挤掉了最久没用的 `b`，最后的 `b` 又得重算。SQL 预编译语句和路由表缓存多了失效：表结构或路由配置变更时，要么键里带版本号，要么主动清缓存。

**信号。** 同一个纯计算被反复调用且输入集合有限：缓存；输入集合无限，缓存必须有上界；结果依赖会变化的外部状态，缓存键里要带上版本。
