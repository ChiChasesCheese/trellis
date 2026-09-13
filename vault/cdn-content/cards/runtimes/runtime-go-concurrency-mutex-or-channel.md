---
id: runtime-go-concurrency-mutex-or-channel
node: runtimes.go-concurrency
type: qa
---
## Q
An in-memory metadata cache needs many reads and short atomic updates. Should it serialize all access through a channel or guard the map with a mutex?

## A
Use a mutex (`RWMutex` only if measurement proves read concurrency helps): the state is shared memory and operations are short. A channel-owned event loop is better when ownership transfer, ordering, or asynchronous coordination is the actual model. Serializing ordinary lookups through a channel adds queueing and a scheduler hop without improving correctness. Whichever model you choose, keep one owner model and verify it with `go test -race`.

## Q zh
进程内 metadata cache 有大量读取和很短的原子更新。应该把所有访问串行化到 channel，还是用 mutex 保护 map？

## A zh
用 mutex；只有 measurement 证明读并发有收益时才用 `RWMutex`。这里的状态是 shared memory，操作也很短。只有当 ownership transfer、ordering 或 asynchronous coordination 才是核心模型时，channel-owned event loop 更合适。普通 lookup 全走 channel 只会增加 queueing 和一次 scheduler hop，不会提升正确性。无论选哪种模型，都要坚持单一 ownership model，并用 `go test -race` 验证。
