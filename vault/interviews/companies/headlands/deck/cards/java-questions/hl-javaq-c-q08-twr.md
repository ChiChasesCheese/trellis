---
id: hl-javaq-c-q08-twr
node: java-questions.c-languages
type: qa
step: 8
---
## Q
写出 Java 里 try-with-resources 的写法。多个资源的关闭顺序是什么？异常路径上先关资源还是先进 catch？

## A
```java
try (var a = openA(); var b = openB()) {
    body();
} catch (Exception e) {
    handle(e);
}
```
- 退出块时按**相反顺序**调用 `close()`：先 close B，再 close A。
- 包括异常路径：**先关资源，再进 catch**（输出顺序：open A、open B、body、close B、close A、caught）。
- 资源类要实现 `AutoCloseable`。
- GC 不管文件、socket、锁何时释放，所以这些必须显式关闭。
