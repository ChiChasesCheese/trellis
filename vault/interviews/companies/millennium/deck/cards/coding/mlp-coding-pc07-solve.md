---
id: mlp-coding-pc07-solve
node: coding.pc07
step: 1
type: qa
---
## Q
**按异位词分组的存储：题与解**｜编程轮

热身：判断只含 `()[]{}` 的字符串里括号是否合法。正题：设计一个存字符串的数据结构 `AnagramStore`，字母相同、顺序不同的词（异位词，anagram）归到同一组。要支持 `add(word)`、`group_of(word)`（返回同组所有词，按插入顺序）、`count(word)`、`remove(word)`（删掉恰好一个这个字符串）和 `most_common_group()`。

## A
**一句话思路。** 给每个词算一个规范键（canonical key）：异位词的键必须相同。把字符排序后拼回字符串当键，字典 `键 -> 词列表` 就是整个存储；增查都只算一次键。热身用栈：左括号入栈，右括号要和栈顶配对，最后栈必须空。

```python
def is_valid_parentheses(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:   # 右括号必须和栈顶配对
            return False
    return not stack                                  # 还有没配对的左括号也不合法

class AnagramStore:
    def __init__(self):
        self.groups = {}                  # 规范键 -> 词列表（插入顺序）

    def key(self, word):
        return "".join(sorted(word))      # O(L log L)，任意字符集都成立

    def add(self, word):
        self.groups.setdefault(self.key(word), []).append(word)

    def group_of(self, word):
        return list(self.groups.get(self.key(word), []))   # 没加过就返回空列表，不算错误

    def count(self, word):
        return len(self.group_of(word))

    def remove(self, word):
        k = self.key(word)
        group = self.groups.get(k)
        if not group or word not in group:
            raise ValueError(f"{word!r} not in store")     # 按字面字符串删，不是同组任意一个
        group.remove(word)                # 删最早插入的那个实例
        if not group:
            del self.groups[k]            # 组空了就删键，most_common 才不会看到空组

    def most_common_group(self):
        if not self.groups:
            return []
        # 并列时取键字典序最小的，结果不依赖插入顺序
        best = min(self.groups, key=lambda k: (-len(self.groups[k]), k))
        return list(self.groups[best])

s = AnagramStore()
for w in ["eat", "tea", "tan", "ate", "nat", "bat"]:
    s.add(w)
print(s.group_of("eat"), s.count("bat"), s.group_of("xyz"))   # ['eat','tea','ate'] 1 []
s.remove("eat")
print(s.most_common_group())                                  # ['tea', 'ate']
print(is_valid_parentheses("{[]}"), is_valid_parentheses("([)]"))   # True False
```

**复杂度。** `add`、`group_of`、`remove` 都是 O(L log L)（排序键，L 为词长）加上组内查找；`most_common_group` 是 O(G)（G 为组数）。内存约 O(N·L)。

**边写边讲。**
- "I group by a **canonical key**: the sorted characters, which works for any alphabet."
- "`remove` deletes the **exact string**, like handing back the record you inserted."
- "Ties go to the **smallest key**, so the answer doesn't depend on insertion order."
