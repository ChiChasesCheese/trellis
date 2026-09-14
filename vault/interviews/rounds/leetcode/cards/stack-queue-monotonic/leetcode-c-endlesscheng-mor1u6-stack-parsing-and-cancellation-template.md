---
id: leetcode-c-endlesscheng-mor1u6-stack-parsing-and-cancellation-template
node: stack-queue-monotonic.stack-parsing-and-cancellation
type: cloze
anki: 1787272420203
tags: [concept-cloze, leetcode, recall, template]
---
括号匹配遇到右括号时，必须从栈顶 {{c1::弹出并比较对应左括号}}。

```
def is_valid_parentheses(s):
    match = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif not stack or stack.pop() != match[ch]:
            return False
    return not stack
```

**Evidence**

§3.4 合法括号字符串（RBS）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.08%20-%20%E6%A0%88%E7%9A%84%E5%8C%B9%E9%85%8D%E3%80%81%E6%B6%88%E9%99%A4%E4%B8%8E%E8%A1%A8%E8%BE%BE%E5%BC%8F%E8%A7%A3%E6%9E%90)
