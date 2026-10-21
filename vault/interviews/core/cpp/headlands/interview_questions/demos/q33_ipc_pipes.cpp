// Pipe and socketpair between a parent and a forked child.
#include <cstdio>
#include <cstring>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>

int main() {
    int pfd[2];
    if (pipe(pfd) != 0) return 1;
    pid_t pid = fork();
    if (pid == 0) {                                  // child: writer
        close(pfd[0]);
        const char msg[] = "price=190.25";
        write(pfd[1], msg, sizeof msg);
        close(pfd[1]);
        _exit(0);
    }
    close(pfd[1]);                                   // parent: reader
    char buf[64] = {};
    ssize_t n = read(pfd[0], buf, sizeof buf);
    close(pfd[0]);
    waitpid(pid, nullptr, 0);
    std::printf("pipe: parent read %zd bytes: \"%s\"\n", n, buf);

    int sv[2];
    socketpair(AF_UNIX, SOCK_STREAM, 0, sv);         // bidirectional
    if (fork() == 0) {
        close(sv[0]);
        char req[16] = {};
        read(sv[1], req, sizeof req);
        std::strcat(req, "-ack");
        write(sv[1], req, std::strlen(req) + 1);
        _exit(0);
    }
    close(sv[1]);
    write(sv[0], "ping", 5);
    char rep[32] = {};
    read(sv[0], rep, sizeof rep);
    wait(nullptr);
    std::printf("socketpair: round trip \"%s\"\n", rep);
}
