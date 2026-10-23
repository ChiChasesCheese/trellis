---
id: hl-os-ipc-java-pipe
node: foundations.os-processes-threads-ipc
type: qa
step: 17
---
## Q
Java 里怎么用管道和子进程通信？`java.nio.channels.Pipe` 是进程间的管道吗？

## A
用 `ProcessBuilder` 启动子进程，得到 stdin / stdout / stderr 三个管道：
```java
Process p = new ProcessBuilder("sort").start();
try (Writer w = new OutputStreamWriter(p.getOutputStream())) {
    w.write("pear\napple\nfig\n");        // 写进子进程 stdin
}
try (BufferedReader r = new BufferedReader(
        new InputStreamReader(p.getInputStream()))) {
    r.lines().forEach(System.out::println);   // apple fig pear
}
p.waitFor();
```
注意 `java.nio.channels.Pipe` **只能在同一个 JVM 内**使用，不是进程间的管道。
