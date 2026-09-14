# pc18 · Number Transformation Path：练的是"用不变量证可达性，再用有界 BFS 求最短"

> [!tldr]
> - 这题考的是：`add(+2)`/`sub(-2)`/`split(//2)` 三种操作下，从 `a` 到 `b` 的任意路径与最短路径；`split` 仅偶数可用是本 kit 声明的重建选择，Part 2 **(reconstructed)**
> - 三步套路：用奇偶性证明"何时不可达" → 直接构造一条可行路径 → 用可行路径的长度证明有界 BFS 的上界足够
> - 最值得带走的一个模式：**遇到数值可能无界的隐式图，先找一个不变量证明可达性边界，再给一个可论证的有限上界做有界 BFS，而不是无脑套无界搜索**

## 1. 题目在说什么（人话版）

从正整数 `a` 出发，每步可以 `+2`、`-2`（不能小于 1）、或者在偶数时 `//2`。求一条从 `a` 到 `b`
的路径（Part 1 任意路径，Part 2 最短路径），走不到就报告不可达。

小例子：
```
transform(4, 7)          -> [4, 6, 8, 10, 12, 14, 7]   # 偶→奇：平移到 2*7=14 再 split 一次
transform(7, 4)          -> None                        # 奇→偶：永远碰不到偶数
shortest_transform(4, 7) -> [4, 6, 3, 5, 7]              # 4 步，比先平移到 14 短得多
```

## 2. 读题：把文字变成模型

- **实体**：正整数状态、三种操作、隐式图（节点是数，边是操作）。
- **输入**：一对正整数 `a, b`。
- **输出**：路径（列表）或不可达标记。
- **状态**：BFS 需要访问过的节点集合 `prev` 与前驱指针。
- **一句话建模**：这是一个 **"状态空间理论上无界，但可达性由一个不变量（奇偶性）直接决定"** 的
  隐式图问题。

> [!note] 为什么先证不变量，而不是直接上 BFS
> `add`/`sub` 永远不改变奇偶性，只有 `split` 能改变奇偶性，而 `split` 只能从偶数出发。所以奇数
> `a` 永远碰不到任何偶数——`b` 是偶数就必然不可达，根本不需要跑一次搜索才知道。证明可达性之后，
> 再用"任意一条可行路径的最大中间值"当作有界 BFS 的搜索上界，这个上界是可以论证的，不是拍脑袋。

## 3. 下笔顺序

1. **问清**：`split` 是不是只对偶数生效？（预览没说，这是本题唯一需要声明的重建选择——如果奇数
   也能 `split`，则任意 `a,b` 都连通，"不可达"这个分支永远不会触发，与题面矛盾。）
2. **Part 1 最小可用**：`a==b` 直接返回 `[a]`；奇 `a` 偶 `b` 直接判 `None`；同奇偶直接平移；
   偶 `a` 奇 `b` 平移到 `2b` 再 `split` 一次落到 `b`。
3. **Part 2 叠加**：复用同样的不可达判定；BFS 时给一个有限上界 `2*max(a,b)+4`（Part 1 的构造已
   经证明最优解不需要探索比这更远的地方），队列 BFS 求最短路并回溯路径。
4. **收尾**：`split` 降到 `1` 之后不能再 `split`（奇）也不能再 `sub`（变 0）；`a<1`/`b<1` 报错。

## 4. 代码怎么组织

```
_check(a, b)                          # 正整数校验，两个 Part 共用
transform(a, b)                       # Part 1：奇偶推理 + 直接构造
shortest_transform(a, b)              # Part 2：同样的不可达判定 + 有界 BFS
part1 / part2(lines)                  # 命令行驱动，IMPOSSIBLE 是唯一的失败态输出
```
两个函数的"判不可达"完全相同，抽成同一段代码（本文用同一句奇偶判断）；差异只在"怎么构造路径"。

## 5. 核心代码（骨架）

```python
def transform(a, b):
    if a == b:
        return [a]
    if a % 2 == 1 and b % 2 == 0:
        return None                      # 奇 a 永远碰不到偶数
    path = [a]
    def walk(start, target):
        step = 2 if target > start else -2
        cur = start
        while cur != target:
            cur += step; path.append(cur)
    if a % 2 == b % 2:
        walk(a, b)                       # 同奇偶：直接平移
    else:
        walk(a, 2 * b); path.append(b)   # 偶→奇：平移到 2b 再 split 一次
    return path

def shortest_transform(a, b):
    if a == b: return [a]
    if a % 2 == 1 and b % 2 == 0: return None
    bound = 2 * max(a, b) + 4            # Part 1 构造给出的可行解证明这个上界够用
    prev, q = {a: None}, deque([a])
    while q:
        cur = q.popleft()
        if cur == b: break
        neighbors = [cur + 2] if cur + 2 <= bound else []
        if cur - 2 >= 1: neighbors.append(cur - 2)
        if cur % 2 == 0: neighbors.append(cur // 2)
        for nxt in neighbors:
            if nxt not in prev:
                prev[nxt] = cur; q.append(nxt)
    path, cur = [], b
    while cur is not None:
        path.append(cur); cur = prev[cur]
    return path[::-1]
```

## 6. 面试里怎么说

- 开始前：「我先确认一下：`split` 是不是只能对偶数使用？如果奇数也能切，这题就不会有真正的
  '不可达'。」
- 写 Part 1 时：「`add`/`sub` 不改变奇偶性，只有 `split` 能改，而它只从偶数出发——所以奇数 `a`
  永远走不到偶数集合，`b` 是偶数就一定不可达，我不需要搜索就能判定。」
- 到 Part 2 时：「数值理论上无界，不能无界 BFS；但 Part 1 的构造已经给出一条可行路径，它的最大
  中间值是 `2*max(a,b)`，所以最优解不会跑到比这更远的地方，我给 BFS 一个 `2*max(a,b)+4` 的
  有限上界。」
- 交付时：「样例过了；如果换成 `split` 对奇数也生效的版本，我会重新论证一遍——那种情况下题目就
  不会有'返回 None'这个分支了。」

## 7. 常见跑偏

- 一上来就写无界 BFS（`while True` 扩展队列），数值可以无限增长，程序永远不会因为"不可达"而
  停下来。
- 把"不可达"完全交给搜索去发现，而不是先用奇偶性直接判断——既慢又容易在边界值上出错（比如
  `split` 降到 1 之后的分支）。
- BFS 上界设置得比"已知可行解的最大中间值"还小，漏掉真正的最短路径（比如只设 `max(a,b)` 而不
  留一点余量）。

## 8. 同族题 / 延伸

- 与 `pc06`（Happy Number，隐式链表判环）同样是"把一个数值变换序列建模成隐式图"的考法，但 pc18
  考的是可达性证明 + 有界搜索，pc06 考的是判环。
- 与 `pc04`（Wiki 最短点击路径）同样是"任意路径 → 最短路径"的递进结构，但 pc18 的图是隐式且
  可能无界的，需要先证明有限的搜索边界。
- 练习命令：`python3 loop/mock.py start pc18`
