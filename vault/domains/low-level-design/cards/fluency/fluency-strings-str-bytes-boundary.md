---
id: fluency-strings-str-bytes-boundary
node: fluency.strings-bytes
type: qa
step: 1
---
## Q
服务从文件和网络读到 `bytes`，业务代码里处理 `str`。`b"abc" == "abc"` 是什么结果？字节在哪里变成文本，遇到不是合法 UTF-8 的字节串时该怎么处理？

## A
**字节在边界解码一次，内部只用 str**

- **两种类型互不相等**：`b"abc" == "abc"` 为 `False`，不报错也不转换；拿字节串当字典键去查 str 键，永远查不到；
- **只在边界转换**：读入时 `decode("utf-8")`，输出时 `encode("utf-8")`；中间所有逻辑只见 `str`；明确写出编码，不依赖机器的默认编码；
- **解码失败是 `UnicodeDecodeError`**（`ValueError` 的子类）：不要吞掉；要么当成 400（输入非法），要么用 `errors="replace"` 把坏字节换成 `�` 并接受信息丢失，二选一是产品决定，不是技术细节；
- **编码也会失败**：`str` 里的孤立代理项（lone surrogate，如 `"\ud800"`）不能编码成 UTF-8，抛 `UnicodeEncodeError`；这类值来自别的语言的序列化，边界上要当作无效输入拒绝；
- **别猜编码**：同一串字节用 `latin-1` 解码永远“成功”，只是得到乱码；解码成功不代表对。

```python
raw = "café".encode("utf-8")
print(raw, raw == "café", raw.decode("utf-8") == "café")   # b'caf\xc3\xa9' False True

bad = b"caf\xe9"                                 # latin-1 的 é，不是合法 UTF-8
try: bad.decode("utf-8")
except UnicodeDecodeError as e: print("bad input:", e.reason)
print(bad.decode("utf-8", errors="replace"))      # caf�
try: "ab\ud800".encode("utf-8")
except UnicodeEncodeError as e: print("cannot encode:", e.reason)   # surrogates not allowed
```

**知识点：**字符串与字节（Strings & Bytes）
