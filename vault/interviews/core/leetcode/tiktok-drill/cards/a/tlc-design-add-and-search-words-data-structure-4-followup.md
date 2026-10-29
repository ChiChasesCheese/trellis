---
id: tlc-design-add-and-search-words-data-structure-4-followup
node: a.design-add-and-search-words-data-structure
type: qa
step: 4
---
## Q
**LC 211 添加与搜索单词 - 数据结构设计**｜追问

面试官接着问：（1）不用递归，能怎么写 `search`？（2）要支持删除单词？（3）通配符 `'*'` 匹配任意长度呢？

## A
1. **不用递归。** 按层推进一个"当前结点集合"，遇到 `'.'` 就把所有孩子加入下一层：

```python
def search_bfs(root: dict[str, dict], word: str) -> bool:
    level = [root]
    for ch in word:
        nxt: list[dict[str, dict]] = []
        for node in level:
            if ch == ".":
                nxt.extend(child for key, child in node.items() if key != "$")
            elif ch in node:
                nxt.append(node[ch])
        if not nxt:                              # 没有任何分支能继续：提前失败
            return False
        level = nxt
    return any("$" in node for node in level)
```

时间同样最坏 `O(总字符数)`，没有递归栈。
2. **删除单词。** 先沿路径走到末尾去掉 `"$"`；再从末尾往回，若某结点没有任何孩子且不是别的单词的结尾，就从父结点里删掉，直到遇到有其他分支的结点。
3. **`'*'` 匹配任意长度。** 单纯 DFS 会重复展开；改成带记忆的递归 `(结点, 位置)`，或者回到动态规划（类似 LC 10 正则表达式匹配），因为同一状态会被多条路径反复到达。

**Python 提醒**：递归写法每层都是一次函数调用，Python 默认递归上限 1000，单词长度 `<= 25` 完全安全；但如果长度放宽到上万，就必须用上面的层推进写法。
