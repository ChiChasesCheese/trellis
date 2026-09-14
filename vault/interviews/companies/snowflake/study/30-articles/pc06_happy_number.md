# pc06 · Happy Number：练的是"迭代一个函数 = 走一条隐式链表，判环不用额外空间"

> [!tldr]
> - Part 1、Part 2 是 2026 夏一手原题与原追问（"先 O(n) 再被要求 O(1)"）；**Part 3 任意进制与幂次、报告环信息是 (reconstructed)**
> - 这题考的是：各位数字平方和反复迭代，会不会到 1
> - 三步套路：集合记录见过的值 → Floyd 快慢指针 → 相遇后绕环一圈量长度
> - 最值得带走的一个模式：**任何"反复套一个函数"的序列都是一条隐式链表**，判环、找环长、找入口都能用快慢指针在 O(1) 空间完成

## 1. 题目在说什么（人话版）

把一个正整数的每位数字平方加起来，得到新数，再重复。能到 1 就是 happy，否则会永远在一个圈里转（十进制下那个圈是 `4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4`）。

```
19 → 1+81=82 → 64+4=68 → 36+64=100 → 1   happy
2  → 4 → 16 → … → 20 → 4 → …            不 happy
```

## 2. 读题：把文字变成模型

- **状态**：当前数；Part 1 加一个见过的集合；Part 2 两个指针。
- **为什么一定进环**：d 位数的下一步至多 81·d，大数迅速变小，之后在有限范围里转——有限状态上的确定性迭代必然进环。
- **一句话建模**：这是一个 **"隐式链表判环"** 问题，环是否是自反点 1 决定答案。

## 3. 下笔顺序

1. **先说为什么一定终止**（面试官经常先问这个）。
2. **Part 1**：`seen` 集合，循环直到 1 或重复。
3. **被要求 O(1) 时**：说"这是链表判环" → Floyd：`slow = n`、`fast = f(n)`，慢一步快两步，直到 `fast == 1` 或相遇。
4. **Part 3**：相遇点一定在环上；从它出发再绕一圈计数，顺便记最小值。`f` 参数化为 `(base, power)`。
5. **收尾**：`n = 1`、非法输入、极大 n。

## 4. 代码怎么组织

```
_step(n, base=10, power=2)     # 唯一的"下一个"函数
is_happy_set(n)                # Part 1
is_happy_floyd(n)              # Part 2：不建任何容器
cycle_info(n, base, power)     # Part 3：Floyd 找环内一点 + 绕环计数
part1..part3
```

## 5. 核心代码骨架

```python
def _step(n, base=10, power=2):
    t = 0
    while n:
        n, d = divmod(n, base)
        t += d ** power
    return t

def is_happy_floyd(n):
    slow, fast = n, _step(n)
    while fast != 1 and slow != fast:
        slow = _step(slow)
        fast = _step(_step(fast))
    return fast == 1

def cycle_info(n, base=10, power=2):
    slow, fast = _step(n, base, power), _step(_step(n, base, power), base, power)
    while slow != fast:
        slow = _step(slow, base, power)
        fast = _step(_step(fast, base, power), base, power)
    length, smallest, cur = 1, slow, _step(slow, base, power)
    while cur != slow:
        length += 1; smallest = min(smallest, cur); cur = _step(cur, base, power)
    return length, smallest
```

## 6. 每个 part 叠加什么

| Part | 空间 | 改动 |
|---|---|---|
| 1 | O(环 + 尾巴) | 集合 |
| 2 | O(1) | 快慢指针 |
| 3 | O(1) | 参数化 `f` + 相遇后绕环计数 |

## 7. 常见坑

- Part 2 偷偷用了 set / dict（测试会把模块里的 `set`、`dict` 换成报错函数）。
- 快指针初始化和慢指针相同，第一轮就判定相遇。
- 用字符串拆位（`str(n)`）——能过，但面试官会问为什么不用 `divmod`，而且 Part 3 非十进制时不通用。
- `n ≤ 0` 没校验。

## 8. 追问怎么接

1. **为什么快慢指针一定相遇？** 两者都进环后，快指针每步相对慢指针靠近 1，环长有限。
2. **怎么找环入口？** 相遇后一个指针回到起点，两者同速走，再次相遇就是入口。
3. **有没有更快的特判？** 十进制平方和版本，不 happy 必经过 4；"走到 1 或 4 就停"——但依赖具体函数，先讲 Floyd 再提。
4. **Brent 算法？** 以 2 的幂次移动"传送点"，函数调用更少，渐近相同。

## 9. 自测清单

- [ ] 30 秒说清为什么一定进环
- [ ] 不看代码写 Floyd 版本
- [ ] 说出找环入口的方法

## 相关题与 skills

S08 复杂度再压一档 · S05 判环。相关：LC 141/142 链表判环、`sd09` 密码存储（同一场面试的系统设计题）。
