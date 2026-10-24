---
id: pl-abstraction-equality-hashing-unique-nan-equality
node: abstraction.equality-hashing
type: qa
step: 8
---
## Q
`NaN` 在 Java、Python、Rust 里的相等行为为什么各不相同？这说明了各语言怎样权衡标准与实用？

## A
IEEE 754 规定 `NaN != NaN`，包括与自己比较。这违反自反性，而哈希表、`List.contains`、排序都假设相等是等价关系。语言各自做了折中。

**Java**：`==` 遵守 IEEE，但 `Double.equals` 为了满足契约，把两个 `NaN` 视为相等，同时把 `0.0` 与 `-0.0` 视为不等：

```java
double d = Double.NaN;
(d == d)                                    // false
Double.valueOf(d).equals(d)                 // true
(0.0 == -0.0)                               // true
Double.valueOf(0.0).equals(-0.0)            // false
```

同一个类型上，`==` 与 `equals` 的答案相反。

**Python**：`==` 遵守 IEEE，但容器的 `in` 先用同一性判断，同一个 `NaN` 对象就算命中：

```python
nan = float("nan")
nan == nan                  # False
nan in [nan]                # True：先 is，再 ==
nan in [float("nan")]       # False：另一个对象
len({nan, nan})             # 1；len({float("nan"), float("nan")}) 是 2
```

**Rust**：干脆拒绝让 `f64` 实现 `Eq`，`HashMap<f64, _>` 编译失败，需要时用 `ordered-float` 之类的包装类型。

三种选择：Java 牺牲 `equals` 与 IEEE 的一致，换集合可用；Python 用同一性短路，造成「看起来矛盾」的结果；Rust 把问题挡在类型层，要求你明确表态。哲学上，Rust 倾向于**不让错误发生**，Java 倾向于**让常见用法可用**，Python 倾向于**实用、先快后修补**。
