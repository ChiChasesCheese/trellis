---
id: leetcode-c-endlesscheng-luu0kb-functional-graph-and-binary-lifting-template
node: graphs-traversal.functional-graph-and-binary-lifting
type: cloze
anki: 1787272459878
tags: [concept-cloze, leetcode, recall, template]
---
查询 k 步跳转时，依次处理 k 的 {{c1::二进制置位}}。

```
def build_jump(next_node, levels):
    up = [next_node[:]]
    for _ in range(1, levels):
        previous = up[-1]
        up.append([previous[previous[node]] for node in range(len(next_node))])
    return up

def jump(up, node, steps):
    bit = 0
    while steps:
        if steps & 1:
            node = up[bit][node]
        steps >>= 1
        bit += 1
    return node
```

**Evidence**

三、图论：倍增、基环树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.14%20-%20%E5%9F%BA%E7%8E%AF%E6%A0%91%E4%B8%8E%E5%80%8D%E5%A2%9E)
