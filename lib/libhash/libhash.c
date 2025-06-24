#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "libhash.h"

unsigned long fnv1a(const char *data, size_t len)
{
    unsigned long hash = FNV_OFFSET_BASIS;
    for (size_t i = 0; i < len; i++) {
        hash ^= (uint8_t)data[i];
        hash *= FNV_PRIME;
    }

    return hash;
}

unsigned long fnv1a_file(const char *filename)
{
    FILE *f = fopen(filename, "rb");
    if (!f) {
        perror("fopen");
        return 0;
    }

    unsigned long hash = FNV_OFFSET_BASIS;
    unsigned char buffer[FNV_FILE_CHUNK_SIZE];
    size_t read_bytes;

    while ((read_bytes = fread(buffer, 1, FNV_FILE_CHUNK_SIZE, f)) > 0) {
        for (size_t i = 0; i < read_bytes; i++) {
            hash ^= buffer[i];
            hash *= FNV_PRIME;
        }
    }

    fclose(f);
    return hash;
}
