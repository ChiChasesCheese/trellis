---
id: cc-model-idem-double-free
node: model.idempotency
type: cloze
---
Releasing a resource twice must not return it to the pool twice: `deallocate("apibox1")` followed by the same call again would otherwise let {{c1::two live hosts share the number 1}}. The guard is {{c2::a set of currently-allocated names, checked before pushing the number back onto the free heap}}; an unknown, malformed or already-freed name is {{c3::ignored, not an error}}, unless the statement asks for a strict mode.

## zh
释放资源两次不能把它放回池子两次：`deallocate("apibox1")` 之后再调一次，否则会让 {{c1::两台活着的主机共用编号 1}}。保护措施是 {{c2::一个"当前已分配名字"的集合，在把编号压回空闲堆之前检查}}；未知的、格式错误的或已释放的名字 {{c3::被忽略，而不是报错}}，除非题面要求严格模式。
