// C04: move semantics. std::move is a cast; the move constructor is where resources change hands.
#include <cstring>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

// [[snip:buffer]]
class Buffer {
    char* data_ = nullptr;
    std::size_t n_ = 0;
public:
    explicit Buffer(std::size_t n) : data_(new char[n]()), n_(n) { std::cout << "  ctor(" << n << ")\n"; }
    ~Buffer() { delete[] data_; }

    Buffer(const Buffer& o) : data_(new char[o.n_]), n_(o.n_) {            // copy: allocate + copy bytes: O(n)
        std::memcpy(data_, o.data_, n_);
        std::cout << "  COPY(" << n_ << ")\n";
    }
    Buffer(Buffer&& o) noexcept : data_(o.data_), n_(o.n_) {              // move: steal the pointer: O(1)
        o.data_ = nullptr; o.n_ = 0;
        std::cout << "  move(" << n_ << ")\n";
    }
    Buffer& operator=(const Buffer& o) {
        if (this != &o) { Buffer tmp(o); swap(tmp); }                      // copy-and-swap: strong guarantee
        return *this;
    }
    Buffer& operator=(Buffer&& o) noexcept {
        if (this != &o) { delete[] data_; data_ = o.data_; n_ = o.n_; o.data_ = nullptr; o.n_ = 0; }
        return *this;
    }
    void swap(Buffer& o) noexcept { std::swap(data_, o.data_); std::swap(n_, o.n_); }
    std::size_t size() const { return n_; }
};
// [[/snip]]

// [[snip:moved_from]]
void moved_from_state() {
    std::string s(40, 'a');
    std::string t = std::move(s);                      // s is "valid but unspecified"
    std::cout << "  t.size()=" << t.size() << "  s.size()=" << s.size() << " (usually empty, but unspecified: do not rely on it)\n";
    s = "reuse is fine";                                // assigning to a moved-from object is always allowed
    std::cout << "  s=" << s << "\n";
}
// [[/snip]]

// [[snip:growth]]
// vector growth uses move only if the move constructor is noexcept (otherwise it copies to keep the strong guarantee)
struct Loud {
    Loud() = default;
    Loud(const Loud&) { std::cout << "c"; }
    Loud(Loud&&) noexcept { std::cout << "m"; }
};
struct LoudThrowing {
    LoudThrowing() = default;
    LoudThrowing(const LoudThrowing&) { std::cout << "c"; }
    LoudThrowing(LoudThrowing&&) { std::cout << "m"; }   // NOT noexcept
};
template <class T>
void grow(const char* name) {
    std::vector<T> v;
    std::cout << "  " << name << " growth sequence: ";
    for (int i = 0; i < 4; ++i) v.emplace_back();        // reallocation relocates the old elements
    std::cout << "\n";
}
// [[/snip]]

int main() {
    std::cout << "[copy vs move]\n";
    // [[snip:main]]
    Buffer a(1 << 20);
    Buffer b = a;                       // copy
    Buffer c = std::move(a);            // move: a is now empty
    std::cout << "  a.size()=" << a.size() << " c.size()=" << c.size() << "\n";
    std::vector<Buffer> v;
    v.reserve(3);
    v.push_back(Buffer(8));             // rvalue argument: moves
    v.push_back(b);                     // lvalue argument: copies
    v.push_back(std::move(b));          // explicit move
    // [[/snip]]
    std::cout << "[moved-from std::string]\n"; moved_from_state();
    std::cout << "[relocation on growth: c = copy, m = move]\n";
    grow<Loud>("noexcept move   ");
    grow<LoudThrowing>("throwing move   ");
}
