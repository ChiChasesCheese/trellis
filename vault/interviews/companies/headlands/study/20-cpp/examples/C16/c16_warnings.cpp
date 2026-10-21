// EXPECT: warn
// C16: -Wall -Wextra warnings worth fixing during the interview: each one usually points at a real bug.
#include <iostream>
#include <vector>

int sum_to(const std::vector<int>& v, int n) {
    int total = 0;
    for (int i = 0; i < v.size(); ++i)        // -Wsign-compare: int vs size_t
        total += v[i];
    int unused = 0;                           // -Wunused-variable
    if (n > 0)
        return total;
}                                             // -Wreturn-type: control reaches end of non-void function (UB if n <= 0)

int main(int argc, char**) {                  // -Wunused-parameter would fire for named but unused params
    int x;
    if (argc > 5) x = 1;
    std::cout << x << " " << sum_to({1, 2}, 1) << "\n";   // -Wsometimes-uninitialized
}
