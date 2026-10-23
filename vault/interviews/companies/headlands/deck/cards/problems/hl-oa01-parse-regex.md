---
id: hl-oa01-parse-regex
node: problems.oa01-job-chain
type: qa
step: 11
---
## Q
解析 `job_id,runtime,next` 一行时，正则怎么写？为什么故意接受负号、为什么用 `matches()` 而不是 `find()`？

## A
```java
private static final Pattern LINE =
    Pattern.compile("\\s*(-?\\d+)\\s*,\\s*(-?\\d+)\\s*,\\s*(-?\\d+)\\s*");
var m = LINE.matcher(raw);
if (!m.matches()) throw new MalformedInputException("bad line: " + raw);
```
- `\s*` 任意空白，`(-?\d+)` 可选负号加数字，括号是捕获组，`m.group(1)` 取值。
- **`matches()` 要求整行匹配**；`find()` 只要某段匹配，会把 `1,2,3,4` 误判成合法（找到 `1,2,3`）。
- 故意接受负号：让 `3,-5,0` 由 `Job` 的紧凑构造器报「时长为负」，信息比「格式错」更准（输出都是 `Malformed Input`）。
- `Integer.parseInt("99999999999")` 溢出抛 `NumberFormatException`，转成同一种 `MalformedInputException`，调用方只处理一种异常。
- 表头按 `#` 开头判断，不要假设第一行一定是表头，否则没有表头时会丢第一条数据；空行忽略。
