---
id: foundations-latency-sequential-reads
node: foundations.numbers
type: cloze
---
Reading 1 MB sequentially: from memory {{c1::~10–50 µs}}, from SSD {{c2::~200 µs–1 ms}} — sequential I/O is close enough to memory speed that {{c3::append-only / log-structured}} designs deliberately trade random writes for sequential ones.


## zh
顺序读 1 MB：从内存 {{c1::~10–50 µs}}，从 SSD {{c2::~200 µs–1 ms}}——顺序 I/O 已经接近内存速度，所以{{c3::append-only / log-structured}} 这类设计才会刻意拿随机写换顺序写。
