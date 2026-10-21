// EXPECT: run-fail
// C09: out-of-bounds access. operator[] does not check. at() throws. Raw arrays and vectors both corrupt memory silently.
#include <iostream>
#include <stdexcept>
#include <vector>

int main(int argc, char**) {
    std::vector<int> v{10, 20, 30};
    try { std::cout << v.at(5) << "\n"; }
    catch (const std::out_of_range& e) { std::cout << "at(5) threw: " << e.what() << "\n"; }
    int idx = 2 + argc;                         // == 3, one past the end
    std::cout << "v[3] = " << v[idx] << "\n";   // heap-buffer-overflow (ASan), silent garbage without it
    int arr[4] = {1, 2, 3, 4};
    std::cout << "arr[4] = " << arr[idx + 1] << "\n";
}
