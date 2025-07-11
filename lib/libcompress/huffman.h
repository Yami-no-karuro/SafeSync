#ifndef HUFFMAN_H
#define HUFFMAN_H

#define MAX_TREE_HT 256

typedef struct MinHNode {
    char item;
    unsigned freq;
    struct MinHNode *left, *right;
} MinHNode;

typedef struct MinHeap {
    unsigned size, capacity;
    MinHNode **array;
} MinHeap;

void huf_compress(const char *input_file, const char *output_file);
void huf_decompress(const char *input_file, const char *output_file);

#endif
