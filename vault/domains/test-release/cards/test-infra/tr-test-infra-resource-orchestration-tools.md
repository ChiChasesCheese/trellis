---
id: tr-test-infra-resource-orchestration-tools
node: test-infra.resource-orchestration
type: qa
step: 4
---
## Q
"给每个团队固定分几台测试机"和"所有设备进一个池子按需租用"相比各有什么优缺点？常见工具里怎么表达"这个作业需要 2 台某类设备"？

## A
**固定分配**：
- 优点：简单，团队清楚自己的机器状态，调试时可以登录上去长期占用。
- 缺点：利用率低，夜里闲着、白天不够；坏了没人发现；机器状态被手工改得各不相同，测试结果不可复现。

**共享池按需租用**：
- 优点：利用率高，设备统一由脚本部署和清理，状态一致；坏机器能自动发现。
- 缺点：要建设调度、排队、清理和健康检查；手工调试需要单独的"调试租约"（时间更长、结束后重装系统）。

实际常见是**池子为主、留少量调试机**。

**几种工具的写法**：
- **Jenkins（Lockable Resources 插件）**：

```groovy
lock(label: 'hw-a', quantity: 2, variable: 'DEVS') {
    sh "pytest -m hardware --devices=${env.DEVS}"
}
```
所需设备都被占用时，作业在队列里等待。

- **Kubernetes**：设备插件（device plugin）把设备登记为扩展资源，Pod 里声明 `resources.limits: {nvidia.com/gpu: 2}`，调度器只把它放到有 2 块空闲 GPU 的节点上。
- **Slurm**（高性能计算集群常用的作业调度器）：`srun --gres=gpu:2 pytest ...`，`--time=60` 限定最长分钟数。
- **自研测试框架**：测试用 marker 声明需求，例如 `@pytest.mark.needs(kind="hw-a", count=2)`，编排器读取后去资源服务申请。

不论哪种工具，判断标准相同：测试只声明"需要什么"，由调度系统决定"用哪台"。
