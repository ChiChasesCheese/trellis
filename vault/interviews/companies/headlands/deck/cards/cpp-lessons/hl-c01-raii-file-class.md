---
id: hl-c01-raii-file-class
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 8
---
## Q
写出一个包装 `FILE*` 的 RAII 类 `File`（构造打开、析构关闭）。为什么必须删除拷贝构造和拷贝赋值？

## A
```cpp
class File {
    std::FILE* f_;
public:
    File(const char* p, const char* m) : f_(std::fopen(p, m)) {
        if (!f_) throw std::runtime_error("cannot open");
    }
    ~File() { if (f_) std::fclose(f_); }
    File(const File&) = delete;
    File& operator=(const File&) = delete;
    std::FILE* get() const { return f_; }
};
```
- 拷贝会得到两个指向同一个 `FILE*` 的对象，各自析构时 `fclose` 两次 = **双重释放**。
- **拥有资源的类必须想清楚拷贝语义**：禁止拷贝、实现深拷贝，或把资源交给标准库成员类型去管理。
- 构造时打不开就抛异常：此时对象尚未完整存在，没有需要清理的东西；使用处的每个 `return` 和 `throw` 都会自动关文件。
