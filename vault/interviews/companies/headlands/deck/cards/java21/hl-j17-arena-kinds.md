---
id: hl-j17-arena-kinds
node: java21.j17-ffm-api
type: qa
step: 5
---
## Q
`Arena` 的四个工厂方法（`ofConfined`、`ofShared`、`ofAuto`、`global`）分别谁能访问、谁来释放、用在哪？

## A
| 工厂方法 | 谁能访问 | 谁来释放 | 用途 |
|---|---|---|---|
| `ofConfined()` | **只有创建它的线程**，别的线程抛 `WrongThreadException` | 你 `close()` | 默认选择，最快 |
| `ofShared()` | 任何线程 | 你 `close()`（要与所有线程同步，较慢） | 多线程共享；堆外 ticker map 用它 |
| `ofAuto()` | 任何线程 | **GC** 回收，不能手动 close | 不想管释放，但仍要比 `ByteBuffer` 清晰的接口 |
| `global()` | 任何线程 | 永不释放 | 程序级常量 |

`Arena` 管理一组内存的**生命周期**。
