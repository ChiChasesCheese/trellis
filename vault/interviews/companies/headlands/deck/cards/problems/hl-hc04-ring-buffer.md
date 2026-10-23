---
id: hl-hc04-ring-buffer
node: problems.hc04-queue-mean-snapshot
type: qa
step: 5
---
## Q
环形缓冲（ring buffer）怎么实现队列？容量为什么取 2 的幂？扩容时怎么抄才对？

## A
固定数组 + `head`（队头下标）+ `size`。第 k 个元素在 `(head + k) % 容量`，队尾下一个空位是 `(head + size) % 容量`；队尾走到末尾后绕回开头复用前面的空格，`pop` 只前移 `head`，O(1)。

容量取 **2 的幂**时 `% 容量` 可换成 `& (容量 - 1)`（`x % 8 == x & 7`），位运算更快；扩容 ×2 自然保持 2 的幂。
```java
void push(long x) {
    if (size == buf.length) grow();
    buf[(head + size) & (buf.length - 1)] = x; size++;
}
long pop() { long x = buf[head]; head = (head + 1) & (buf.length - 1); size--; return x; }
```
**扩容**必须按**逻辑顺序**（从 `head` 起绕回去）分两段抄，`head` 归零：
```java
long[] bigger = new long[Math.multiplyExact(buf.length, 2)];
int firstPart = buf.length - head;
System.arraycopy(buf, head, bigger, 0, firstPart);
System.arraycopy(buf, 0, bigger, firstPart, head);
buf = bigger; head = 0;
```
直接 `Arrays.copyOf` 在 `head` 不在 0 时顺序全乱（测试专让 head 停在 10）。`multiplyExact` 让容量翻倍溢出时抛异常而不是变负数。

**均摊 O(1)**：偶尔扩容抄 n 个，但翻倍后要再 push n 次才下次扩容，昂贵操作平摊到之前 n 次便宜操作上。
