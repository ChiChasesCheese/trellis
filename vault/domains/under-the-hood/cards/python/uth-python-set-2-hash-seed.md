---
id: uth-python-set-2-hash-seed
node: python.set
type: qa
step: 2
---
## Q
**字符串集合的顺序为什么每次运行都不同**｜Python · CPython 3.14

同一段代码 `print(list({'apple','banana','cherry','date'}))` 连续跑几次，输出顺序为什么会变？

## A
**结构。** `str` 和 `bytes` 的哈希是带密钥的 SipHash（3.14 默认 `siphash13`），密钥在进程启动时随机生成。

**细节。**

- 哈希变了，元素落进的槽就变了，遍历顺序随之改变；实测三次输出三种顺序。
- `PYTHONHASHSEED=0` 关闭随机化，两次输出相同。
- `int` 不随机，小整数集合的顺序每次相同，但也不能依赖它。

**为什么。** 防哈希洪水（hash flooding）：攻击者构造一批哈希相同的字符串，把 O(1) 的插入拖成 O(n²)。密钥保密，他就无法预先构造。

**对应 LeetCode：** LC 49 字母异位词分组 · LC 387 字符串中的第一个唯一字符
