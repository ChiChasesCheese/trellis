---
id: tr-test-infra-framework-architecture-extend
node: test-infra.framework-architecture
type: qa
step: 4
---
## Q
"新特性加测试只需要写一层"在测试框架里具体怎么做到？举一个给推理服务加新配置的例子。

## A
做法是**把变化的东西变成数据**，测试逻辑只写一次，配置矩阵决定它跑几次。

例：一个推理服务（把训练好的模型部署成在线服务，模型是一大组数字参数加一串计算步骤）新增一种"量化"配置。量化（quantization）是把模型参数从 16 位数字压成 8 位，省一半内存，结果会略有不同。不该做的是把已有 200 条测试各复制一份。该做的是：

1. **配置文件加一行**，测试逻辑不动：

```yaml
# configs/serving.yaml
- {name: bf16-base, dtype: bf16, max_batch: 64}
- {name: fp8-quant, dtype: fp8,  max_batch: 128, rtol: 0.05}
```

2. **框架用钩子把配置展开成参数**：

```python
def pytest_generate_tests(metafunc):
    if "serving_cfg" in metafunc.fixturenames:
        cfgs = load_yaml("configs/serving.yaml")
        metafunc.parametrize("serving_cfg", cfgs, ids=[c["name"] for c in cfgs])
```

3. **判定层读取配置里的容差**：`rtol` 放在配置中，判定函数统一用它，测试函数里不写数字。
4. **新特性独有的行为**才写新测试，例如"量化模型的内存占用比基线少 40% 以上"。

**几个扩展点要预留**：
- **驱动适配器接口**：新硬件或新部署方式实现同一个接口，例如 `start() / generate() / metrics() / stop()`；
- **资源声明**：测试用 marker 声明需要什么（`@pytest.mark.needs(devices=8)`），调度层据此安排，测试不写机器名；
- **判定插件**：新的比较方式（如按分布比较）注册进判定层，所有测试都能用。

衡量标准：加一个配置，改动应该只在配置文件和（必要时）一个适配器里，评审一眼看完。
