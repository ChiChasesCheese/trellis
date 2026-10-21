// EXPECT: run-fail
// RUN: ASAN_OPTIONS=alloc_dealloc_mismatch=1:symbolize=0 $BIN
// C10: pairing rules: new/delete, new[]/delete[], malloc/free. Crossing them is UB.
#include <cstdlib>
#include <iostream>

int main() {
    int* a = new int[8];
    delete a;                       // should be delete[] : ASan "alloc-dealloc-mismatch"
    std::cout << "survived the mismatched delete\n";
}
