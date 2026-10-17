# 08 · 链表（Linked list）

> 本讲覆盖：LC 206 Reverse Linked List · 21 Merge Two Sorted Lists · 2 Add Two Numbers · 138 Copy List with Random Pointer · 25 Reverse Nodes in k-Group（Hard）
> 前置：Python 中「变量是对象的引用」这一点（本讲会讲）。第 05 讲的 LC 23 也用到了本讲的 `ListNode`。
> 读完你应该能：(1) 在脑中（或纸上）画出指针的变化；(2) 用 dummy 头节点消灭「头节点特殊情况」；(3) 写出 `prev / cur / nxt` 三指针反转，并推广到分段反转。

## 1. 这个模式是什么，为什么存在

### 1.1 链表是什么（从零讲）

数组把元素放在一段连续内存里，按下标 O(1) 访问，但在中间插入 / 删除要搬动后面所有元素：O(n)。
**链表**把每个元素放在一个独立的**节点（node）**里，节点保存值和指向下一个节点的引用 `next`：

```text
head -> [1| ] -> [2| ] -> [3| ] -> None
```

- 在已知节点后面插入 / 删除：只改 1–2 个 `next`，O(1)。
- 按位置访问：必须从头走，O(n)。
- Python 里变量保存的是**对象的引用**，`a.next = b` 只是让 `a.next` 也指向 `b` 所指的对象，不会复制节点。

### 1.2 从最笨的解法开始

LC 206 反转链表。最笨的做法：遍历一遍把值放进数组，再倒着创建一条新链表。O(n) 时间，O(n) 额外空间，并且做了不必要的拷贝。面试官的追问通常是「**能不能 O(1) 空间、原地**？」

### 1.3 慢在哪里 / 难在哪里

链表题的难点几乎不在复杂度，而在**指针操作的顺序**：你一旦执行了 `cur.next = prev`，原来 `cur.next` 指向的「剩下的链表」就**丢了**——没有任何变量还指着它。

> 因果链：改指针会丢信息 → 改之前必须先把要用的信息存起来（`nxt = cur.next`）→ 于是有了 `prev / cur / nxt` 三指针的固定套路。头节点可能被删除或替换 → 引入 **dummy 头节点**，让每个真实节点都「有前驱」，不再需要对头节点特殊处理。

### 1.4 常用工具

| 工具 | 解决什么 |
|---|---|
| dummy 头节点（哨兵） | 结果链表的头未知（合并、删除、插入） |
| `prev / cur / nxt` | 就地反转 |
| 快慢指针（fast / slow） | 找中点、判环、找倒数第 k 个 |
| 哈希表 `旧节点 → 新节点` | 复制带随机指针的链表 |
| 先画图再写代码 | 指针题的 90% |

