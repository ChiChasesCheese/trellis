---
id: s23-browser-ide-print-debugging
node: stripe.solving
type: qa
---

## Q
HackerRank 这种浏览器 IDE 没有断点，还会记录切换标签页的次数，调试该怎么打印才不出问题？

## A
HackerRank 记录切换标签页的次数，也没有断点。因此：

- **只往 stderr 打印**：`print(x, file=sys.stderr)`。stdout 上多一个字符就全挂。
- 打印**结构化**的东西：`print(f"{acct=} {total=} {fraud=}", file=sys.stderr)`
  （`f"{x=}"` 自动带变量名，Python 3.8+）。
- 交卷前全部删掉。
