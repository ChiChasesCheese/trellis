---
id: hl-c03-four-pointer-table
node: cpp-lessons.c03-smart-pointers
type: qa
step: 2
---
## Q
面试问：`unique_ptr`、`shared_ptr`、`weak_ptr` 和裸指针各自表达什么所有权？大小多少？什么时候用？
Interview question: When do you use `unique_ptr`, `shared_ptr` and `weak_ptr`?

## A
| 类型 | 所有权 / 大小 | 场景 |
|---|---|---|
| `unique_ptr<T>` | 唯一拥有；1 个指针（8 字节，零额外开销）；禁止拷贝，只能移动 | **默认选择**；工厂返回；容器里放多态对象 |
| `shared_ptr<T>` | 多个共同拥有，计数归零释放；2 个指针（16 字节） | 真有多个拥有者、生命周期难定 |
| `weak_ptr<T>` | 不拥有，只观察 `shared_ptr`；2 个指针 | 打破循环引用、缓存、观察者 |
| `T*` / `T&` | 不拥有，只借用 | 函数参数、非拥有的反向指针 |

默认 `unique_ptr`，需要共享再升级（`unique_ptr` 可直接转成 `shared_ptr`）。
