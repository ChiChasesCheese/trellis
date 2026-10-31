---
id: tlc-serialize-and-deserialize-n-ary-tree-0-whole
node: p2.serialize-and-deserialize-n-ary-tree
type: qa
---
## Q
**LC 428 序列化和反序列化 N 叉树**｜Hard · LC TikTok 近 3 个月热度 62/100（全时段 38） · CodeTop 国内累计 1 次 · 最近 2021-08-10（国内 CodeTop）

设计一个把 N 叉树（每个结点有任意多个孩子）转成字符串、再从字符串还原成原树的算法：`serialize(root)` 返回字符串，`deserialize(data)` 返回树，格式自定。算法必须**无状态**——不能用类成员、全局变量或静态变量保存状态。

约束：结点数在 `[0, 10^4]`，`0 <= Node.val <= 10^4`，N 叉树的高度 `<= 1000`。

例：`root = [1,null,3,2,4,null,5,6]`（层序格式：`1` 的孩子是 `3,2,4`，`3` 的孩子是 `5,6`）经 `serialize` 再 `deserialize` 后必须得到同一棵树；`root = []` 得到 `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先序遍历，每个结点写成「值 + 孩子个数」；读的时候先读值和个数，再递归建那么多棵子树。因为孩子个数已经写进去了，不需要任何分隔符或空标记。`O(n)`。

**识别。** 「序列化 / 反序列化」要的是**可逆编码**：解码时必须能无歧义地知道每个结点的孩子何时结束。二叉树常用「先序 + 空标记」，N 叉树没有固定的两个孩子位置，空标记会很啰嗦；改成**写出孩子个数**（或每组孩子后加结束标记）就够了。树高可达 `1000`，递归深度正好触及 Python 默认的递归上限，要留意。

**推导。** 朴素想法：只记先序的值——`1→[2,3]` 与 `1→2→3` 都是 `1 2 3`，不可逆。补救：用括号 / 层序加分隔 `null`（题面给的格式）能用，但解析要处理嵌套或队列。更紧凑：先序时把每个结点写成 `值 孩子数`，整串是自描述的——读到一个结点，就知道后面紧跟着多少棵子树。解码就是读到孩子数 `c`，递归建 `c` 棵子树。

**简单解法。** 借 `json`：每个结点写成嵌套列表 `[值, [孩子...]]`，`dumps` / `loads` 各一行，再递归还原成结点。

```python
import json

class Codec:
    def serialize(self, root: Node | None) -> str:
        def to_list(node: Node) -> list:
            return [node.val, [to_list(c) for c in node.children]]   # 嵌套列表本身就带结构，不需要孩子个数

        return json.dumps(to_list(root) if root else [])   # 空树写成 []

    def deserialize(self, data: str) -> Node | None:
        def build(arr: list) -> Node:
            return Node(arr[0], [build(c) for c in arr[1]])   # 与 to_list 一一对应

        arr = json.loads(data)
        return build(arr) if arr else None                 # [] 对应空树
```

时间 `O(n)`、空间 `O(n)`；输出体积约是主解法的 2 倍，树高 `1000` 时也会碰到递归上限，只适合当开场答案。

最优解：

```python
class Codec:
    def serialize(self, root: Node | None) -> str:
        out: list[str] = []

        def dfs(node: Node) -> None:
            out.append(f"{node.val} {len(node.children)}")   # 值 + 孩子个数
            for child in node.children:
                dfs(child)

        if root:
            dfs(root)
        return " ".join(out)

    def deserialize(self, data: str) -> Node | None:
        if not data:                              # 空树："".split() 是 []，必须先判空
            return None
        tokens = map(int, data.split())           # 一次性迭代器，递归调用之间共享读到哪了

        def build() -> Node:
            node = Node(next(tokens), [])
            for _ in range(next(tokens)):         # 读到几个孩子，就递归建几棵子树
                node.children.append(build())
            return node

        return build()
```

运行：`serialize([1,null,3,2,4,null,5,6])` → `'1 3 3 2 5 0 6 0 2 0 4 0'`，`deserialize 再按层序输出` → `[1, None, 3, 2, 4, None, 5, 6]`，`示例 1 来回一趟后与原数组相同` → `True`，`root=[]` → `('', None)`，`高 1000 的单链` 在默认递归上限下抛 `RecursionError`，调高上限后往返一致。

**复杂度。** 时间 `O(n)`：每个结点序列化时被访问一次、反序列化时被创建一次；空间 `O(n)`（输出字符串与结点本身），额外递归栈 `O(h)`。字符串长度约为 `2n` 个整数。

**拓展优化。**
- 层序（BFS）版：同样是「值 + 孩子个数」，按层序输出，读时用队列记住谁还缺孩子；完全不递归，树高 `1000` 也没问题。

```python
from collections import deque

class CodecBFS:
    def serialize(self, root: Node | None) -> str:
        if root is None:
            return ""
        out: list[str] = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            out += [str(node.val), str(len(node.children))]   # 值 + 孩子个数
            queue.extend(node.children)
        return " ".join(out)

    def deserialize(self, data: str) -> Node | None:
        if not data:
            return None
        tokens = map(int, data.split())
        root = Node(next(tokens), [])
        queue = deque([(root, next(tokens))])      # (结点, 它还要读几个孩子)；层序读，与序列化的入队顺序一致
        while queue:
            node, cnt = queue.popleft()
            for _ in range(cnt):                   # 孩子在输出里的顺序和入队顺序一致
                child = Node(next(tokens), [])
                node.children.append(child)
                queue.append((child, next(tokens)))
        return root
```

**易错点。**
- 只存先序的值：`1→[2,3]` 与 `1→2→3` 序列化出同一串 `1 2 3`，不可逆。加上孩子个数后分别是 `1 2 2 0 3 0` 与 `1 1 2 1 3 0`。
- 递归深度：高 1000 的单链需要约 1000 层递归，CPython 默认递归上限约 1000，序列化和反序列化都会抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成显式栈（见追问）。
- 空树：`serialize(None)` 要返回 `""`，`deserialize("")` 返回 `None`；`"".split()` 得 `[]`，直接 `next(tokens)` 会 `StopIteration`，必须先判空。
- 把状态放进 `self`（比如把迭代器存成成员）：题面明确禁止，两次调用之间会互相污染。上面所有状态都是局部变量（`out`、`tokens` 在每次调用里新建）。

**追问。**
- 树高 1000 的链递归爆栈：两边都改成显式栈。序列化用栈做先序，反着压孩子使左孩子先出；反序列化用「结点栈 + 还缺几个孩子」的并行栈还原，缺口为 0 就弹栈：
```python
class CodecStack:
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
- 想要人能读懂的格式：括号形式 `1(3(5 6) 2 4)`，更短也更可读，代价是解析要用栈匹配括号。
- 树巨大、不能一次拿到整个字符串：序列化改成生成器 `yield` 每个 token，反序列化从迭代器读——本方案的 `tokens` 迭代器已经是流式的。
- 结点值是任意字符串或可为负：用 `json.dumps` 序列化 `[val, [children...]]` 的嵌套列表最稳，注意深度上限；或给 token 加长度前缀。

**同模式。** LC 297 二叉树的序列化与反序列化、LC 449 序列化和反序列化二叉搜索树、LC 331 验证二叉树的前序序列化、LC 536 从字符串生成二叉树。
