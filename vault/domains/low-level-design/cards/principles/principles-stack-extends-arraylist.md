---
id: principles-stack-extends-arraylist
node: principles.composition
type: qa
step: 3
---
## Q
```python
class Stack(list):
    def push(self, item):
        self.append(item)
    def peek(self):
        return self[-1]
```
为什么用"继承 `list` 来实现 `Stack`"是一个设计错误？

## A
`Stack` 是一个 LIFO（后进先出）结构，但 `list` 是一个可按下标随机访问、可任意插入删除的序列。继承之后：

- 调用者仍然能调用 `stack[0]`、`stack.insert(0, x)`、`stack.sort()`——这些操作没有一个是 `Stack` 这个概念授权过的。
- 这违反了里氏替换原则：`Stack` 的调用者期望的是 LIFO 行为，却拿到了一个能做任意随机访问的对象。
- `Stack` 白白继承了一堆不相关的方法：`index`、`extend`、`sort` 等等，都成了它公开 API 的一部分。

正确设计：`Stack` **组合**一个 `list`（更地道的选择是 `collections.deque`，两端操作都是 O(1)），只暴露 `push`/`pop`/`peek` 三个方法——这是组合而不是继承。
