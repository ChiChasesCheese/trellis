#pragma once
int square(int x);                 // declaration only: the definition lives in q03_lib.cpp
inline int twice(int x) { return 2 * x; }   // `inline`: every TU may carry the definition
