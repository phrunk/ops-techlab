#include <stdlib.h>
#include <string.h>

int main() {
  const int BUF_SIZE = 1024*1024*1024;

  void* buf = malloc(BUF_SIZE);
  memset(buf, 0, BUF_SIZE);
  for (;;) {
    sleep(1);
  }

  return 0;
}
