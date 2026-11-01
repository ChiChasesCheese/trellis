---
id: hi-lld-design-principles-6-srp-ocp
node: lld.in-a-hurry.design-principles
type: qa
step: 6
---
## Q
**SRP 与 OCP：按变化原因拆分，用接口扩展**｜低层设计 · 速览

单一职责（SRP）和开闭原则（OCP）各是什么意思？请各举一个违反与修正的例子。

## A
**SRP。** 一个类只有一个变化的理由。Report 既生成内容、又画 PDF、又写文件，就应拆成 Report、PDFPrinter、FileStorage，PDF 库换了只改 PDFPrinter，存储换成数据库只改 FileStorage。

**OCP。** 对扩展开放，对修改关闭：加新行为不改旧代码。

```python
class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount: float) -> None: ...

class PaymentProcessor:
    def process(self, method: PaymentMethod, amount: float) -> None:
        method.process(amount)  # 加 CryptoPayment 只需新增一个类
```

违反例子：`process` 里 `if payment_type == "credit" ... elif "paypal"`，每加一种支付就要改这个方法，可能弄坏已有逻辑。
