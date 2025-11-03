#pragma once

#include "hls_stream.h"

typedef int DTYPE;
const int SIZE = 256;
const int BLOCK_SIZE = 32;

typedef struct
{
    DTYPE a[BLOCK_SIZE];
} blockvec;

typedef struct
{
    DTYPE out[BLOCK_SIZE][BLOCK_SIZE];
} blockmat;

void blockmatmul(hls::stream<blockvec> &Arows, hls::stream<blockvec> &Bcols,
                 blockmat &ABpartial, DTYPE iteration);
