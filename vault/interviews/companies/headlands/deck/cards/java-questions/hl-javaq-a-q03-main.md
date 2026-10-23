---
id: hl-javaq-a-q03-main
node: java-questions.a-speed
type: qa
step: 9
---
## Q
Java 在哪些地方能接近 C++ 的延迟，哪些地方不能？你会怎么搭一个低延迟 Java 系统？
Where can Java approach C++ latency, and where can't it? How would you build a low-latency Java system?

## A
一句话：**稳态热路径可以接近 C++（几百纳秒到微秒级），差距在尾部**。

能接近的：热点循环、数值计算、被逃逸分析消除的小对象（稳态每次迭代约 1 ns）；GC 造成的尾延迟可压到亚毫秒。

不能（或很难）接近的：预热、去优化（deoptimization）、对象头与指针追逐、没有内联值类型、GC 屏障开销、系统调用与内核旁路网络、safepoint、页错误和 OS 调度。

做法：**热路径零分配 + 预热 + 低暂停 GC + 绑核 + 必要时堆外**。内核旁路网络之类场景，诚实地说仍然期望 C++。
