#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

int main()
{
    const uint32_t seed = 0xdeadbeef;

    uint32_t state = seed;
    size_t period = 0;

    do {
        uint8_t new_bit = (state >> 7) ^ (state >> 6) ^ (state >> 2) ^ (state) & (uint8_t)1;
        state = (state >> 1) | ((uint32_t)new_bit << 31);
        ++period;
    } while (state != seed);

    printf("%u\n", period);

    return 0;
}
