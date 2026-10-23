---
id: hl-cq-q12-new-steps-placement
node: cpp-questions.c-memory-ownership
type: qa
step: 8
---
## Q
`new Widget` 分哪几步？构造函数抛异常时内存怎么办？补全：在 `malloc` 得到的原始内存上用 placement new 构造 `Widget`，再正确销毁。

## A
- `new Widget`：先 `operator new(sizeof(Widget))` 拿内存，再在那块内存上调用构造函数；构造函数抛异常时内存会被自动归还。
- `delete`：反过来，先析构再 `operator delete`。

```cpp
void* raw = std::malloc(sizeof(Widget));   // 只有字节，没有 Widget
Widget* b = new (raw) Widget;              // placement new：在已有内存上构造
b->~Widget();                              // 手动析构
std::free(raw);                            // 再释放
```
