// EXPECT: compile-fail
#include <iostream>
struct Point { int x, y; }                             // missing ';' after the class definition
int main() {
    Point p{1, 2};
    std::cout << p.x << "\n";
}
