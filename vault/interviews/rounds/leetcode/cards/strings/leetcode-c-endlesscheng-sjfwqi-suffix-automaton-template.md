---
id: leetcode-c-endlesscheng-sjfwqi-suffix-automaton-template
node: strings.suffix-automaton
type: cloze
anki: 1787272449681
tags: [concept-cloze, leetcode, recall, template]
---
后缀自动机追加字符后若 len[p]+1 不等于 len[q]，必须创建 {{c1::clone 状态}} 重定向转移。

```
def build_suffix_automaton(s):
    nexts = [{}]
    link = [-1]
    length = [0]
    last = 0
    for ch in s:
        cur = len(nexts)
        nexts.append({})
        link.append(0)
        length.append(length[last] + 1)
        p = last
        while p != -1 and ch not in nexts[p]:
            nexts[p][ch] = cur
            p = link[p]
        if p == -1:
            link[cur] = 0
        else:
            q = nexts[p][ch]
            if length[p] + 1 == length[q]:
                link[cur] = q
            else:
                clone = len(nexts)
                nexts.append(nexts[q].copy())
                link.append(link[q])
                length.append(length[p] + 1)
                while p != -1 and nexts[p].get(ch) == q:
                    nexts[p][ch] = clone
                    p = link[p]
                link[q] = link[cur] = clone
        last = cur
    return nexts, link, length
```

**Evidence**

八、后缀数组/后缀自动机

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.09%20-%20%E5%90%8E%E7%BC%80%E8%87%AA%E5%8A%A8%E6%9C%BA%20%28SAM%29)
