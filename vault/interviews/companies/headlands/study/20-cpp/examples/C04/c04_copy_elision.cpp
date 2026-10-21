// EXPECT: warn
// C04: copy elision. C++17 guarantees it for prvalues; NRVO is allowed but optional. `return std::move(x)` hurts.
#include <iostream>
#include <string>
#include <utility>

struct Heavy {
    std::string tag;
    explicit Heavy(std::string t) : tag(std::move(t)) { std::cout << "    ctor " << tag << "\n"; }
    Heavy(const Heavy& o) : tag(o.tag) { std::cout << "    COPY " << tag << "\n"; }
    Heavy(Heavy&& o) noexcept : tag(std::move(o.tag)) { std::cout << "    move\n"; }
};

struct Pinned {                                  // neither copyable nor movable
    int v;
    explicit Pinned(int x) : v(x) { std::cout << "    Pinned ctor\n"; }
    Pinned(const Pinned&) = delete;
    Pinned(Pinned&&) = delete;
};

// [[snip:forms]]
Pinned make_pinned() { return Pinned(7); }       // C++17: guaranteed elision, so a non-movable type can be returned
Heavy make_prvalue() { return Heavy("prvalue"); }            // no copy, no move: constructed in the caller's slot
Heavy make_nrvo() { Heavy h("nrvo"); return h; }             // named return: NRVO (optional, but every compiler does it here)
Heavy make_pessimized() { Heavy h("pessimized"); return std::move(h); }   // BAD: blocks NRVO, forces a move
Heavy make_two_paths(bool f) {                               // two different locals: NRVO is impossible -> move (implicit)
    Heavy a("path-a"), b("path-b");
    if (f) return a;
    return b;
}
// [[/snip]]

int main() {
    std::cout << "  guaranteed elision, non-movable type:\n";
    Pinned p = make_pinned();
    std::cout << "    p.v=" << p.v << "\n";
    std::cout << "  prvalue:\n";   Heavy h1 = make_prvalue();
    std::cout << "  NRVO:\n";      Heavy h2 = make_nrvo();
    std::cout << "  return std::move(local):\n"; Heavy h3 = make_pessimized();
    std::cout << "  two candidate locals:\n";    Heavy h4 = make_two_paths(true);
}
