#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "huffman.h"

static MinHNode *newNode(char item, unsigned freq) {
    MinHNode *node = (MinHNode *)malloc(sizeof(MinHNode));
    node->left = node->right = NULL;
    node->item = item;
    node->freq = freq;

    return node;
}

static MinHeap *createMinHeap(unsigned capacity) {
    MinHeap *heap = (MinHeap *)malloc(sizeof(MinHeap));
    heap->size = 0;
    heap->capacity = capacity;
    heap->array = (MinHNode **)malloc(capacity * sizeof(MinHNode *));

    return heap;
}

static void swapNodes(MinHNode **a, MinHNode **b) {
    MinHNode *t = *a;
    *a = *b;
    *b = t;
}

static void minHeapify(MinHeap *heap, int idx) {
    int smallest = idx, l = 2 * idx + 1, r = 2 * idx + 2;
    if (l < (int)heap->size && heap->array[l]->freq < heap->array[smallest]->freq)
        smallest = l;

    if (r < (int)heap->size && heap->array[r]->freq < heap->array[smallest]->freq)
        smallest = r;

    if (smallest != idx) {
        swapNodes(&heap->array[smallest], &heap->array[idx]);
        minHeapify(heap, smallest);
    }
}

static int isSizeOne(MinHeap *heap) {
    return (heap->size == 1);
}

static MinHNode *extractMin(MinHeap *heap) {
    MinHNode *min = heap->array[0];
    heap->array[0] = heap->array[--heap->size];
    minHeapify(heap, 0);

    return min;
}

static void insertMinHeap(MinHeap *heap, MinHNode *node) {
    int i = heap->size++;
    while (i && node->freq < heap->array[(i - 1) / 2]->freq) {
        heap->array[i] = heap->array[(i - 1) / 2];
        i = (i - 1) / 2;
    }

    heap->array[i] = node;
}

static void buildMinHeap(MinHeap *heap) {
    for (int i = (heap->size - 2) / 2; i >= 0; --i)
        minHeapify(heap, i);
}

static int isLeaf(MinHNode *node) {
    return !(node->left) && !(node->right);
}

static MinHeap *buildHeap(unsigned freq[256]) {
    MinHeap *heap = createMinHeap(256);
    for (int i = 0; i < 256; ++i)
        if (freq[i])
            heap->array[heap->size++] = newNode((char)i, freq[i]);

    buildMinHeap(heap);
    return heap;
}

static MinHNode *buildHuffmanTree(unsigned freq[256]) {
    MinHeap *heap = buildHeap(freq);
    while (!isSizeOne(heap)) {
        MinHNode *left = extractMin(heap);
        MinHNode *right = extractMin(heap);
        MinHNode *top = newNode('$', left->freq + right->freq);

        top->left = left;
        top->right = right;
        insertMinHeap(heap, top);
    }

    return extractMin(heap);
}

static void buildCodeTable(MinHNode *root, char *code, int top, char codes[256][MAX_TREE_HT]) {
    if (root->left) {
        code[top] = '0';
        buildCodeTable(root->left, code, top + 1, codes);
    }

    if (root->right) {
        code[top] = '1';
        buildCodeTable(root->right, code, top + 1, codes);
    }

    if (isLeaf(root)) {
        code[top] = '\0';
        strcpy(codes[(unsigned char)root->item], code);
    }
}

void compress(const char *input_file, const char *output_file) {
    FILE *in = fopen(input_file, "rb");
    FILE *out = fopen(output_file, "wb");
    if (!in || !out) {
        perror("An unexpected error occurred while executing the function: \"compress\"");
        exit(1);
    }

    fseek(in, 0, SEEK_END);
    long size = ftell(in);
    if (size == 0) {
        fclose(in);
        fclose(out);
        return;
    }

    rewind(in);

    unsigned freq[256] = {0};
    int c;

    while ((c = fgetc(in)) != EOF)
        freq[(unsigned char)c]++;

    rewind(in);
    fwrite(freq, sizeof(unsigned), 256, out);

    MinHNode *root = buildHuffmanTree(freq);
    char codes[256][MAX_TREE_HT] = {{0}};
    char code[MAX_TREE_HT];

    buildCodeTable(root, code, 0, codes);

    unsigned char buf = 0;
    int bits = 0;

    while ((c = fgetc(in)) != EOF) {
        char *str = codes[(unsigned char)c];
        for (int i = 0; str[i]; ++i) {
            buf <<= 1;
            if (str[i] == '1')
                buf |= 1;

            bits++;
            if (bits == 8) {
                fputc(buf, out);
                bits = 0;
                buf = 0;
            }
        }
    }

    if (bits > 0) {
        buf <<= (8 - bits);
        fputc(buf, out);
    }

    fclose(in);
    fclose(out);
}

void decompress(const char *input_file, const char *output_file) {
    FILE *in = fopen(input_file, "rb");
    FILE *out = fopen(output_file, "wb");
    if (!in || !out) {
        perror("An unexpected error occurred while executing the function: \"decompress\"");
        exit(1);
    }

    fseek(in, 0, SEEK_END);
    long size = ftell(in);
    if (size == 0) {
        fclose(in);
        fclose(out);
        return;
    }

    rewind(in);

    unsigned freq[256];
    fread(freq, sizeof(unsigned), 256, in);

    MinHNode *root = buildHuffmanTree(freq);
    MinHNode *curr = root;

    int byte;
    while ((byte = fgetc(in)) != EOF) {
        for (int i = 7; i >= 0; --i) {
            int bit = (byte >> i) & 1;
            curr = bit ? curr->right : curr->left;
            if (isLeaf(curr)) {
                fputc(curr->item, out);
                curr = root;
            }
        }
    }

    fclose(in);
    fclose(out);
}
