---
id: tr-reliability-fault-injection-failpoints
node: reliability.fault-injection
type: qa
step: 2
---
## Q
进程内故障点（failpoint，在代码中预留的故障注入开关）和进程外故障注入（杀进程、改网络）相比，各有什么优缺点？进程内故障点怎么写？

## A
**进程外注入**：
- **优点**：不改被测代码，故障是真实的（真的断网、真的崩溃），能发现操作系统、网络栈、客户端库层面的问题。
- **缺点**：时机难控制。想测"写完数据但还没确认时崩溃"，用 `kill -9` 只能碰运气；结果不可重复。

**进程内故障点**：
- **优点**：可以把故障精确地放在某一行代码、某一个状态之后，每次都在同一位置触发，测试可重复；还能注入外部难以制造的错误，例如设备返回某个特定错误码。
- **缺点**：要改被测代码；注入的是"代码以为的故障"，可能和真实故障表现不同；故障点必须在生产构建中关闭或编译掉。

**一个最小实现**：

```python
_ACTIVE: dict[str, Exception] = {}

def failpoint(name: str) -> None:
    exc = _ACTIVE.get(name)
    if exc is not None:
        raise exc

def write_checkpoint(data):
    tmp = write_tmp(data)
    failpoint("after_tmp_before_rename")
    os.replace(tmp, FINAL)

def test_crash_between_write_and_rename(monkeypatch):
    monkeypatch.setitem(_ACTIVE, "after_tmp_before_rename",
                        RuntimeError("injected"))
    with pytest.raises(RuntimeError):
        write_checkpoint(b"new")
    assert read_final() == b"old"
```

成熟的实现会支持概率触发、第 N 次触发、延迟而不是报错，并能通过环境变量或管理接口开关，例如 Go 的 `pingcap/failpoint`、FreeBSD 和 Linux 内核的故障注入框架。

**搭配使用**：进程内故障点验证每个关键状态转换的处理逻辑；进程外注入验证整个系统在真实故障下的行为。
