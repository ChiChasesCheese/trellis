---
id: errors-unrecoverable-crash-or-recover
node: errors.unrecoverable
type: qa
step: 1
---
## Q
什么错误应该让进程直接停掉，什么错误值得恢复继续跑？服务启动时发现必需的配置缺失，该怎么办？

## A
**知道怎么办才恢复，状态不可信就停**

- **可恢复**：有明确的下一步，如超时重试、依赖挂了降级、单个请求失败回滚、单条记录无效跳过；
- **不可恢复**：继续运行只会产出错误结果：配置缺失、不变量被破坏、内存耗尽、代码本身的缺陷；
- **带着坏状态继续比崩溃更糟**：崩溃是一次可见的故障，坏数据则一路写进库里，之后很难查；
- **启动期的错误尽早、整体地报**：把缺的配置项一次列全然后退出，别等第一个请求碰到才发现；
- **崩溃之后靠外层拉起**：进程管理器（systemd、容器编排）负责重启，进程自己不必假装没事。

```python
REQUIRED = ("DB_URL", "API_KEY")

def load_config(env: dict) -> dict:
    missing = [k for k in REQUIRED if k not in env]
    if missing:                                   # 启动期：缺配置就不要开门营业
        raise SystemExit(f"missing config: {', '.join(missing)}")
    return {k: env[k] for k in REQUIRED}

try: load_config({"DB_URL": "x"})
except SystemExit as e: print(e.code)             # missing config: API_KEY
```

**知识点：**不可恢复错误与顶层处理（Crash vs Recover）
