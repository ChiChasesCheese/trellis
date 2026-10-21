---
id: amz-logger-parse-log-lines
node: amazon.amz-logger
type: qa
step: 6
tags: [grown]
---
## Q
在日志框架设计里，追加需求「把日志行解析回 `LogRecord`，且支持多种格式」，怎么设计？

## A
解析是 Formatter 的逆，单独做一个 `parse(line)`，不塞进 Formatter。多格式：按「以 `{` 开头先试 JSON，否则试文本正则」的顺序逐个尝试；新增格式只在列表里加一个解析函数。解析不了的行返回 `None` 让调用方计数，不抛异常——日志文件里总有被截断的行。
```python
LINE = re.compile(r"(\S+) (\w+) ([\w.]+): (.*)")

def parse(line):
    if line.startswith("{"):
        d = json.loads(line)
        return LogRecord(d["ts"], Level[d["level"]], d["name"], d["msg"])
    m = LINE.fullmatch(line)
    if m is None:
        return None
    return LogRecord(m[1], Level[m[2]], m[3], m[4])
```
