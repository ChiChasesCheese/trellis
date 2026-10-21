// EXPECT: compile-fail
#include <algorithm>
#include <list>
int main() {
    std::list<int> l{3, 1, 2};
    std::sort(l.begin(), l.end());                     // std::sort needs random-access iterators; use l.sort()
}
