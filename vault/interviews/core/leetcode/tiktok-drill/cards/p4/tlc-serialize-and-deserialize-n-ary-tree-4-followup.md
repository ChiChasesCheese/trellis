---
id: tlc-serialize-and-deserialize-n-ary-tree-4-followup
node: p4.serialize-and-deserialize-n-ary-tree
type: qa
step: 4
---
## Q
**LC 428 序列化和反序列化 N 叉树**｜追问

面试官接着问：（1）值可能是任意字符串、负数怎么办？（2）树大到字符串放不下，要流式处理？（3）把 `serialize` 的结果压到最短，或要人能读懂的格式？

## A
1. **任意值**：空格分隔的整数只适合此处。通用做法是把每个结点编码为 `json.dumps([val, [child, ...]])` 的嵌套结构，由 JSON 处理转义；或给每个 token 加长度前缀 `len:payload`。嵌套极深时 `json.dumps` 会触到递归深度限制（树高 1000 的嵌套还能过，更深就 `RecursionError`），要先问清树高。
2. **流式**：序列化写成生成器，每个结点 `yield` 两个 token，调用方边生成边写文件 / 网络；反序列化的 `tokens` 本来就是迭代器，传入 `iter(file_tokens)` 即可，空间 `O(h)`（不含结果树）。
3. **更短 / 更可读**：更短——叶子很多时，用括号省去叶子的 `0`（`1 3 3 2 5 0 6 0 2 0 4 0` 变成 `1(3(5 6) 2 4)`）；更可读——括号形式；代价是解析逻辑比计数版复杂。


**Python 提醒**：`Node(val, children=[])` 这种可变默认参数会让所有结点共享同一个列表；LeetCode 的定义是 `children=None` 后再换成新列表。自己建结点时始终显式传 `[]`。
