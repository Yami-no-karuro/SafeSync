#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#include "huffman.h"

static void huf_free_heap(MinHeap *heap) {
    free(heap->array);
    free(heap);
}

static void huf_free_tree(MinHNode *node) {
    if (!node) 
        return;
    
    huf_free_tree(node->left);
    huf_free_tree(node->right);
    free(node);
}

static MinHNode *huf_new_node(unsigned char item, unsigned freq) {
    MinHNode *node = malloc(sizeof(MinHNode));
    if (!node) {
        perror("malloc failed");
        exit(1);
    }
    
    node->left = node->right = NULL;
    node->item = item;
    node->freq = freq;
    
    return node;
}

static MinHeap *huf_create_min_heap(unsigned capacity) {
    MinHeap *heap = malloc(sizeof(MinHeap));
    if (!heap) {
        perror("malloc failed");
        exit(1);
    }
    
    heap->size = 0;
    heap->capacity = capacity;
    heap->array = malloc(capacity * sizeof(MinHNode *));
    
    if (!heap->array) {
        perror("malloc failed");
        free(heap);
        exit(1);
    }
    
    return heap;
}

static void huf_swap_nodes(MinHNode **a, MinHNode **b) {
    MinHNode *t = *a;
    *a = *b;
    *b = t;
}

static void huf_min_heapify(MinHeap *heap, int idx) {
    int smallest = idx, l = 2 * idx + 1, r = 2 * idx + 2;
    if (l < (int)heap->size && heap->array[l]->freq < heap->array[smallest]->freq)
        smallest = l;
    
    if (r < (int)heap->size && heap->array[r]->freq < heap->array[smallest]->freq)
        smallest = r;
    
    if (smallest != idx) {
        huf_swap_nodes(&heap->array[smallest], &heap->array[idx]);
        huf_min_heapify(heap, smallest);
    }
}

static int huf_is_size_one(MinHeap *heap) {
    return (heap->size == 1);
}

static MinHNode *huf_extract_min(MinHeap *heap) {
    MinHNode *min = heap->array[0];
    heap->array[0] = heap->array[--heap->size];
    huf_min_heapify(heap, 0);
    return min;
}

static void huf_insert_min_heap(MinHeap *heap, MinHNode *node) {
    int i = heap->size++;
    while (i && node->freq < heap->array[(i-1)/2]->freq) {
        heap->array[i] = heap->array[(i-1)/2];
        i = (i-1)/2;
    }
    
    heap->array[i] = node;
}

static void huf_build_min_heap(MinHeap *heap) {
    for(int i = (heap->size-2)/2; i >= 0; --i)
        huf_min_heapify(heap, i);
}

static int huf_is_leaf(MinHNode *node) {
    return !(node->left) && !(node->right);
}

static MinHeap *huf_build_heap(unsigned freq[256]) {
    MinHeap *heap = huf_create_min_heap(256);
    for(int i = 0; i < 256; ++i)
        if (freq[i])
            heap->array[heap->size++] = huf_new_node((unsigned char)i, freq[i]);
    
    huf_build_min_heap(heap);
    return heap;
}

static MinHNode *huf_build_huffman_tree(unsigned freq[256]) {
    MinHeap *heap = huf_build_heap(freq);
    while (!huf_is_size_one(heap)) {
        MinHNode *left = huf_extract_min(heap);
        MinHNode *right = huf_extract_min(heap);
        MinHNode *top = huf_new_node('$', left->freq + right->freq);
        
        top->left = left;
        top->right = right;
        huf_insert_min_heap(heap, top);
    }
    
    MinHNode *root = huf_extract_min(heap);
    huf_free_heap(heap);
    return root;
}

static void huf_build_code_table(MinHNode *root, char *code, int top, char codes[256][MAX_TREE_HT]) {
    if (root->left) {
        code[top] = '0';
        huf_build_code_table(root->left, code, top+1, codes);
    }
    
    if (root->right) {
        code[top] = '1';
        huf_build_code_table(root->right, code, top+1, codes);
    }
    
    if (huf_is_leaf(root)) {
        code[top] = '\0';
        strcpy(codes[root->item], code);
    }
}

void huf_compress(const char *input_file, const char *output_file) {
    FILE *in = fopen(input_file, "rb");
    if (!in) {
        perror("Failed to open input file");
        exit(1);
    }
    
    FILE *out = fopen(output_file, "wb");
    if (!out) {
        perror("Failed to open output file");
        fclose(in);
        exit(1);
    }

    fseek(in, 0, SEEK_END);
    long size = ftell(in);
    if (size <= 0) {
        fclose(in);
        fclose(out);
        return;
    }
    
    rewind(in);

    unsigned freq[256] = {0};
    int c;
    
    while ((c = fgetc(in)) != EOF)
        freq[(unsigned char)c]++;

    fwrite(freq, sizeof(unsigned), 256, out);
    uint32_t original_size = (uint32_t)size;
    fwrite(&original_size, sizeof(uint32_t), 1, out);

    MinHNode *root = huf_build_huffman_tree(freq);
    char codes[256][MAX_TREE_HT] = {{0}};
    char code[MAX_TREE_HT];
    
    huf_build_code_table(root, code, 0, codes);

    unsigned char buf = 0;
    int bits = 0;
    
    rewind(in);
    
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

    huf_free_tree(root);
    fclose(in);
    fclose(out);
}

void huf_decompress(const char *input_file, const char *output_file) {
    FILE *in = fopen(input_file, "rb");
    if (!in) {
        perror("Failed to open input file");
        exit(1);
    }
    
    FILE *out = fopen(output_file, "wb");
    if (!out) {
        perror("Failed to open output file");
        fclose(in);
        exit(1);
    }

    fseek(in, 0, SEEK_END);
    long size = ftell(in);
    if (size <= 0) {
        fclose(in);
        fclose(out);
        return;
    }
    
    rewind(in);

    unsigned freq[256];
    fread(freq, sizeof(unsigned), 256, in);
    uint32_t original_size;
    fread(&original_size, sizeof(uint32_t), 1, in);

    MinHNode *root = huf_build_huffman_tree(freq);
    MinHNode *curr = root;
    size_t written = 0;

    int byte;
    while ((byte = fgetc(in)) != EOF && written < original_size) {
        for (int i = 7; i >= 0 && written < original_size; --i) {
            int bit = (byte >> i) & 1;
            curr = bit ? curr->right : curr->left;
            if (huf_is_leaf(curr)) {
                fputc(curr->item, out);
                curr = root;
                written++;
            }
        }
    }

    huf_free_tree(root);
    fclose(in);
    fclose(out);
}
