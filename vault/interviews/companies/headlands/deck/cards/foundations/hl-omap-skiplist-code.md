---
id: hl-omap-skiplist-code
node: foundations.ordered-maps-trees
type: qa
step: 18
---
## Q
写出最小跳表的 `randomLevel`、`contains` 和 `insert` 核心代码。

## A
```java
Node[] next;  // 每个节点 next[i] = 第 i 层下一个节点
int randomLevel() {
    int lvl = 1;
    while (lvl < MAX_LEVEL && rnd.nextBoolean()) lvl++;
    return lvl;
}
boolean contains(int key) {
    Node x = head;
    for (int i = levels - 1; i >= 0; i--)
        while (x.next[i] != null && x.next[i].key < key) x = x.next[i];
    x = x.next[0];
    return x != null && x.key == key;
}
void insert(int key) {
    Node[] update = new Node[MAX_LEVEL];       // 每层插入点的前驱
    Node x = head;
    for (int i = levels - 1; i >= 0; i--) {
        while (x.next[i] != null && x.next[i].key < key) x = x.next[i];
        update[i] = x;
    }
    int lvl = randomLevel();
    if (lvl > levels) { for (int i = levels; i < lvl; i++) update[i] = head; levels = lvl; }
    Node n = new Node(key, lvl);
    for (int i = 0; i < lvl; i++) { n.next[i] = update[i].next[i]; update[i].next[i] = n; }
}
```
关键：记下每层的前驱 `update[i]`，然后每层做一次链表插入。
