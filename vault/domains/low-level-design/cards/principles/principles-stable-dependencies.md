---
id: principles-stable-dependencies
node: principles.coupling
type: cloze
step: 4
---
耦合有方向。**传入耦合（Afferent Coupling）** Ca = {{c1::依赖这个组件的类的数量}}（传入的，难以改变，因为改了会连累依赖它的一切）；**传出耦合（Efferent Coupling）** Ce = {{c2::这个组件依赖的类的数量}}（传出的，相对容易改）。不稳定性 I = {{c3::Ce / (Ca + Ce)}}，所以 I = 0 是最稳定，I = 1 是最不稳定。**稳定依赖原则**：依赖方向应该指向{{c4::更稳定的组件}}——易变的代码可以依赖稳定的代码，反过来不行。当箭头必须反过来指时，修复方法是{{c5::由更稳定、更高层的一方定义抽象接口}}，让易变的具体实现反过来依赖这个接口。
