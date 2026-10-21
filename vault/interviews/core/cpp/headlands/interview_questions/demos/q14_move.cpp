// Move semantics: what std::move really does, rule of five, noexcept and vector growth, copy elision.
#include <cstdio>
#include <string>
#include <utility>
#include <vector>

struct Buf {
    int* data; std::size_t n;
    static inline int copies = 0, moves = 0;
    explicit Buf(std::size_t n_) : data(new int[n_]()), n(n_) {}
    ~Buf() { delete[] data; }
    Buf(const Buf& o) : data(new int[o.n]), n(o.n) { for (std::size_t i = 0; i < n; ++i) data[i] = o.data[i]; ++copies; }
    Buf(Buf&& o) noexcept : data(o.data), n(o.n) { o.data = nullptr; o.n = 0; ++moves; }       // steal
    Buf& operator=(Buf o) noexcept { std::swap(data, o.data); std::swap(n, o.n); return *this; }   // copy-and-swap
};
struct BufThrowingMove {                                      // same, but the move constructor is not noexcept
    Buf b;
    explicit BufThrowingMove(std::size_t n) : b(n) {}
    BufThrowingMove(const BufThrowingMove& o) : b(o.b) {}
    BufThrowingMove(BufThrowingMove&& o) : b(std::move(o.b)) {}
};

struct Tracer {
    static inline int ctor = 0, copy = 0, move = 0;
    Tracer() { ++ctor; }
    Tracer(const Tracer&) { ++copy; }
    Tracer(Tracer&&) noexcept { ++move; }
};
Tracer make_prvalue() { return Tracer(); }                    // C++17: guaranteed elision, nothing to copy
Tracer make_named() { Tracer t; return t; }                   // NRVO: allowed, clang does it
struct Pinned { Pinned() = default; Pinned(const Pinned&) = delete; Pinned(Pinned&&) = delete; };
Pinned make_pinned() { return Pinned(); }                     // compiles in C++17 only because of guaranteed elision

void report(const char* label) {
    std::printf("%-28s ctor=%d copy=%d move=%d\n", label, Tracer::ctor, Tracer::copy, Tracer::move);
    Tracer::ctor = Tracer::copy = Tracer::move = 0;
}

int main() {
    std::string a(40, 'a');
    std::string b = std::move(a);                             // std::move is only a cast to rvalue
    std::printf("after move: a.size()=%zu (valid but unspecified), b.size()=%zu\n", a.size(), b.size());
    const std::string c(40, 'c');
    std::string d = std::move(c);                             // const rvalue: binds the COPY constructor
    std::printf("move from const: c.size()=%zu (still full: it was copied)\n", c.size());

    Buf::copies = Buf::moves = 0;
    std::vector<Buf> v;
    for (int i = 0; i < 8; ++i) v.emplace_back(100);
    std::printf("vector<Buf> noexcept move  : copies=%d moves=%d\n", Buf::copies, Buf::moves);
    Buf::copies = Buf::moves = 0;
    std::vector<BufThrowingMove> w;
    for (int i = 0; i < 8; ++i) w.emplace_back(100);
    std::printf("vector, move not noexcept  : copies=%d moves=%d\n", Buf::copies, Buf::moves);

    { Tracer t = make_prvalue(); (void)t; } report("return prvalue");
    { Tracer t = make_named();   (void)t; } report("return named local (NRVO)");
    { Pinned p = make_pinned();  (void)p; }
    std::printf("Pinned (no copy, no move) returned by value: compiles\n");
}
