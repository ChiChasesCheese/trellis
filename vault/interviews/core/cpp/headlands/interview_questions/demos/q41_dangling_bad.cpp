// EXPECTED TO FAIL under ASan (with stack-use-after-return detection): returning a reference to a local.
#include <cstdio>
#include <string>
const std::string& longest(const std::string& a, const std::string& b) {
    std::string tmp = a.size() >= b.size() ? a : b;
    return tmp;                          // reference to a local that dies at the closing brace
}
int main() {
    std::string x(30, 'x'), y(20, 'y');
    std::printf("%c\n", longest(x, y)[0]);
}
