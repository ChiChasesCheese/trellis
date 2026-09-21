%% trellis:begin %%
# 导入系统：模块对象、`sys.modules`、包与循环导入
*解释器与执行模型*

掌握模块只执行一次并缓存于 `sys.modules`、`__init__.py` 与命名空间包、相对导入，以及循环导入的成因与三种解法。

**Requires:** [[domains/python/map/runtime.compile-bytecode|从源码到字节码：编译、`code` 对象、`dis` 与 `.pyc` 缓存]]

## Readings
- [[effective-14-collaboration|Effective Python 3e · 第 14 章 协作]]
- [[pydocs-import-system|导入系统（import system）完整机制]]
- [[pydocs-sys-module|sys 模块：解释器内部状态入口]]
- [[pydocs-tutorial-modules|Python 教程第 6 章：模块]]

## Drills
- [[runtime-explain-the-traceback-and-the-import-cycle|Drill：解释一个循环导入报错，再解释一个「异常被吞掉」的 traceback]]

## Cards (6)
1. [[circular-import-partial-module-and-fixes]]
2. [[finder-returns-spec-loader-executes]]
3. [[module-executes-once-via-sys-modules-cache]]
4. [[regular-vs-namespace-package]]
5. [[relative-import-dot-syntax]]
6. [[sys-modules-inserted-before-exec-breaks-recursion]]
%% trellis:end %%

## Notes
