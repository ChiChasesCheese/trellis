---
id: hl-j07-test-idiom
node: java21.j07-text-blocks
type: qa
step: 16
---
## Q
测试里"多行输入 → 多行期望输出"用文本块的惯用法是什么？写出辅助方法和一个例子。

## A
```java
static List<String> lines(String block) { return block.lines().toList(); }

var input = lines("""
        # 样例
        LIMIT 1 SELL 101 5
        LIMIT 2 BUY 101 3

        """);
var expected = lines("""
        BUY id=2 qty=3
        total=8
        """);
assertEquals(expected, summarize(input));
```
把题面样例**原样粘进**测试，逐字符比较，不用逐行加引号和 `\n`。`.lines()` 不受结尾换行影响（不产生末尾空行）。
