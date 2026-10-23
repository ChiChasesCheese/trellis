---
id: hl-oa01-sealed-outcome
node: problems.oa01-job-chain
type: qa
step: 12
---
## Q
任务链报表里用 sealed 接口 `Outcome` 加模式匹配 `switch` 输出结果，代码怎么写？好处是什么？

## A
```java
public sealed interface Outcome permits Ok, Malformed {}
public record Ok(List<Chain> chains) implements Outcome {}
public record Malformed(String reason) implements Outcome {}

static Outcome analyze(List<String> lines) {
    try { return new Ok(chains(parse(lines))); }
    catch (MalformedInputException e) { return new Malformed(e.getMessage()); }
}
static List<String> render(Outcome o) {
    return switch (o) {
        case Malformed _ -> List.of("Malformed Input");
        case Ok(var chains) -> { ...; yield lines; }
    };
}
```
- 内部各层**抛异常**；在 `analyze` 这**一个**边界把异常变成值，之后只处理值。
- `sealed ... permits Ok, Malformed`：两个 `case` 就穷尽，不需要 `default`；新增第三种结果（如 `Empty`）时，没处理它的 `switch` **编译失败**。
- `case Ok(var chains)` 是 record 模式，一步完成判断类型加取字段；`case Malformed _` 的 `_` 表示不需要字段（Java 21 预览）；`yield` 在 switch 表达式块里返回分支值。
- 这种「封闭类型族 + 按类型分派」叫代数数据类型（algebraic data type）。
