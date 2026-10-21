// HackerRank shape: stdin -> stdout.  The statement requires exit status 0 even when the input is malformed.
#include <iostream>

#include IMPL_HEADER

int main() {
    std::ios::sync_with_stdio(false);
    return jobchains::run(std::cin, std::cout);
}
