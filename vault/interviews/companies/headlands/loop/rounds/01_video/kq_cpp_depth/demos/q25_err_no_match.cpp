#include <string>
#include <vector>
void place(std::string sym, int qty, double px);
int main() {
    place("AAPL", 100);               // missing the third argument
    std::vector<int> v;
    v.push_back("seven");             // wrong element type
}
