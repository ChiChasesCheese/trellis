---
nodes: [problems.booking.library]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/library-management-system.md
---
# awesome-low-level-design — Designing a Library Management System

值得读：开源题库（GPL-3.0），六种语言各一份实现。题面把 `Book` 写成一个带 `availability status`
的扁平对象，但 `solutions/python/librarymanagementsystem/` 里的实现其实已经把 `LibraryItem`
和 `BookCopy` 分开了——**题面和代码不一致本身就值得看**：前者是大多数人凭印象写出来的样子，
后者是认真做一遍之后被迫走到的地方。

四处当反面教材最有价值。第一，它为图书／期刊建了继承树，基类上开一个 `get_author_or_publisher()`
抽象方法——图书返作者、期刊返出版者，三个子类行为完全相同，这是命名问题被当成了多态问题。
第二，预约用的是挂在书目上的**观察者列表**：还书时 `notify_observers()` 通知**所有**排队的人，
而 `OnHoldState.checkout` 允许**任何一个**曾经预约过的人取走——先来先到的承诺就此作废，队列
不是队列。第三，**保留没有到期时间**：一位读者预约了、通知收到了、再也没来，这本副本就永远停在
`OnHoldState`，馆里有书谁也借不到，而且没有任何代码能把它救回来。第四，失败路径一律是 `print`
（"Cannot return an item that is already available."），调用方既接不住也测不了。

此外它没有借期与到期日（`Loan` 只有 `checkout_date`）、没有罚金、没有续借、没有按读者类型的限额，
`date.today()` 直接写在 `Loan.__init__` 里因此无法注入时钟，`LibraryManagementSystem` 是
`get_instance()` 单例，还为检索建了一组 `SearchByXxxStrategy` 类。本题解相应地改成：书目与副本
分离、预约是真正的 FIFO 队列加带到期时刻的取书架、分配规则收敛成一个惰性 `_sweep`、
政策做成一张按 (读者类型, 介质) 查的表、失败路径是一个小异常层级。
