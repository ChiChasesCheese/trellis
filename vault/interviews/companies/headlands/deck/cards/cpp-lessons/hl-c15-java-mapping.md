---
id: hl-c15-java-mapping
node: cpp-lessons.c15-io-performance
type: qa
step: 1
---
## Q
Java 的 `BufferedReader.readLine`、`Scanner.nextInt`、`String.split`、`Integer.parseInt`、`System.out.println`、`String.format("%.2f")` 在 C++ 里分别对应什么？

## A
- `BufferedReader.readLine()` ↔ `std::getline(std::cin, line)`
- `Scanner.nextInt()`（慢）↔ `std::cin >> x`（也慢）；快：`from_chars` / `fread`
- `String.split(" ")` ↔ 手写切分（返回 `string_view`）或 `istringstream`
- `Integer.parseInt` ↔ `std::stoi`（抛异常）、`strtol`、`std::from_chars`（无异常、最快）
- `System.out.println`（带刷新）↔ `std::cout << x << '\n'`（不刷新）
- `String.format("%.2f")` ↔ `std::fixed << std::setprecision(2)`、`printf("%.2f")`、`std::format`
