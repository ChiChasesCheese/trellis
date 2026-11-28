---
id: pl-out-cross-passing-copy-move
node: output.cross-passing
type: qa
step: 3
---
## Q
**赋值：别名、拷贝、移动**｜读代码说输出

**Python**
```python
a = [1]
b = a
b.append(2)
print(a)
```
**C++**
```cpp
int main() {
    vector<int> a{1};
    auto b = a;
    b.push_back(2);
    cout << a.size() << endl;
}
```
**Go**
```go
func main() {
	a := [2]int{1, 2}
	b := a
	b[0] = 9
	s := []int{1, 2}
	t := s
	t[0] = 9
	fmt.Println(a, s)
}
```
**Rust**
```rust
fn main() {
    let a = vec![1];
    let b = a;
    println!("{:?}", a);
}
```

输出什么？

## A
**输出。**
**Python**
```
[1, 2]
```
**C++**
```
1
```
**Go**
```
[1 2] [9 2]
```
**Rust**
```
error[E0382]: borrow of moved value: `a`
```（编译失败，没有输出）

**为什么。**
- Python 的 `b = a` 只复制引用，两个名字指向同一个列表，`a` 看到追加的 2。Go 的切片 `t := s` 同理共享底层数组，所以 `s` 变成 `[9 2]`。
- C++ 的 `auto b = a` 拷贝整个 `vector`，两个独立，`a` 的 size 仍是 1；Go 的数组是值类型，`b := a` 也是复制，`a` 仍是 `[1 2]`。
- Rust 的 `let b = a` 把所有权移动（move）给 `b`，`a` 随即失效，再使用就编译失败：`error[E0382]: borrow of moved value: `a``。

**语言为什么这样设计。**
- 有垃圾回收的语言（Python、Java、Go 切片）让别名安全：多个引用放心共享，回收由 GC 管。C++ 默认值语义，要共享得显式用指针或引用；Rust 规定每个值只有一个主人，没有 GC 也能安全释放，代价是你必须想清楚谁拥有。
- 同样一行 `b = a`，语义分别是共享、复制、转让。

**怎么写才对。**
```python
b = a.copy()            # Python：或 a[:]
```
```go
t := slices.Clone(s)    // Go
```
```rust
let b = a.clone();      // Rust：想要两份就显式克隆
```

**面试里一句话。**
Assignment aliases in Python and Go slices, copies in C++ and Go arrays, and moves in Rust, where the old name stops being usable.
