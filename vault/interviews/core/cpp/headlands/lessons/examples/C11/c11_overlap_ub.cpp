// EXPECT: run-fail
// C11: memcpy with overlapping ranges is undefined; AddressSanitizer checks it explicitly.
#include <cstring>
#include <iostream>

int main(int argc, char**) {
    char buf[16] = "abcdefghijklmno";
    std::memcpy(buf + argc, buf, 8 * argc);        // regions [1,9) and [0,8) overlap (runtime size: a real library call)
    std::cout << buf << "\n";
}
