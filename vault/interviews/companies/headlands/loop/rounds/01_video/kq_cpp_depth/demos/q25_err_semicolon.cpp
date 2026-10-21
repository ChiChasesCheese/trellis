#include <cstdio>
struct Tick {
    int px;
    int qty;
}                                       // missing semicolon after the struct
int main() { Tick t{1, 2}; std::printf("%d\n", t.px); }
