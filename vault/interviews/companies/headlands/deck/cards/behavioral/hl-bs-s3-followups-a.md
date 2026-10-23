---
id: hl-bs-s3-followups-a
node: behavioral.stories
type: qa
step: 19
---
## Q
被追问 S3：为什么没有异常？为什么函数重载危险？你怎么排除"只是延迟"？
Why no exception? Why are overloads dangerous? How did you rule out lag?

## A
- **Why no exception?** SQL 的 **NULL 传播**：`NULL || x` 是 NULL；查找**没匹配**，所以**没产生行**。
- **Why are overloads dangerous?** **同名不同行为**；调用由**实参**决定；CTE 和 `MERGE` 选中了不同的重载。
- **How did you rule out lag?** **对照组**（该字段已设的行）有手续费；**年龄分桶**全是 0%。
