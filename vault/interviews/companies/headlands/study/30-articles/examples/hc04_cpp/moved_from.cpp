// The implicitly generated move constructor moves each member.  For `int` "move" is just copy,
// so the moved-from object keeps its counters but loses its buffer.
#include <iostream>
#include <utility>
#include <vector>

struct Broken {
    std::vector<long long> buf;
    std::size_t size = 0;
    Broken() = default;
    Broken(Broken&&) = default;            // moves buf, copies size
};

struct Fixed {
    std::vector<long long> buf;
    std::size_t size = 0;
    Fixed() = default;
    Fixed(Fixed&& o) noexcept : buf(std::move(o.buf)), size(std::exchange(o.size, 0)) { o.buf.clear(); }
};

int main() {
    Broken a;
    a.buf = {1, 2, 3};
    a.size = 3;
    Broken b = std::move(a);
    std::cout << "Broken: moved-from claims size " << a.size << " but holds " << a.buf.size() << " elements\n";

    Fixed c;
    c.buf = {1, 2, 3};
    c.size = 3;
    Fixed d = std::move(c);
    std::cout << "Fixed:  moved-from claims size " << c.size << " and holds " << c.buf.size() << " elements\n";
}
