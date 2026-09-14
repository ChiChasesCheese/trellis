---
id: cc-toolbox-deque-popleft
node: toolbox.deque
type: cloze
---
`list.pop(0)` shifts every remaining element, so it costs {{c1::O(n)}} and a BFS built on it is {{c2::O(n²)}} overall; `collections.deque.popleft()` is {{c3::O(1)}}. The same asymmetry applies at the front for insertion — `lst.insert(0, x)` versus `dq.appendleft(x)`. What a deque does *not* give you is {{c4::indexing in the middle — `dq[i]` is O(n)}}, so anything needing random access or slicing stays a list.

## zh
`list.pop(0)` 会移动其余每一个元素，所以代价是 {{c1::O(n)}}，基于它的 BFS 整体是 {{c2::O(n²)}}；`collections.deque.popleft()` 是 {{c3::O(1)}}。头部插入也是同样的不对称 —— `lst.insert(0, x)` 对比 `dq.appendleft(x)`。deque *不*提供的是 {{c4::中间下标访问 —— `dq[i]` 是 O(n)}}，所以需要随机访问或切片的场合仍然用 list。
