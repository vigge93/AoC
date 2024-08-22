#include <math.h>
#include <string.h>
#include <stdio.h>
#include "Timer.h"

int hash_str(char* str) {
    int hash = 0;
    for (int i = 0; i < strlen(str); i++) {
        hash += str[i];
        hash *= 17;
    }
    hash %= 256;
    return hash;
}

int main() {
    Timer timer;
    double elapsedTime;
    char* input[] = {
        
    };
    timer.start();
    int res = 0;
    for(int i = 0; i < 4000; i++) {
        res += hash_str(input[i]);
    }
    timer.stop();
    printf("%i\n", res);
    printf("Time taken %lf μs\n", timer.getElapsedTimeInMicroSec());
    return 0;
}