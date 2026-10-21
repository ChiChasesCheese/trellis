// EXPECT: run-fail
// C09: lifetime bugs: use-after-free, double free, returning the address of a local.
#include <iostream>

int* dangling_local() { int x = 7; return &x; }          // clang warns here (-Wreturn-stack-address)

int main(int argc, char**) {
    int* p = new int(5);
    delete p;
    if (argc == 1) std::cout << "after delete: " << *p << "\n";      // use-after-free
    int* q = dangling_local();
    std::cout << "returned local address is " << (q ? "non-null" : "null") << " (reading it would be UB)\n";
    delete p;                                                          // double free
}
