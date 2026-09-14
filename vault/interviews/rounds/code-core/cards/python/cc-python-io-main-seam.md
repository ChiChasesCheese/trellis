---
id: cc-python-io-main-seam
node: python.io
type: qa
---
## Q
The grader runs your file as a script, but your tests want to drive the logic directly with no subprocess. What signature makes both work?

## A
```python
def main(stdin=sys.stdin, stdout=sys.stdout) -> None: ...

if __name__ == "__main__":
    main()
```

- Passing the streams as **defaulted parameters** lets a test hand in `io.StringIO(sample)` and read the answer back from another `StringIO` — no files, no subprocess, no monkeypatching of `sys.stdin`.
- The `__main__` guard keeps `import` free of side effects; without it, importing the module inside a test consumes the test runner's stdin and hangs.
- Keep `main` to three statements — read, dispatch, write — with all logic in pure functions ([[cc-python-io-part-dispatch]]).

## Q zh
评测机把你的文件当脚本运行，而你的测试想不起子进程、直接驱动逻辑。什么样的签名能同时满足两者？

## A zh
```python
def main(stdin=sys.stdin, stdout=sys.stdout) -> None: ...

if __name__ == "__main__":
    main()
```

- 把两个流作为**带默认值的参数**传入，测试就能塞进 `io.StringIO(sample)`，再从另一个 `StringIO` 读回答案 —— 不用文件、不起子进程、也不用 monkeypatch `sys.stdin`。
- `__main__` 守卫让 `import` 没有副作用；没有它，测试里 import 这个模块会吞掉 runner 的 stdin 并卡死。
- 把 `main` 控制在三条语句 —— 读、分派、写 —— 逻辑全放在纯函数里（[[cc-python-io-part-dispatch]]）。
