---
nodes: [problems.booking.library]
url: https://docs.python.org/3/library/collections.html#collections.deque
---
# collections.deque — 双端队列

值得读：预约队列为什么选 `deque` 而不是 `list`，依据就在这一节。`deque` 两端的 `append` 与
`popleft` 都是 O(1)，而 `list.pop(0)` 是 O(n)——每取走一位队首都要把后面所有人往前搬一格。
预约队列的核心操作恰好就是"队尾进、队首出"，这是 `deque` 被发明出来的那个形状。

同一页还回答了这道题的另外两个问题。第一，`deque.remove(x)` 是 O(n)：读者主动取消预约时用得上，
而队列长度在图书馆场景里是几十，完全可以接受——**知道它是 O(n) 并判断它可以接受**，比盲目换成
一个带索引的结构更能说明问题。第二，`in` 对 `deque` 同样是 O(n) 的线性扫描，所以"这位读者是不是
已经排过队"的检查也是 O(队长)；真要按 id 秒查，正确的加法是**另外**维护一张
`(读者, 书目) → 队列` 的索引，而不是把队列本身换掉——顺序和查找是两件事，让两个结构各管一件。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/collections.html#collections.deque)

## Archived copy
![[src-pydocs-music-streaming-clip]]
%% trellis:end %%
