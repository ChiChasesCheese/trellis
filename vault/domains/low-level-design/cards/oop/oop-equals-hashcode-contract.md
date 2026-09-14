---
id: oop-equals-hashcode-contract
node: oop.values
type: qa
---
## Q
You override `equals` on `Money` but not `hashCode`. `set.add(new Money(5, USD))` then `set.contains(new Money(5, USD))` returns **false**. Explain, and state the contract that was broken.

## A
`HashSet` looks in the bucket chosen by `hashCode` first. Two equal objects with different identity hash codes land in different buckets, so `equals` is never even called.

Contract: **equal ⇒ equal hash codes** (the converse is not required — collisions are legal, just slower). Also required: reflexive, symmetric, transitive, consistent, and `x.equals(null) == false`.

Two practical consequences:
- **Symmetry with subclasses**: `instanceof` in a superclass `equals` lets `sub.equals(super)` disagree with `super.equals(sub)`; `getClass() !=` avoids that but forbids subclass equality entirely.
- Only fields that never change may participate — otherwise a mutation strands the object in the wrong bucket.

## Q zh
你给 `Money` 重写了 `equals` 但没重写 `hashCode`。`set.add(new Money(5, USD))` 之后 `set.contains(new Money(5, USD))` 返回 **false**。解释原因，并说出被破坏的是哪条契约。

## A zh
`HashSet` 先按 `hashCode` 选桶。两个相等的对象如果 identity hash code 不同，就落到不同的桶里，于是 `equals` 根本没被调用过。

契约：**相等 ⇒ hash code 相等**（反向不要求 —— 碰撞是合法的，只是更慢）。另外还要求：自反、对称、传递、一致，以及 `x.equals(null) == false`。

两个实际后果：
- **子类下的对称性**：父类 `equals` 里用 `instanceof`，会让 `sub.equals(super)` 和 `super.equals(sub)` 结果不一致；改用 `getClass() !=` 能避免，但也就彻底禁止了子类之间相等。
- 只有永不改变的字段才能参与比较 —— 否则一次修改就会把对象留在错误的桶里。
