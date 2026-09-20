---
id: quality-test-doubles
node: quality.testability
type: qa
step: 3
---
## Q
写一个依赖了 `EmailSender` 的类的测试，什么时候该用一个手写的 fake，什么时候不得不用 `unittest.mock.patch`，为什么默认应该偏向前者？

## A
fake 是一个真实可用的轻量实现——`class FakeEmailSender: sent = []; def send(self, msg): self.sent.append(msg)`——它有自己的状态和行为，测试断言的是这个状态（"`sent` 里有一封给对方的邮件"），和生产实现之间只差"真的把邮件发出去"这一步。`patch` 打的是被测代码内部对某个名字的引用，测试断言变成"某个函数是不是被调用了、参数是什么"，这把测试焊死在了实现细节上——换一种实现方式（哪怕行为完全等价）测试就会跟着挂。

fake 需要通过构造函数注入才能生效，前提是这个类本身是可测的（见接缝/构造函数注入）；如果依赖是一段遗留代码，构造函数注入不到（比如它内部直接 `import` 了一个模块级函数），`patch` 是唯一能插进去的办法，但这应该被当作一个临时的应急手段，理想状态是逐步把这类代码改造成可以接受注入的依赖，而不是把 `patch` 当成默认的测试风格。
