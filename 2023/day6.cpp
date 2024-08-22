#include <math.h>
#include <stdio.h>
#include "Timer.h"

int main() {
    Timer timer;
    double elapsedTime;
    timer.start();
    long res, res2;
    for (int j = 0; j < 1000000; j++) {
        long data[5][2] = {
        };

        res = 1;
        for (int i = 1; i < 5; i++) {
            long time = data[i][0];
            long distance = data[i][1];
            double c_1 = time/2;
            double c_2 = sqrt(c_1*c_1 - distance);
            long t_release_1 = (long) (c_1 - c_2);
            long t_release_2 = (long) (c_1 + c_2);
            res *= t_release_2 - t_release_1;
        }
        long time = data[0][0];
        long distance = data[0][1];
        double c_1 = time/2;
        double c_2 = sqrt(c_1*c_1 - distance);
        long t_release_1 = (long) (c_1 - c_2);
        long t_release_2 = (long) (c_1 + c_2);
        res2 = t_release_2 - t_release_1;
    }
    timer.stop();
    printf("%li\n", res);
    printf("%li\n", res2);
    printf("Time taken %lf ns\n", timer.getElapsedTimeInMicroSec()/1000);
    return 0;
}