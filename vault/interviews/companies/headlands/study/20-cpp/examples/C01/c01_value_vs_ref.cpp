// C01: value semantics. A C++ object IS its bytes; a Java object is a reference to a heap object.
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

struct Point {          // Java: class Point { int x, y; }  (a heap object behind a reference)
    int x = 0;
    int y = 0;
};

// [[snip:copy]]
void demo_copy() {
    Point a{1, 2};
    Point b = a;        // COPY: b is a second, independent Point (Java: both would name one object)
    b.x = 99;
    std::cout << "a.x=" << a.x << " b.x=" << b.x << "\n";            // 1 and 99

    Point& r = a;       // reference = another name for the SAME object (closest to Java's reference)
    r.x = 7;
    std::cout << "a.x=" << a.x << " (changed through r)\n";           // 7
}
// [[/snip]]

// [[snip:layout]]
void demo_layout() {
    std::vector<Point> v(4);                       // one contiguous block: 4 * sizeof(Point) bytes
    std::cout << "sizeof(Point)=" << sizeof(Point) << "\n";
    for (int i = 1; i < 4; ++i) {
        auto d = reinterpret_cast<std::uintptr_t>(&v[i]) - reinterpret_cast<std::uintptr_t>(&v[i - 1]);
        std::cout << "&v[" << i << "] - &v[" << i - 1 << "] = " << d << " bytes\n";
    }
    // Java's Point[] holds 4 references; each Point is a separate heap object with a 12-16 byte header.
}
// [[/snip]]

// [[snip:value_in_value]]
struct Order {
    std::string symbol;   // the std::string object lives INSIDE Order (its characters may be on the heap)
    Point where;          // Point lives inside Order too: no pointer, no header
    long qty;
};

void demo_nested() {
    Order o{"AAPL", {3, 4}, 100};
    Order copy = o;                  // deep copy by default: symbol is copied, too
    copy.symbol = "MSFT";
    std::cout << o.symbol << " vs " << copy.symbol << "; sizeof(Order)=" << sizeof(Order) << "\n";
}
// [[/snip]]

int main() {
    demo_copy();
    demo_layout();
    demo_nested();
}
