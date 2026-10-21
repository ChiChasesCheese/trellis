// EXPECT: compile-fail
#include <memory>
#include <vector>
int main() {
    std::unique_ptr<int> a = std::make_unique<int>(1);
    std::unique_ptr<int> b = a;                        // copying a unique_ptr: the copy constructor is deleted
    return *b;
}
