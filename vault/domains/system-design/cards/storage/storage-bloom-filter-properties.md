---
id: storage-bloom-filter-properties
node: storage.internals.lsm
type: qa
---
## Q
A Bloom filter's two possible answers are asymmetric: one is trustworthy, one is not. State the asymmetry, why an LSM engine is safe with the untrustworthy side, and what knob trades memory for accuracy.

## A
- **"Definitely not present"** is guaranteed: if any of the key's hashed bit positions is 0, the key was never inserted. **No false negatives, ever** — this is the load-bearing property; a false negative would make the engine skip an SSTable that holds the key and *return a wrong result*.
- **"Possibly present"** can lie (**false positive**): other keys may have set the same bits. The cost of the lie is only a **wasted SSTable read** that finds nothing — correctness is untouched, so a small lie rate is a fine price.

The knob is **bits per key** (equivalently filter size and hash count): ~10 bits/key gives roughly a 1% false-positive rate, and each extra ~5 bits per key cuts it about 10×. Tune down for memory-tight, write-mostly data; tune up when the workload does many lookups of absent keys (the exact case filters exist for).

## Q zh
Bloom filter 的两种可能回答是不对称的：一种可信，一种不可信。说出这种不对称性、为什么 LSM 引擎能安全承受不可信的那一面，以及哪个旋钮用内存换准确率。

## A zh
- **"肯定不存在"**是有保证的：只要 key 哈希到的位里有任何一位是 0，这个 key 就从未插入过。**永远没有 false negative** — 这是承重性质；一次 false negative 会让引擎跳过实际持有该 key 的 SSTable，*返回错误结果*。
- **"可能存在"**会撒谎（**false positive**）：其他 key 可能置了相同的位。谎言的代价只是**一次白读 SSTable**、什么也没找到 — 正确性不受影响，所以小小的撒谎率是划算的价格。

旋钮是**每 key 的位数**（等价于 filter 大小和哈希函数个数）：约 10 bits/key 给出大约 1% 的 false positive 率，每多约 5 bits/key 大约再降 10 倍。内存紧张、以写为主的数据往低调；工作负载经常查找不存在的 key 时往高调（这正是 filter 存在的意义所在的场景）。
