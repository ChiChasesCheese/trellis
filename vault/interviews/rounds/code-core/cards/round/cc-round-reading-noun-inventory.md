---
id: cc-round-reading-noun-inventory
node: round.reading
type: qa
---
## Q
Two minutes into a spec about merchants, category codes, charges and disputes. What do you write down before any code?

## A
**The noun inventory: which nouns are keyed, which are counted, which are events.** Each line becomes one structure.

```
merchant -> category            dict
category -> threshold           dict
charge_id -> (merchant, fraud)  ledger, needed to undo
merchant -> (fraud, total)      counters
```

Naming them before coding makes the later part an added dict rather than a rewrite, and gives you the vocabulary to talk about the design. If a noun appears in a later part's rule but in none of your lines, you have found the structure you were about to forget.

## Q zh
读一份关于商户、类别码、扣款和争议的题面，两分钟后。写任何代码之前你先写下什么？

## A zh
**名词清单：哪些名词被当 key、哪些被计数、哪些是事件。** 每一行对应一个结构。

```
merchant -> category            dict
category -> threshold           dict
charge_id -> (merchant, fraud)  ledger, needed to undo
merchant -> (fraud, total)      counters
```

先命名再写代码，能让后面的部分变成"多加一个 dict"而不是重写，也给了你谈论设计的词汇。如果某个名词出现在后面部分的规则里、却不在你的任何一行里，那正是你差点漏掉的结构。
