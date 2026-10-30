---
id: uth-python-classes-mro-3-c3
node: python.classes-mro
type: qa
step: 3
---
## Q
**C3 线性化：MRO 怎么排出来**｜Python · CPython 3.14

为什么 `D(B, C)` 排出的是 `D B C A object`？什么样的继承写法会让 Python 在建类时直接报错？

## A
**背景。** 排顺序要同时满足两条常识：子类一定排在父类前面；`class D(B, C)` 里写的先后顺序要保持，`B` 在 `C` 前。深度优先会违反第一条（`A` 排到了 `C` 前面）。Python 2.3 起改用 C3 线性化（C3 linearization）。

**结构。** 把每个父类自己的 MRO 和父类名单本身当成几张清单，反复做合并：看第一张清单的队头，如果它不在任何清单「队头之后的部分」里，就放进结果并从所有清单划掉；否则换下一张清单的队头试。以 `D(B, C)` 为例，三张清单是 `[B, A, object]`、`[C, A, object]`、`[B, C]`：

| 步 | 候选 | 能放吗 | 结果 |
|---|---|---|---|
| 1 | B | 可以 | D B |
| 2 | A | 不行，在 `[C, A, object]` 的后半 | 改试 C |
| 3 | C | 可以 | D B C |
| 4 | A | 可以 | D B C A |
| 5 | object | 可以 | D B C A object |

**细节。**

- 顺序矛盾时建类直接失败。实测 `P(X, Y)`、`Q(Y, X)` 再写 `R(P, Q)`，得到 `TypeError: Cannot create a consistent method resolution order (MRO) for bases X, Y`。
- MRO 在建类时算完，之后固定在 `__mro__`。

**为什么。** C3 保证单调性（monotonic）：父类里已经有的先后关系，到子类里不会被颠倒。矛盾时宁可报错，也不悄悄选一个。

**坑。** 把 `object` 写在别的基类前面，例如 `class B(object, X)`，实测同样报 `Cannot create a consistent method resolution order`。

**对应 LeetCode：** 无直接对应的题
