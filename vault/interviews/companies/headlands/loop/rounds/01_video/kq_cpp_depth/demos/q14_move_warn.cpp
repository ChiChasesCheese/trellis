// EXPECTED WARNING: return std::move(local) blocks copy elision.
#include <string>
std::string bad() { std::string s(50, 'x'); return std::move(s); }
std::string good() { std::string s(50, 'x'); return s; }
int main() { return static_cast<int>(bad().size() + good().size()) - 100; }
