---
slug: amazon-hierarchical-document-search
---
## Q
**层级文档搜索**｜Medium

文档按树组织，节点是 `{"name": str, "children": [...]}`。给关键词 `q`，按先序返回所有名称包含 `q`（不分大小写）的节点完整路径，如 `"root/docs/api"`。

## A
**一句话。** 自顶向下 DFS，把父路径当参数带下去，节点命中就记下自己的完整路径，再递归孩子。

```python
def search(root, q):
    q, out = q.lower(), []

    def dfs(node, path):
        name = node["name"]
        path = f"{path}/{name}" if path else name
        if q in name.lower():
            out.append(path)  # 先序：父在子前
        for child in node.get("children", []):
            dfs(child, path)

    dfs(root, "")
    return out
```

**复杂度。** 时间 `O(所有路径长度之和)`，空间 `O(树高)`。

**易错点。**
- 路径放共享列表却不回溯：`append` 后忘了 `pop`，兄弟节点的路径串在一起。
- 树很深时递归爆栈：改显式栈压 `(节点, 路径)`，孩子逆序入栈才保持先序。

**追问。**
- 查询很频繁？：按谓词建索引：名称精确匹配用哈希倒排，路径前缀用 trie，正文用倒排索引；子树移动时整棵子树的路径索引都要改。
- 父节点命中就不展开子树？：命中后直接 `return`，剪掉整棵子树。
- 有权限继承？：DFS 把「可见」状态往下传，不可见的子树整棵跳过。

**同模式。** LC 112 路径总和、LC 257 二叉树的所有路径、LC 1166 设计文件系统、LC 588 设计内存文件系统
