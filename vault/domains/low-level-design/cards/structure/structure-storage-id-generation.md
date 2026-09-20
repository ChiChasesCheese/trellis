---
id: structure-storage-id-generation
node: structure.storage
type: cloze
step: 2
---
内存存储里用 `self._next_id += 1` 生成主键，在并发下会出问题，因为这一行其实是{{c1::"读取旧值、加一、写回"三个步骤，不是单一原子操作}}；两个线程可能读到同一个旧值，其中一次自增会{{c2::丢失（丢失更新）}}。想要紧凑、有序的 id，应该改用 {{c3::`itertools.count()` 配合一把锁（或 `threading.Lock` 保护整个读改写）}}。当 id 必须**不经协调**地生成（多个进程/多台机器各自建对象）时改用 {{c4::`uuid.uuid4()`}}，代价是 id 又长又没有顺序含义。永远不要从可变的业务字段推导 id——它必须在其他一切都改变时保持稳定。
