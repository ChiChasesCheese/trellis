---
slug: design-browser-history
---
## Q
**LC 1472 设计浏览器历史记录**｜Medium

实现 `visit(url)`（清空前进记录）、`back(steps)`、`forward(steps)`，后两者越界就停在端点，返回所在页面。

## A
**一句话。** 一个数组加两个下标：`cur` 是当前页，`last` 是能前进到的最后一页；`visit` 覆盖写 `cur + 1` 并把 `last` 设成它，不必真删。

```python
class BrowserHistory:
    def __init__(self, homepage):
        self.pages = [homepage]
        self.cur = 0         # 当前页
        self.last = 0        # 能前进到的最后一页

    def visit(self, url):
        self.cur += 1
        if self.cur == len(self.pages):
            self.pages.append(url)
        else:
            self.pages[self.cur] = url   # 覆盖旧的前进记录
        self.last = self.cur

    def back(self, steps):
        self.cur = max(0, self.cur - steps)
        return self.pages[self.cur]

    def forward(self, steps):
        self.cur = min(self.last, self.cur + steps)
        return self.pages[self.cur]
```

**复杂度。** 每个操作 `O(1)`，空间 `O(访问次数)`。

**易错点。**
- `forward` 夹到 `len(pages) - 1`：覆盖写法下旧记录还在数组里，会前进到已经作废的页面。
- `visit` 忘了更新 `last`：之前更长的前进记录又能走回去。

**追问。**
- 双栈写法？：后退栈、前进栈，`visit` 清空前进栈；每步移动一个元素，`back(k)` 是 `O(k)`。
- 双向链表？：节点存页面，`visit` 断开后继；`back/forward` 同样 `O(steps)`。

**同模式。** LC 155 最小栈、LC 146 LRU 缓存、LC 1381 设计一个支持增量操作的栈
