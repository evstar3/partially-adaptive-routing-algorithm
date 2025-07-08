#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

int main()
{
    const uint8_t seed = 0xed;

    uint8_t state = seed;
    size_t period = 0;

    do {
        uint8_t new_bit = (state >> 4) ^ (state >> 3) ^ (state >> 2) ^ (state) & (uint8_t)1;
        state = (state >> 1) | (new_bit << 7);
        ++period;
    } while (state != seed);

    printf("%u\n", period);

    return 0;
}
