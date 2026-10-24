---
id: tlc-serialize-and-deserialize-n-ary-tree-0-whole
node: a.serialize-and-deserialize-n-ary-tree
type: qa
---
## Q
**LC 428 序列化和反序列化 N 叉树**｜Hard · TikTok 高频

设计一个把 N 叉树（每个结点有任意多个孩子）转成字符串、再从字符串还原成原树的算法：`serialize(root)` 返回字符串，`deserialize(data)` 返回树，格式自定。算法必须**无状态**——不能用类成员、全局变量或静态变量保存状态。

约束：结点数在 `[0, 10^4]`，`0 <= Node.val <= 10^4`，N 叉树的高度 `<= 1000`。

例：`root = [1,null,3,2,4,null,5,6]`（层序格式：`1` 的孩子是 `3,2,4`，`3` 的孩子是 `5,6`）经 `serialize` 再 `deserialize` 后必须得到同一棵树；`root = []` 得到 `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先序遍历，每个结点写成「值 + 孩子个数」；读的时候用一个栈记录「当前链上每个结点还缺几个孩子」，缺的数到 0 就回到父结点。因为孩子个数已经写进去了，不需要任何分隔符或空标记。`O(n)`。

**识别。** 「序列化 / 反序列化」要的是**可逆编码**：解码时必须能无歧义地知道每个结点的孩子何时结束。二叉树常用「先序 + 空标记」，N 叉树没有固定的两个孩子位置，空标记会很啰嗦；改成**写出孩子个数**（或每组孩子后加结束标记）就够了。树高可达 `1000` 触及 Python 递归上限，要考虑迭代。

**推导。** 朴素想法：只记先序的值——`1→[2,3]` 与 `1→2→3` 都是 `1 2 3`，不可逆。补救：用括号 / 层序加分隔 `null`（题面给的格式）能用，但解析要处理嵌套或队列。更紧凑：先序时把每个结点写成 `值 孩子数`，整串是自描述的——读到一个结点，就知道后面紧跟着多少棵子树。解码时用栈保持「当前正在填的结点 + 还缺几个孩子」，缺的数为 0 就弹栈。递归写法最短，但高 1000 的链会触发 `RecursionError`，所以两边都用显式栈。

```python
class Codec:
    def serialize(self, root: Node | None) -> str:
        if root is None:
            return ""
        out: list[str] = []
        stack = [root]
        while stack:                              # 迭代先序，树高 1000 也不会爆递归栈
            node = stack.pop()
            out.append(f"{node.val} {len(node.children)}")   # 值 + 孩子个数
            stack.extend(reversed(node.children))            # 反着压，左孩子先弹出
        return " ".join(out)

    def deserialize(self, data: str) -> Node | None:
        if not data:
            return None
        tokens = map(int, data.split())
        root = Node(next(tokens), [])
        nodes, left = [root], [next(tokens)]      # 当前链上的结点，及各自还缺几个孩子
        while nodes:
            if left[-1] == 0:                     # 孩子收齐了，回到父结点
                nodes.pop()
                left.pop()
                continue
            left[-1] -= 1
            child = Node(next(tokens), [])
            nodes[-1].children.append(child)
            nodes.append(child)
            left.append(next(tokens))
        return root
```

运行：`serialize([1,null,3,2,4,null,5,6])` → `'1 3 3 2 5 0 6 0 2 0 4 0'`，`deserialize 再按层序输出` → `[1, None, 3, 2, 4, None, 5, 6]`，`示例 1 来回一趟后与原数组相同` → `True`，`root=[]` → `('', None)`，`高 1000 的单链` → `1000`。

**复杂度。** 时间 `O(n)`：每个结点序列化时出入栈一次、反序列化时被创建一次；空间 `O(n)`（输出字符串与结点本身），额外栈 `O(h)`。字符串长度约为 `2n` 个整数。

**易错点。**
- 只存先序的值：`1→[2,3]` 与 `1→2→3` 序列化出同一串 `1 2 3`，不可逆。加上孩子个数后分别是 `1 2 2 0 3 0` 与 `1 1 2 1 3 0`。
- 递归解码：高 1000 的单链会 `RecursionError`（Python 默认上限 1000）；上面两个方法都用显式栈。
- 空树：`serialize(None)` 要返回 `""`，`deserialize("")` 返回 `None`；`"".split()` 得 `[]`，直接 `next(tokens)` 会 `StopIteration`，必须先判空。
- 把状态放进 `self`（比如把迭代器存成成员）：题面明确禁止，两次调用之间会互相污染。上面所有状态都是局部变量。

**追问。**
- 想要人能读懂的格式：括号形式 `1(3(5 6) 2 4)`，更短也更可读，代价是解析要用栈匹配括号。
- 树巨大、不能一次拿到整个字符串：序列化改成生成器 `yield` 每个 token，反序列化从迭代器读——本方案的 `tokens` 迭代器已经是流式的。
- 结点值是任意字符串或可为负：用 `json.dumps` 序列化 `[val, [children...]]` 的嵌套列表最稳，注意深度上限；或给 token 加长度前缀。

**同模式。** LC 297 二叉树的序列化与反序列化、LC 449 序列化和反序列化二叉搜索树、LC 331 验证二叉树的前序序列化、LC 536 从字符串生成二叉树。
