---
id: problems-unique-id-generator-clock-rollback-refuse
node: problems.foundations.unique-id-generator
type: qa
step: 4
tags: [grown]
---
## Q
In a Snowflake-style ID generator, why must the generator explicitly compare the current local clock reading against the timestamp used for its last generated ID, and refuse to generate when the clock reads earlier than that — instead of just using whatever the clock currently says?

## A
A time-of-day clock can step backwards (e.g. an NTP correction), so a later call to the generator could read a wall-clock value smaller than the timestamp embedded in an ID it already produced. If the generator naively used that smaller value, it could produce a new ID with a timestamp equal to or less than one already issued, directly violating the guarantee that IDs from the same node are strictly increasing, and risking a duplicate if the sequence counter also happens to collide. The correct behavior is to detect now < lastTimestampMs and refuse to generate (block or error) until the local clock catches back up to the last used timestamp, accepting a bounded pause in availability on that node rather than a correctness violation.

## Q zh
在一个 Snowflake 风格的 ID 生成器里，为什么生成器必须显式比较当前本地时钟读数和它上一次生成 ID 所用的时间戳，并在时钟读数比这个时间戳更早时拒绝生成，而不是直接用当前时钟给出的值？

## A zh
日期时间时钟可能向后跳变（例如一次 NTP 纠偏），所以生成器之后某次调用读到的墙钟值可能比它已经产出的某个 ID 里编码的时间戳更小。如果生成器天真地直接用这个更小的值，就可能产出一个时间戳等于或小于已发出 ID 的新 ID，直接违反'同节点 ID 严格递增'的保证，如果序列号计数器恰好也撞上，还有产生重复 ID 的风险。正确做法是检测到 now < lastTimestampMs 时拒绝生成（阻塞或报错），直到本地时钟追上上一次使用的时间戳为止，宁可接受该节点上一段有界的可用性暂停，也不接受正确性被破坏。
