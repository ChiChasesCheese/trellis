---
id: hl-cq-q20-error-message-compare
node: cpp-questions.e-templates
type: qa
step: 3
---
## Q
传一个没有 `price()` 的类型 `Rock` 给模板函数 `mark<T>`：带 concept 和不带 concept 的编译错误分别出现在哪里、长什么样？

## A
- **带 concept**：错误出现在**调用处**，并给出原因：
  - `no matching function for call to 'mark'`
  - `constraints not satisfied [with T = Rock]`
  - `because 't.price()' would be invalid: no member named 'price' in 'Rock'`
- **不带 concept**：错误出现在**模板体内部**，要靠 “in instantiation of function template specialization 'mark<Rock>' requested here” 这条 note 追溯到实例化点。
- 这就是 concepts 的价值：把页数很长的错误缩成一行清楚的理由。
