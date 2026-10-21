// EXPECT: run-fail
// C09: a tour of what UBSan catches. UBSan keeps running after each report, so one run prints them all.
#include <climits>
#include <cstdint>
#include <cstring>
#include <iostream>

struct S { int field; };

int main(int argc, char**) {
    int n = 31 + argc;                        // 32 at run time
    std::cout << "shift: " << (1 << n) << "\n";                  // shift exponent 32 is too large for a 32-bit int
    int m = INT_MIN + argc - 1;               // INT_MIN
    std::cout << "division: " << m / (-argc) << "\n";            // INT_MIN / -1 overflows
    int zero = argc - 1;
    std::cout << "div by zero: " << 10 / zero << "\n";           // division by zero
    alignas(8) char buf[16] = {};
    std::cout << "misaligned: " << *reinterpret_cast<std::int64_t*>(buf + argc) << "\n";   // misaligned 8-byte load
    double d = 1e300 * argc;
    std::cout << "float->int: " << static_cast<int>(d) << "\n";  // out-of-range conversion
    bool b = false;
    unsigned char raw = static_cast<unsigned char>(2 + argc);
    std::memcpy(&b, &raw, 1);
    std::cout << "invalid bool: " << b << "\n";                   // a bool object holding 3
    S* sp = argc == 1 ? nullptr : new S{1};
    std::cout << "null member access: " << sp->field << "\n";    // reported by UBSan, then the SEGV kills us (so: last)
}
