// EXPECT: compile-fail
#include <iostream>
#include <vector>
int main() {
    std::vector<int> v{1, 2, 3};
    std::cout << std::accumulate(v.begin(), v.end(), 0) << "\n";   // <numeric> not included
}
