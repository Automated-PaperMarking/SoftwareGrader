#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) {
        return 0; 
    }
    printf("%d\n", n * n);
    return 0;
}
