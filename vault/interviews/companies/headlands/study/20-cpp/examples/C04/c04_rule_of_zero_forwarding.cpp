// C04: rule of zero, plus perfect forwarding (what emplace_back does) and "sink parameter" style.
#include <iostream>
#include <memory>
#include <string>
#include <type_traits>
#include <utility>
#include <vector>

// [[snip:zero]]
// Rule of zero: every member already manages itself, so write NO special member functions.
struct Account {
    std::string name;
    std::vector<int> history;
    std::unique_ptr<int> secret = std::make_unique<int>(7);     // makes the class move-only automatically
};
static_assert(std::is_nothrow_move_constructible_v<Account>);
static_assert(!std::is_copy_constructible_v<Account>);          // unique_ptr member deletes the copy
// [[/snip]]

// [[snip:sink]]
class Person {
    std::string name_;
public:
    explicit Person(std::string name) : name_(std::move(name)) {}   // sink: by value, then move. One move for rvalues,
                                                                    // one copy + one move for lvalues. Simple and fast enough.
    const std::string& name() const { return name_; }
};
// [[/snip]]

// [[snip:forward]]
template <class T>
struct Recorder {
    std::vector<T> items;
    template <class... Args>
    void emplace(Args&&... args) {                       // Args&& here is a FORWARDING reference
        items.emplace_back(std::forward<Args>(args)...); // keeps lvalue-ness / rvalue-ness of each argument
    }
};

struct Trade {
    std::string sym; int qty; double px;
    Trade(std::string s, int q, double p) : sym(std::move(s)), qty(q), px(p) { std::cout << "  Trade built in place\n"; }
    Trade(const Trade&) { std::cout << "  Trade COPY\n"; }
    Trade(Trade&&) noexcept { std::cout << "  Trade move\n"; }
};
// [[/snip]]

int main() {
    Account a;
    Account b = std::move(a);
    std::cout << "moved Account holds secret=" << *b.secret << ", source secret is " << (a.secret ? "set" : "null") << "\n";

    std::string n = "alice";
    Person p1(n);                    // copy then move
    Person p2(std::move(n));         // move then move
    std::cout << p1.name() << " " << p2.name() << " n.size() after move: " << n.size() << "\n";

    Recorder<Trade> r;
    r.items.reserve(4);
    std::cout << "emplace with constructor arguments:\n";
    r.emplace("AAPL", 100, 187.5);
    std::cout << "push_back(Trade(...)) temporary:\n";
    r.items.push_back(Trade("MSFT", 50, 410.0));
    std::cout << "emplace_back(Trade(...)) still builds a temporary first:\n";
    r.items.emplace_back(Trade("NVDA", 10, 900.0));
}
