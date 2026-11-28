---
id: mlp-coding-pc07-followups
node: coding.pc07
step: 2
type: qa
---
## Q
**按异位词分组：追问与变体**｜编程轮

写完 `AnagramStore` 后面试官怎么追问？

## A
- **排序键还是计数向量：** 26 位计数向量 O(L)，但只认小写 a-z；排序键 O(L log L)，任意字符集都行。字母表固定且已知时计数更快；要支持大小写混合或 Unicode 就用排序键。
- **为什么键不能是 `Counter`：** `Counter` 是 dict 的子类，不可哈希，不能当字典的键；要先转成排序字符串，或排序后的 `(char, count)` 元组。
- **忽略大小写：** 算键前用 `word.casefold()`（比 `lower()` 更适合 Unicode），分组里仍存原始大小写的字符串，只是分组依据变了。
- **top-k 个最大的组：** 按（成员数降序，键升序）排序后取前 k 个；和 `most_common_group` 必须用同一条并列规则，否则两个查询给出不同的第一名。

```python
def top_k_groups(self, k):
    if k <= 0:
        raise ValueError("k must be positive")
    ranked = sorted(self.groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return [list(words) for _, words in ranked[:k]]     # 组数不足 k 就全返回
```

- **`remove` 为什么按字面删：** 存储里是一条条具体记录，调用方通常想删刚插入的那条，而不是同组随便一个；按字面删语义确定，也好测试。
- **内存：** N 个长度 L 的词，原始词 O(N·L)，加上 G 个键 O(G·L)。
- **每次查询都全扫的性能问题：** `most_common_group` 每次 O(G)；若频繁查询，可以另外维护按大小分桶的结构或堆，代价是增删时多一份维护。
- **会多花一个测试用例的边界：** 空存储上的查询返回空结果；同一个字符串加两次，`group_of` 里出现两次，`remove` 一次只删一个；删从未加过的词抛 `ValueError`，即使同组还有别的词；括号题里只有右括号或只有左括号都不合法，空串合法。

**英文答法。**
- "A `Counter` isn't **hashable**, so I convert it to a sorted string or tuple."
- "The count vector is faster but only for **fixed lowercase letters**; sorting works for any alphabet."
- "I use `casefold`, and keep the **original casing** in the stored words."
