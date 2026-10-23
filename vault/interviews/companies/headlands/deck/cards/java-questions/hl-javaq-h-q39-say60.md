---
id: hl-javaq-h-q39-say60
node: java-questions.h-ipc
type: qa
step: 8
---
## Q
用英文 60 秒回答：How would you implement shared memory IPC in Java? How do you get correct visibility across processes?

## A
结构：映射同一文件（Linux 用 /dev/shm）→ SPSC 环形缓冲，各写自己的序号，release 与 acquire 发布 → 用 VarHandle，普通 putLong 不保证可见 → head 与 tail 分缓存行 → 实测 0.15 微秒 → 生产用现成库并加校验和。

> "I'd map one file into both JVMs - on Linux in `/dev/shm` so it's pure memory - and build a single-producer single-consumer ring buffer on it. Each side owns one sequence number: the producer writes the slot, then publishes the new tail with release semantics; the consumer reads the tail with acquire semantics, processes the slot, then publishes the head. For the atomic accesses on mapped memory I use a `VarHandle` from `byteBufferViewVarHandle`, because plain `putLong` has no visibility guarantee. Head and tail go on separate cache lines to avoid false sharing. I tried the simplest version, a ping-pong between two JVMs, and got about 0.15 microseconds per round trip. For production I'd consider Aeron or Chronicle Queue, and I'd add checksums so a crashed writer doesn't leave a half-written record visible."
