---
id: review-risk-bypass-path
node: review.risk-patterns
type: qa
step: 4
---
## Q
一个 diff 新增了批量修复脚本，直接写数据库；同一个 diff 里，还删掉了测试夹具中“禁止连接生产库”的检查，理由是“它让测试跑不起来”。评审时这两处为什么都要打回？

## A
**新增写入路径，要问它是否经过同一个入口；删守卫，要问它挡的是什么**

- **每个写入入口都应该走同一个函数**：记录审计、校验、权限都在里面；脚本自己写库，就绕过了它们，事后无法追溯是谁改了什么；
- **评审问法**：“这个仓库里还有几条路径会写这张表？它们都经过同一个入口吗？”；
- **删守卫的理由要认真对待**：“它让测试跑不起来”往往说明测试正在碰生产，守卫挡的正是它；改法是修测试，不是删守卫；
- **同样的信号**：删掉的断言、被放宽的权限、被注释掉的检查，diff 里的减号比加号更值得看；
- **要求的修改**：脚本调用公共入口，加一条测试断言“每次写入都留下记录”。

```python
audit, db = [], {}

def write(key, value, who):              # 唯一入口：写入必留记录
    audit.append((who, key, value))
    db[key] = value

def fix_script(key, value):              # 新增的脚本：直接写，绕过 write
    db[key] = value

write("r1", "ok", "api"); fix_script("r2", "fixed")
print(len(db), len(audit))                          # 2 1：两处写入，只留了一条记录
print(set(db) - {k for _, k, _ in audit})           # {'r2'}：这一条没有记录
```

**知识点：**diff 里的高风险信号（Risk Patterns）
