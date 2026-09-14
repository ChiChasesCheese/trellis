---
id: storage-encoding-compat-directions
node: storage.encoding
type: cloze
---
Schema evolution has two directions: {{c1::backward compatibility}} means **new code can read data written by old code** (the common, easier case — new readers handle old records), while {{c2::forward compatibility}} means **old code can read data written by new code** (harder — old readers must tolerate fields they don't know about, typically by {{c3::preserving/ignoring unknown fields}} rather than erroring or silently dropping them on rewrite).

## zh
Schema 演进有两个方向：{{c1::backward compatibility}} 意思是**新代码能读旧代码写的数据**（常见、更简单的情况——新读端处理旧记录），而 {{c2::forward compatibility}} 意思是**旧代码能读新代码写的数据**（更难——旧读端必须容忍它不知道的字段，通常通过 {{c3::保存/忽略未知字段}}而不是出错或在重写时无声丢弃）。
