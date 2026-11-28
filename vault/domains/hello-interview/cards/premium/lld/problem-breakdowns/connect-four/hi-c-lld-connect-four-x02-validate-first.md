---
id: hi-c-lld-connect-four-x02-validate-first
node: lld.problem-breakdowns.connect-four.exam
type: qa
step: 12
---
## Q
**四子棋 · 先改后校验的后果**｜考点 · 必会

有人把 `make_move` 写成先落子再检查是否轮到该玩家：
```python
row = board.place(col, p.color)
if p != self.current:
    return False
```
会发生什么？

## A
- **后果：** 不该走的玩家被拒绝了，棋子却已经落在盘上，状态被破坏；返回假却改了数据，调用方无从得知
- **更糟：** 之后合法玩家下同一列会落在更高的位置
- **规则：** 先把所有会失败的检查做完，再改状态
- **同理：** 悔棋、联网重试里，失败的操作也不能留下副作用
