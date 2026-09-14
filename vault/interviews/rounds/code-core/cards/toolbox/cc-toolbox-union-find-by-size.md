---
id: cc-toolbox-union-find-by-size
node: toolbox.union-find
type: cloze
---
Union by size attaches the root of the {{c1::smaller}} set under the root of the {{c2::larger}} one, so the tree depth never exceeds {{c3::log n}}; combined with path compression the amortized cost per operation is {{c4::α(n), effectively constant}}. Attaching blindly (`parent[rb] = ra`) is still *correct*, but a test that unions in a chain degrades the structure to {{c5::a linked list}} — and it also destroys the size bookkeeping you need to answer "how big is this component".

## zh
按大小合并会把{{c1::较小}}集合的根挂到{{c2::较大}}集合的根之下，于是树高永远不超过 {{c3::log n}}；再配合路径压缩，每次操作的摊销代价是 {{c4::α(n)，实际上等于常数}}。无脑挂接（`parent[rb] = ra`）仍然*正确*，但按链式合并的测试会把结构退化成 {{c5::一条链表}} —— 而且它还会毁掉你回答「这个连通块有多大」所需的大小记账。
