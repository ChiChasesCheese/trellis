---
id: hl-j13-real-sites
node: java21.j13-unnamed-variables
type: qa
step: 15
---
## Q
真实代码里 `_` 的典型用法有哪几类（未命名模式变量、共用分支、record 解构、catch 参数）？各举一例。

## A
- 未命名模式变量：`case Malformed _ -> List.of("Malformed Input");`，`case Not _ -> ~reg;`
- 共用分支：`case Limit _, Market _ -> byId.containsKey(cmd.id()) ? DUPLICATE_ID : null;`
- record 解构跳过字段：`case Ready<T>(var v, _) -> out.add(v);`（`Ready` 是 `record Ready<T>(T value, int stream)`，合并输出只要值）
- catch 参数：`} catch (InterruptedException _) {`，`} catch (StackOverflowError _) {`

同一个 `switch` 里常见 `case Done<T> _ -> { return out; }` 与 `case Pending<T> _ -> throw new AssertionError(...)`。
