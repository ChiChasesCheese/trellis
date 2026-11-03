---
id: craft-frozen-value-objects-5-scales
node: craft.idioms.frozen-value-objects
type: qa
step: 5
---
## Q
**不可变值对象 · 从分组的键到跨机器的请求摘要**｜写法

LeetCode 的字母异位词分组、LLD 的幂等转账、支付 API 的 `Idempotency-Key` 都在做「内容相同就当成同一个」。这个思路从进程内搬到多台机器时，哪一步必须变？

## A
**要点。** 三层的共同点：把「内容」压成一个可比较、可哈希的值，再用它查表。进程内，对象本身就是这个值，靠冻结保证放进表后不会变。跨机器，对象不能直接比较，要存**规范化后的摘要**（canonical form 的哈希）：同一内容在任何机器上都要得到同一个字节串。

```python
import hashlib, json
from dataclasses import asdict

# 1) LeetCode：字母异位词分组。键 = 排序后的字母元组：不可变、可哈希、内容相同则相等
def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for w in words:
        groups[tuple(sorted(w))].append(w)       # 用 list 当键会 TypeError
    return list(groups.values())

# 2) LLD：请求指纹是冻结对象，同键比较就是一个 !=
@dataclass(frozen=True, slots=True)
class Req:
    src: str
    dst: str
    amount: int

# 3) 分布式：指纹要跨进程、跨机器，对象本身不能用，存「规范化后的摘要」
def digest(r: Req) -> str:
    canon = json.dumps(asdict(r), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canon.encode()).hexdigest()[:12]

print(group_anagrams(["eat", "tea", "tan", "ate", "nat"]))
print(Req("a", "b", 5) == Req("a", "b", 5))
print(digest(Req("a", "b", 5)) == digest(Req("a", "b", 5)), digest(Req("a", "b", 6)) == digest(Req("a", "b", 5)))
```

实际输出：

```
[['eat', 'tea', 'ate'], ['tan', 'nat']]
True
True False
```

**变化。** 进程内冻结靠语言保证；跨机器靠约定：字段顺序固定（`sort_keys`）、分隔符固定、数字格式固定，否则同一个请求在两台机器上摘要不同，会被误判成冲突。服务端把摘要和键一起存下来，同键不同摘要返回 422。

**代价。** 摘要只能判断「相同与否」，不能还原请求；调试时要同时存原文。摘要还会截断或碰撞：生产里用完整的 SHA-256，这里截断只为排版。

**信号。** 一个请求或对象要「按内容」去重、缓存或比较，而内容含多个字段。
