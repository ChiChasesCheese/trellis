// std::sort needs a STRICT weak order: comp(x, x) must be false.  `<=` is not one; with many equal keys it can make std::sort
// read past the end of the array.  This program only checks the property; it never sorts with the bad comparator.
#include <iostream>

int main() {
    auto good = [](long long a, long long b) { return a < b; };
    auto bad = [](long long a, long long b) { return a <= b; };
    std::cout << "good(5, 5) = " << good(5, 5) << "   (irreflexive: required)\n";
    std::cout << "bad(5, 5)  = " << bad(5, 5) << "   (violates the requirement: undefined behaviour inside std::sort)\n";
    // Two equal elements would each claim to come before the other:
    std::cout << "bad(5, 5) && bad(5, 5) says 5 is before 5, and 5 is before 5, at once\n";
}