## 2. 模板与逐行讲解

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build(values):
    dummy = tail = ListNode()
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_list(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out

# Template L1: dummy head -- the head might change or not exist; a dummy makes every node "have a previous"
def remove_value(head, target):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next:
        if prev.next.val == target:
            prev.next = prev.next.next            # unlink; do NOT advance prev (the next one may match too)
        else:
            prev = prev.next
    return dummy.next

# Template L2: fast/slow pointers (middle, cycle detection)
def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow                                    # 2nd middle when the length is even

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:                           # the fast runner lapped the slow one
            return True
    return False

assert to_list(remove_value(build([1, 2, 2, 3, 2]), 2)) == [1, 3]
assert middle(build([1, 2, 3, 4, 5])).val == 3 and middle(build([1, 2, 3, 4])).val == 3
loop = build([1, 2, 3])
loop.next.next.next = loop.next
assert has_cycle(loop) and not has_cycle(build([1, 2, 3]))
```

逐行讲解：

1. `build` / `to_list`：测试辅助函数，平时面试里你也会先写这两个来验证；`build` 用 dummy + tail 追加，正是模板 L1 的用法。
2. `remove_value`：`dummy = ListNode(0, head)`，`prev = dummy`。**我们总是看 `prev.next`**，所以头节点被删除也和别的节点没区别。
3. 删除时**不移动 `prev`**：`prev.next = prev.next.next` 之后，新的 `prev.next` 可能也要删除（连续相同值）。只有不删除时才前进。
4. `middle`：`fast` 每次走两步、`slow` 一步；`fast` 到尾时 `slow` 在中点。循环条件 `while fast and fast.next` 要同时判断两者（偶数长度时 `fast` 最终是 `None`，奇数长度时 `fast.next` 是 `None`）。
5. `has_cycle`：有环时 `fast` 会追上 `slow`（环里每步距离缩短 1），所以一定相遇；无环时 `fast` 先走到 `None`。O(n) 时间 O(1) 空间，比哈希集合省内存。

## 3. 完整手算（Worked trace）

反转 `1 -> 2 -> 3`。`prev` 是「已经反转好的部分」的头，`cur` 是「还没处理的部分」的头：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def show(node):
    out = []
    while node:
        out.append(str(node.val))
        node = node.next
    return " -> ".join(out) + " -> None" if out else "None"

def reverse_trace(head):
    prev, cur = None, head
    step = 0
    while cur:
        step += 1
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
        print(f"step {step}: reversed part = {show(prev)}   rest = {show(cur)}")
    return prev

head = ListNode(1, ListNode(2, ListNode(3)))
print("start: prev = None   cur =", show(head))
new = reverse_trace(head)
assert show(new) == "3 -> 2 -> 1 -> None"
```

```text
start: prev = None   cur = 1 -> 2 -> 3 -> None
step 1: reversed part = 1 -> None   rest = 2 -> 3 -> None
step 2: reversed part = 2 -> 1 -> None   rest = 3 -> None
step 3: reversed part = 3 -> 2 -> 1 -> None   rest = None
```

每一步做四件事（对应 `206` 的四行代码）：
1. `nxt = cur.next` —— 先存住「剩下的部分」；
2. `cur.next = prev` —— 把当前节点指向已反转部分；
3. `prev = cur` —— 已反转部分的头前进一格；
4. `cur = nxt` —— 处理下一个。

循环结束时 `cur` 是 `None`，`prev` 就是新的头。**如果颠倒 1 和 2 的顺序，`cur.next` 已经被覆盖，剩余链表丢失。**

## 4. 题目

```python
class Node:                                   # LC 138's node: next pointer + a random pointer
    def __init__(self, x, next=None, random=None):
        self.val = x
        self.next = next
        self.random = random
```

### 4.1 LC 206 · Reverse Linked List（Easy，频率 62）

```python
# solutions/206_reverse_linked_list.py
def reverse_list(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next        # 1. remember the rest before we cut the link
        cur.next = prev       # 2. point backwards
        prev = cur            # 3. advance prev
        cur = nxt             # 4. advance cur
    return prev               # prev is the new head when cur falls off the end


def reverse_list_recursive(head):
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)   # reverse the tail first
    head.next.next = head                          # the node after head now points back at head
    head.next = None
    return new_head
```

- **一句话洞见**：`prev / cur / nxt` 三指针，每步把一个节点的 `next` 掉头。递归版本：先反转后面的，再让 `head.next.next = head`。
- **复杂度**：迭代 O(n) 时间 O(1) 空间；递归 O(n) 时间 O(n) 栈空间。

**资深追问**

- **规模 ×1000**：递归版本在链表长 10⁵ 时会 `RecursionError`（Python 默认深度 1000），必须用迭代。
- **流式**：链表就是「流」的形态；反转需要先到达末尾，无法边读边出，但原地反转不需要额外内存。
- **内存**：迭代 O(1)。
- **并发**：反转过程中其他线程在遍历会看到断裂的链表；要么加读写锁，要么返回一个**新的**反转副本（持久化 / 不可变结构）。
- **接口 / 边界**：原地修改还是返回新链表？原来的 `head` 在反转后变成尾节点，调用者手里的旧引用现在指向尾——要在文档里写明。空链表和单节点；输入如果有环会死循环（可先用快慢指针检测）。
- **测试**：长度 0、1、2、n；`to_list(reverse(x)) == to_list(x)[::-1]`；性质：节点身份（`id`）集合不变，说明是原地的。

### 4.2 LC 21 · Merge Two Sorted Lists（Easy，频率 67）

```python
# solutions/21_merge_two_sorted_lists.py
def merge_two_lists(a, b):
    dummy = tail = ListNode()              # dummy removes the "is the result empty yet?" special case
    while a and b:
        if a.val <= b.val:                 # <= keeps the merge stable (a's equal items first)
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b                     # splice whatever is left, no copying
    return dummy.next
```

- **一句话洞见**：dummy 头 + 两个指针，每次接上较小的那个；最后把剩下的一整段直接接上（不用逐个复制）。
- **复杂度**：时间 O(m + n)，空间 O(1)（复用原节点）。

**资深追问**

- **规模 ×1000**：线性；k 路归并用堆（第 05 讲 LC 23），或两两分治，O(N log k)。
- **流式**：两个有序流的合并就是归并排序的合并步骤，输出也是流；需要处理「其中一路暂时没有数据」的语义。
- **内存**：复用节点 O(1)；若不允许改输入，拷贝节点 O(m + n)。
- **并发**：并行归并（把一个列表按中点切开，用 merge path 找切分点，两半各自合并）。
- **接口**：稳定性（值相等时哪个列表在前——`<=` 取第一个列表的）；降序列表怎么办；是否允许修改输入。
- **测试**：两个空、一个空、全部相等、一个列表全小于另一个、交错；与 `sorted(a + b)` 对拍。

### 4.3 LC 2 · Add Two Numbers（Medium，频率 80）

```python
# solutions/2_add_two_numbers.py
def add_two_numbers(a, b):
    dummy = tail = ListNode()
    carry = 0
    while a or b or carry:                 # carry keeps the loop alive for the final extra digit
        total = carry
        if a:
            total += a.val
            a = a.next
        if b:
            total += b.val
            b = b.next
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next
```

- **一句话洞见**：个位在链表头，所以可以像竖式加法一样从头走到尾，`carry` 带到下一位；循环条件加上 `or carry` 处理最后一次进位。
- **复杂度**：时间 O(max(m, n))，空间 O(1) 额外（输出链表不计）。

**资深追问**

- **规模 ×1000**：数字有 10⁶ 位时仍是线性；这也是大整数（BigInteger）加法的基本形态。
- **流式**：最高位在前（LC 445）时不能直接做；用两个栈，或先反转，或递归对齐位数；最低位在前的流可以边读边输出。
- **内存**：可以把结果就地写进较长的那条链表上，O(1) 额外空间（需要允许修改输入）。
- **并发**：进位是串行依赖；并行加法用进位前瞻（carry-lookahead），一般面试里只需要提到。
- **接口**：数字是否有前导零？负数？不同进制？链表是空（表示 0 还是非法）？
- **测试**：`999 + 1`（进位链）、长度不等、两个 0、单个节点进位（5+5）；与 Python 大整数运算对拍。

### 4.4 LC 138 · Copy List with Random Pointer（Medium，频率 75）

```python
# solutions/138_copy_list_with_random_pointer.py
def copy_random_list(head):
    clone = {None: None}                    # old node -> new node; None maps to None
    cur = head
    while cur:                              # pass 1: create all copies
        clone[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                              # pass 2: wire next/random through the map
        clone[cur].next = clone[cur.next]
        clone[cur].random = clone[cur.random]
        cur = cur.next
    return clone[head]


def copy_random_list_o1(head):
    if not head:
        return None
    cur = head
    while cur:                              # A -> A' -> B -> B' ...
        cur.next = Node(cur.val, cur.next)
        cur = cur.next.next
    cur = head
    while cur:                              # A'.random = A.random' (the node right after A.random)
        if cur.random:
            cur.next.random = cur.random.next
        cur = cur.next.next
    new_head = head.next
    cur = head
    while cur:                              # unzip the two lists, restoring the original
        copy = cur.next
        cur.next = copy.next
        copy.next = copy.next.next if copy.next else None
        cur = cur.next
    return new_head
```

- **一句话洞见**：深拷贝的难点是 `random` 指向「还没创建的新节点」。先一遍创建所有新节点并记录 `旧 → 新` 映射，第二遍再连接 `next` 和 `random`。O(1) 空间版本把新节点**织进**旧链表（`A → A' → B → B'`），`A'.random = A.random.next`，最后拆开。
- **复杂度**：映射版 O(n) 时间 O(n) 空间；交织版 O(n) 时间 O(1) 空间。

**资深追问**

- **规模 ×1000**：线性。映射版在 10⁸ 节点时内存压力大（每个映射条目 ≥ 几十字节）→ 面试官想听到交织版。
- **流式 / 序列化**：把带随机指针的结构序列化到磁盘 = 给节点编号，`random` 存编号；反序列化时按编号重建——本质是同一个映射。
- **内存**：映射 O(n) vs 交织 O(1)；交织版会暂时破坏原链表，**必须保证最后还原**（并发读者会看到被破坏的状态）。
- **并发**：拷贝过程中链表被修改会得到不一致的副本；先加锁拿快照，或使用不可变 / 持久化结构。
- **接口**：`random` 可以指向 `None`；如果 `random` 指向链表之外的节点怎么办？一般图的深拷贝（LC 133）要处理环，同样用「旧→新」映射。
- **测试**：空链表、单节点自指、所有 `random` 为 `None`、全部指向头；检查：副本与原链表**没有共享节点**，结构（值 + random 下标）相同，原链表没有被改动。

### 4.5 LC 25 · Reverse Nodes in k-Group（Hard，频率 62）

```python
# solutions/25_reverse_nodes_in_k_group.py
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy                         # node just before the current block
    while True:
        kth = group_prev
        for _ in range(k):                     # find the k-th node of the block, or stop if short
            kth = kth.next
            if not kth:
                return dummy.next
        group_next = kth.next                  # first node after the block
        prev, cur = group_next, group_prev.next
        while cur is not group_next:           # reverse the block; its tail ends up pointing at group_next
            cur.next, prev, cur = prev, cur, cur.next
        block_tail = group_prev.next           # old first node is now the block's tail
        group_prev.next = kth                  # kth is the new block head
        group_prev = block_tail
```

- **一句话洞见**：对每一组先「向前数 k 个」确认够长（不够就停，保持原样），再用 206 的三指针反转这一组，并把它接回前后。dummy 头 + `group_prev`（组前一个节点）保证每一组的接法一样。
- **关键细节**：反转时让 `prev` 初值是**下一组的头**（`group_next`），这样反转完这一组的尾自动指向下一组。
- **复杂度**：时间 O(n)（每个节点被访问 ≤ 2 次），空间 O(1)。

**资深追问**

- **规模 ×1000**：线性；递归版本深度 n/k，要小心栈溢出，迭代版 O(1)。
- **流式**：每次只需要缓冲 k 个节点，内存 O(k)；输出可以按组吐出，最后一个不足 k 的组原样输出。
- **内存**：O(1) 额外。
- **并发**：先顺序找到各组边界（O(n) 一遍），然后各组的反转互相独立，可以并行；但接回前后的指针要在合并阶段统一处理。
- **接口**：`k = 1` 或 `k > 长度`原样返回；最后不足 k 的组是否也反转（本题不反转，某些变体反转）；`k <= 0` 非法。
- **测试**：长度恰为 k 的倍数、不是倍数、`k = 1`、`k = 长度`、空链表、单节点；与「把数组切块 + 每块反转」的数组实现对拍。

## 5. 常见 bug

1. **先改 `cur.next` 再保存 `nxt`**：丢失剩余链表。
2. **忘记 dummy 头节点**：头节点被删除 / 替换时返回错误的头；或写出一堆 `if head is None` 特判。
3. **`while fast.next and fast.next.next` 写成 `while fast.next.next`**：空链表 / 单节点时 `AttributeError`（`None.next`）。
4. **删除节点后还前进 `prev`**：跳过了连续相同值的下一个。
5. **返回 `dummy` 而不是 `dummy.next`**。
6. **链表里出现环**：反转 / 合并里变成死循环，面试里可以先问「保证无环吗」。
7. **LC 25 的一行多重赋值**：`cur.next, prev, cur = prev, cur, cur.next` 先计算右边的元组再从左到右赋值，所以是对的；但任何顺序错误都会出事，写的时候一定要慢。
8. **交织版 138 忘记最后拆开原链表**，导致原链表被破坏。

## 6. 自测题

1. 为什么反转链表一定要先保存 `nxt = cur.next`？
   <details><summary>答案</summary>`cur.next = prev` 会覆盖原来的 `next` 引用，如果没有提前存起来，后面的节点没有任何引用指向，就无法继续遍历（丢失）。</details>
2. dummy 头节点解决了什么问题？
   <details><summary>答案</summary>让头节点也有「前驱」，删除 / 插入 / 合并时不必对头节点做特殊处理；最后返回 `dummy.next`。</details>
3. 快慢指针为什么能判环？
   <details><summary>答案</summary>进环后快指针每步比慢指针多走 1 格，环内的距离差每轮减 1，必然减到 0，两者相遇；无环则快指针先走到 `None`。</details>
4. 小编程：删除链表倒数第 n 个节点（LC 19），只遍历一次。
   <details><summary>答案</summary>`dummy` 头；`fast` 先走 n 步；然后 `fast` 与 `slow`（从 dummy 出发）一起走到 `fast.next is None`；`slow.next = slow.next.next`。O(n) 时间，O(1) 空间。</details>
5. 判断链表是否回文（LC 234）怎么做到 O(1) 空间？
   <details><summary>答案</summary>快慢指针找中点；反转后半段；两段逐个比较；（可选）比较完再把后半段反转回来还原输入。</details>
6. 资深追问：你的链表反转函数被一个多线程服务调用，其他线程正在遍历它，怎么办？
   <details><summary>答案</summary>原地修改对并发读者不安全。选项：对链表加读写锁；或返回新的反转副本，并用原子引用替换旧头（copy-on-write / 持久化数据结构）；让读者拿到一致的快照。</details>
