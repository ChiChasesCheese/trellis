// EXPECT: compile-fail
#include <string>
#include <vector>
int add(int a, int b) { return a + b; }
int main() {
    std::vector<int> v{1, 2};
    return add(v, 2);                                  // vector<int> is not an int
}
