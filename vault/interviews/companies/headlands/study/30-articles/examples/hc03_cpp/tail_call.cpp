// Does the compiler turn recursion into a loop?  Try:  ./a.out tail|musttail|plain 100000000
//   -O0: tail and plain crash (stack overflow), musttail works.   -O2: all three print the sum.
// The standard promises none of this; [[clang::musttail]] (clang only) makes the tail call mandatory.
#include <cstdlib>
#include <iostream>
#include <string>

long long sum_tail(long long n, long long acc) {
    if (n == 0) return acc;
    return sum_tail(n - 1, acc + n);          // last action of the function: a tail call
}

long long sum_musttail(long long n, long long acc) {
    if (n == 0) return acc;
    [[clang::musttail]] return sum_musttail(n - 1, acc + n);   // compile error if it cannot be a jump
}

long long sum_plain(long long n) {            // NOT a tail call: the add happens after the call returns
    if (n == 0) return 0;
    return n + sum_plain(n - 1);
}

int main(int argc, char** argv) {
    std::string mode = argc > 1 ? argv[1] : "tail";
    long long n = argc > 2 ? std::atoll(argv[2]) : 1000;
    if (mode == "tail") std::cout << sum_tail(n, 0) << "\n";
    else if (mode == "musttail") std::cout << sum_musttail(n, 0) << "\n";
    else std::cout << sum_plain(n) << "\n";
}
