// EXPECTED TO FAIL: the same mistake without a concept errors inside the template body.
template <class T> double mark(const T& t) { return t.price(); }
struct Rock {};
int main() { return static_cast<int>(mark(Rock{})); }
