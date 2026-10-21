// EXPECT: compile-fail
#include <string>
#include <vector>
struct Counter { int n = 0; void inc() { ++n; } };
void use(const Counter& c) { c.inc(); }                // calling a non-const member on a const reference
int main() { Counter c; use(c); }
