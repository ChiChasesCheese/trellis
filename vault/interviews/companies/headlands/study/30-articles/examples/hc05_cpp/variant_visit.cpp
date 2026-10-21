// std::variant + std::visit: a closed set of event types and a visitor the compiler checks for completeness.
#include <iostream>
#include <string>
#include <variant>

struct Trade { long long px; long long qty; };
struct Rested { long long px; long long qty; };
struct Cancelled { long long remaining; };
using Event = std::variant<Trade, Rested, Cancelled>;

template <class... Ts>
struct overloaded : Ts... { using Ts::operator()...; };
template <class... Ts>
overloaded(Ts...) -> overloaded<Ts...>;

std::string render(const Event& e) {
    return std::visit(overloaded{
                          [](const Trade& t) { return "TRADE " + std::to_string(t.qty) + " @ " + std::to_string(t.px); },
                          [](const Rested& r) { return "REST " + std::to_string(r.qty) + " @ " + std::to_string(r.px); },
                          [](const Cancelled& c) { return "CANCEL " + std::to_string(c.remaining); },
                          // Add a fourth alternative to Event and delete nothing here: this call stops compiling,
                          // because std::visit requires the visitor to accept EVERY alternative.
                      },
                      e);
}

int main() {
    for (const Event& e : {Event{Trade{101, 5}}, Event{Rested{99, 3}}, Event{Cancelled{2}}}) std::cout << render(e) << "\n";
    const Event e = Trade{1, 2};
    if (const auto* t = std::get_if<Trade>(&e)) std::cout << "get_if: trade of " << t->qty << "\n";  // one alternative, no visitor
}
