// C05: std::vector = ArrayList<T> that stores T itself (not references), with a capacity you can see and control.
#include <algorithm>
#include <array>
#include <iostream>
#include <vector>

// [[snip:growth]]
void growth() {
    std::vector<int> v;
    std::size_t last_cap = v.capacity();
    std::cout << "  capacity trace (push_back 0..1000):";
    int reallocations = 0;
    for (int i = 0; i < 1000; ++i) {
        v.push_back(i);
        if (v.capacity() != last_cap) {          // each change = new block allocated, elements moved, old block freed
            last_cap = v.capacity();
            ++reallocations;
            if (reallocations <= 12) std::cout << " " << last_cap;
        }
    }
    std::cout << " ... total " << reallocations << " reallocations\n";
    std::vector<int> r;
    r.reserve(1000);
    for (int i = 0; i < 1000; ++i) r.push_back(i);
    std::cout << "  with reserve(1000): capacity " << r.capacity() << ", reallocations 0\n";
}
// [[/snip]]

// [[snip:erase]]
void erase_idioms() {
    std::vector<int> v{5, 3, 8, 3, 9, 3, 1};
    v.erase(std::remove(v.begin(), v.end(), 3), v.end());          // erase-remove idiom (C++20: std::erase(v, 3))
    std::cout << "  after erase-remove(3):";
    for (int x : v) std::cout << " " << x;
    std::cout << "\n";
    std::vector<int> w{1, 2, 3, 4, 5, 6};
    std::erase_if(w, [](int x) { return x % 2 == 0; });            // C++20
    std::cout << "  after erase_if(even):";
    for (int x : w) std::cout << " " << x;
    std::cout << "\n";
}
// [[/snip]]

// [[snip:bool]]
void vector_bool_trap() {
    std::vector<bool> flags(10);
    auto first = flags[0];            // NOT a bool&: a proxy object that points into a bit-packed word
    flags[0] = true;
    std::cout << "  vector<bool>::operator[] returns a proxy; the proxy taken before the write now reads " << static_cast<bool>(first)
              << " (it aliases the vector, it is not a copy)\n";
    // bool* p = &flags[0];           // does not compile: there is no address of a bit
}
// [[/snip]]

int main() {
    growth();
    erase_idioms();
    vector_bool_trap();
    std::array<int, 4> a{1, 2, 3, 4};                // fixed size, lives where it is declared (stack here), no allocation
    std::cout << "  sizeof(std::array<int,4>)=" << sizeof(a) << " (exactly 4 ints, no header, no pointer)\n";
    std::vector<int> v;
    std::cout << "  sizeof(std::vector<int>)=" << sizeof(v) << " (three pointers: begin, end, end-of-capacity)\n";
}
