---
id: cc-algorithms-backtracking-undo
node: algorithms.backtracking
type: qa
---
## Q
The recursion works for the first branch and returns garbage after that. What is the usual cause?

## A
**A mutation that is not undone symmetrically.** Every change made before recursing must be reverted after it, in reverse order, on *every* exit path.

```python
path.append(x)
saved, arr[j] = arr[j], arr[j] + delta
dfs(i + 1)
arr[j] = saved                      # exact mirror
path.pop()
```

- **Save the old value** rather than "subtracting back". Subtraction reintroduces a bug the moment the transition is not exactly invertible (clamping, `max`, a set insert that was already present).
- An early `return` inside the branch skips the undo. Use a single exit point, or restore in a `finally`.
- Record the best as a **copy** (`best = path[:]`); otherwise `best` aliases the list you are about to mutate and ends up empty.
- The symmetry is checkable: for every mutation before the recursive call there must be exactly one restore after it, and they should read as a mirrored pair.

## Q zh
递归在第一个分支上是对的，之后返回的都是垃圾。通常是什么原因？

## A zh
**某个修改没有对称地撤销。** 递归前做的每一处改动，都必须在递归后按相反顺序、在*每一条*出口路径上还原。

```python
path.append(x)
saved, arr[j] = arr[j], arr[j] + delta
dfs(i + 1)
arr[j] = saved                      # 精确镜像
path.pop()
```

- **保存旧值**，而不是「再减回去」。一旦转移不是严格可逆的（有钳位、有 `max`、往集合里插入了本已存在的元素），减法就会带回 bug。
- 分支内部的提前 `return` 会跳过撤销。使用单一出口，或在 `finally` 里还原。
- 记录最优解时要存**副本**（`best = path[:]`）；否则 `best` 只是你即将修改的那个列表的别名，最后会变成空的。
- 这种对称性是可检查的：递归调用前的每一处修改，之后都必须恰有一处还原，两者读起来应当是一对镜像。
