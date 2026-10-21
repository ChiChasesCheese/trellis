// stdin -> stdout: first line the initial value, then instructions; prints one line per query and the final register.
#include <iostream>
#include <string>

#include IMPL_HEADER

int main() {
    std::ios::sync_with_stdio(false);
    std::vector<std::string> lines;
    for (std::string line; std::getline(std::cin, line);) lines.push_back(line);
    for (const std::string& out : regsim::solve(lines)) std::cout << out << '\n';
    return 0;
}
